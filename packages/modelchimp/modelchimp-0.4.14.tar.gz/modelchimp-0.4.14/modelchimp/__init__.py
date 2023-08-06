from __future__ import print_function
import requests
import json
import future
import six
import zlib
import sys
import inspect
import os
from . import metrics
import atexit
import queue
import time
import logging
import pickle
import cloudpickle
import tempfile
from datetime import datetime

# Optional imports
library_base_class = []
try:
    from sklearn.base import BaseEstimator
    library_base_class.append(BaseEstimator)
except ImportError:
    pass

try:
    from keras.engine.training import Model
    from . import mckeras
    library_base_class.append(Model)
except ImportError as e:
    pass


from .sklearn_tracker import sklearn_loader
from .tracker_thread import TrackerThread
from .event_queue import event_queue
from .connection_thread import WSConnectionThread, RestConnection
from .utils import generate_uid, current_string_datetime, is_uuid4_pattern
from .enum import ClientEvent
from .log import log_dict_config
from modelchimp import settings

LOG = logging.getLogger(__name__)
LOG.setLevel(logging.DEBUG)
#LOG.config.dictConfig(log_dict_config)

class PlatformLibraryType(object):
    SKLEARN = '1'
    KERAS = '2'
    CHOICES = (
        (SKLEARN, 'Sklearn'),
        (KERAS, 'Keras')
    )


class Track:
    URL = "https://www.modelchimp.com/"

    def __init__(self, key):
        self._session = requests.Session()
        self._features = []
        self._model = None
        self._evaluation = []
        self._deep_learning_parameters = []
        self._algorithm = ""
        self._http_headers = {}
        self._project_id = ""
        self._platform_library = ""
        self.__authenticate(key)
        self.__parse_ml_code()

    def add_evaluation(self, eval_name, eval_value):
        if not isinstance(eval_name, str):
            raise Exception("Evaluation name should be a string")

        if eval_name == "":
            raise Exception("Evaluation name should not be empty")

        if not ( isinstance(eval_value, int) or isinstance(eval_value, float) ):
            raise Exception("Evaluation value should be a number")

        self._evaluation.append({'key': eval_name, 'value': eval_value})

    def show(self):
        '''
        Prints the details that is going to be synced to the cloud
        '''
        print("\n")
        print("---Model Parameter List---")
        for obj in self._model:
            model_text = "%s : %s" % (obj['key'], obj['value'])
            print(model_text)

        print("\n")
        print("---Evaluation List---")
        for obj in self._evaluation:
            evaluation_text = "%s : %s" % ( obj['key'],
                                            obj['value'])
            print(evaluation_text)

    def save(self, name=None):
        '''
        Save the details to the ModelChimp cloud
        '''

        ml_model_url = Track.URL + 'api/ml-model/'
        result = {
            "name": name,
            "features": json.dumps(self._features),
            "model_parameters": json.dumps(self._model),
            "evaluation_parameters": json.dumps(self._evaluation),
            "deep_learning_parameters": json.dumps(self._deep_learning_parameters),
            "project": self._project_id,
            "algorithm": self._algorithm,
            "platform": "PYTHON",
            "platform_library": self._platform_library
        }

        if self._algorithm == "" and len(self._evaluation) == 0:
            print("No model or evaluation data to save")
            return None

        # Check if its python script
        frame = inspect.stack()[1]
        module = inspect.getmodule(frame[0])
        try:
            filename = module.__file__
            with open(filename, 'rb') as f:
                save_request = self._session.post(ml_model_url, data=result,
                files={"code_file": f}, headers=self._http_headers)
        except AttributeError:
            save_request = self._session.post(ml_model_url, data=result,
                            headers=self._http_headers)

        # Success Message
        if self._algorithm != "" and len(self._evaluation) == 0:
            success_message = "ML Model successfully saved"
        elif  self._algorithm == "" and len(self._evaluation) != 0:
            success_message = "Evaluation metrics successfully saved"
        else:
            success_message = "ML Model and Evaluation metrics successfully \
            saved"

        if save_request.status_code == 201:
            print(success_message)
        else:
            print("The data could not be saved")

    def __authenticate(self, key):
        authentication_url = Track.URL + 'api/decode-key/'
        auth_data = {"key": key}

        request_auth = self._session.post(authentication_url, data=auth_data)
        # Check if the request got authenticated
        if request_auth.status_code != 200:
            raise requests.exceptions.RequestException(
                "Authentication failed. Have you added the correct key")

        # Get the authenticated token and assign it to the header
        token = json.loads(request_auth.text)['token']
        self._http_headers = {'Authorization': 'Token ' + token}
        self._project_id = json.loads(request_auth.text)['project_id']

    def __parse_ml_code(self):
        ml_code_dict = inspect.stack()[2][0].f_locals
        keys = list(ml_code_dict)

        for key in keys:
            value = ml_code_dict[key]
            try:
                if isinstance(value, BaseEstimator):
                    self._platform_library = PlatformLibraryType.SKLEARN
                    self._model = self.__dict_to_kv(value.get_params())
                    self._algorithm = value.__class__.__name__

                if isinstance(value, Model):
                    self._platform_library = PlatformLibraryType.KERAS
                    keras_model_params = value.__dict__
                    self._algorithm = value.__class__.__name__
                    self._deep_learning_parameters = mckeras._get_layer_info(value.layers) if self._algorithm == 'Sequential' else []

                if isinstance(value, str) or isinstance(value, unicode):
                    if mckeras.get_compile_params(value):
                        keras_compile_params = mckeras.get_compile_params(value)

                    if mckeras.get_fit_params(value):
                        keras_fit_params = mckeras.get_fit_params(value)

            except NameError as e:
                pass

        if self._platform_library == PlatformLibraryType.KERAS:
            keras_model_params.update(keras_compile_params)
            keras_model_params.update(keras_fit_params)
            keras_model_params = mckeras._get_relevant_params(keras_model_params, ml_code_dict)
            self._model = self.__dict_to_kv(keras_model_params)

        if self._platform_library == "":
            print("There are no machine learning model in your existing scope. \
(Currently, sklearn and keras models are recorded by ModelChimp)")

    def __dict_to_kv(self, dict_val):
        result = [{'key': k, 'value': v} for k, v in dict_val.items()]
        result.sort(key=lambda e: e['key'])

        return result


class Tracker:
    def __init__(self, key, host=None ,experiment_name=None, tracking=True, auto_log=False, existing_exp_id=None):
        self.key = key
        self.experiment_name = experiment_name
        self.host = host
        self.rest = None
        self.tracking = tracking
        self.auto_log = auto_log
        self._experiment_start = current_string_datetime()
        self._experiment_end = None

        if existing_exp_id:
            self.experiment_id = existing_exp_id
        else:
            self.experiment_id = generate_uid()

        self._initialize()


    def _initialize(self):
        # Get the filename path of the script
        frame = inspect.stack()[2]
        module = inspect.getmodule(frame[0])
        self._experiment_file = module.__file__

        if os.getenv('MODELCHIMP_DEBUG') == 'True':
            rest_address = "http://%s/" %(self.host,)
            ws_address = "ws://%s/ws/tracker/%s/" % (self.host, self.experiment_id)
        else:
            rest_address = "https://%s/" %(self.host,)
            ws_address = "wss://%s/ws/tracker/%s/" % (self.host, self.experiment_id)

        # Create the experiment
        self.rest = RestConnection(rest_address, self.key, self.experiment_name)
        if not self.tracking:
            return

        experiment_created_flag = self.rest.create_experiment(self.experiment_id, self._experiment_file)
        if not experiment_created_flag:
            return

        # Start the websocket
        self.web_socket = WSConnectionThread(ws_address)
        self.web_socket.start()

        # Start the tracker thread
        self.tracker_thread = TrackerThread(self.web_socket, self.rest,  self.key, self._experiment_file)
        self.tracker_thread.start()

        # Send experiment start
        event_queue.put({
            'type' : ClientEvent.EXPERIMENT_START,
            'value' : self._experiment_start
        })

        # Send the code file
        event_queue.put({
            'type' : ClientEvent.CODE_FILE,
            'value' : {
                'filename' : self._experiment_file,
                'experiment_id' : self.experiment_id
            }
        })

        settings.current_tracker = self

        # Scrape the parameters from the script objects
        if self.auto_log:
            sklearn_loader()

        atexit.register(self._on_end)


    def _on_end(self):
        self._experiment_end = current_string_datetime()
        event_queue.put({
            'type' : ClientEvent.EXPERIMENT_END,
            'value' : self._experiment_end
        })
        self.tracker_thread.stop()


    def add_param(self, param_name, param_value):

        # Perform the necessary checks
        if not isinstance(param_name, str):
            LOG.warning('param_name should be a string')
            return

        if param_name == "":
            LOG.warning('param_name cannot be empty')
            return

        if not self.tracking:
            return

        # Add the event to the queue
        eval_event = {'type': ClientEvent.MODEL_PARAM, 'value': {}}
        eval_event['value'] = { param_name : param_value }
        event_queue.put(eval_event)


    def add_multiple_params(self, params_dict):
        # Perform the necessary checks
        if not isinstance(params_dict, dict):
            LOG.warning('Please provide a dict for multiple parameters')
            return

        if not self.tracking:
            return

        for k in params_dict.keys():
            self.add_param(k, params_dict[k])


    def add_metric(self, metric_name, metric_value, epoch=None):
        # Perform the necessary checks
        if not isinstance(metric_name, str):
            LOG.warning('metric_name should be a string')
            return

        if metric_name == "":
            LOG.warning('metric_name cannot be empty')
            return


        if not ( isinstance(metric_value, int) or isinstance(metric_value, float) ):
            LOG.warning('metric_value should be a number')
            return

        if epoch is not None and not ( isinstance(epoch, int) or
                                        isinstance(epoch, float) ):
            LOG.warning('epoch should be a number')
            return

        if not self.tracking:
            return

        # Add the event to the queue
        metric_event = {'type': ClientEvent.EVAL_PARAM,
                        'value': {},
                        'epoch': epoch}
        metric_event['value'] = { metric_name : metric_value }
        event_queue.put(metric_event)


    def add_multiple_metrics(self, metrics_dict, epoch=None):
        # Perform the necessary checks
        if not isinstance(metrics_dict, dict):
            LOG.warning('Please provide a dict for multiple parameters')
            return

        if not self.tracking:
            return

        for k in metrics_dict:
            self.add_metric(k, metrics_dict[k], epoch)


    def add_duration_at_epoch(self, tag, seconds_elapsed, epoch):
        # Perform the necessary checks
        if not isinstance(tag, str):
            LOG.warning('tag should be a string')
            return

        if tag == "":
            LOG.warning('tag cannot be empty')
            return

        if not ( isinstance(seconds_elapsed, int) or
                isinstance(seconds_elapsed, float) ):
            LOG.warning('seconds_elapsed should be a number')
            return

        if epoch is None:
            LOG.warning('epoch should be present')
            return

        if epoch is not None and not ( isinstance(epoch, int) or
                                        isinstance(epoch, float) ):
            LOG.warning('epoch should be a number')
            return

        if not self.tracking:
            return

        # Add the event to the queue
        duration_event = {'type': ClientEvent.DURATION_PARAM,
                        'value': {},
                        'epoch': epoch}
        duration_event['value'] = { tag : seconds_elapsed }
        event_queue.put(duration_event)


    def add_dataset_id(self, id):
        if not isinstance(id, (int,float,str)):
            LOG.warning('Dataset id should be a number or string')
            return

        if not self.tracking:
            return

        dataset_id_event = {'type': ClientEvent.DATASET_ID,
                            'value': id}
        event_queue.put(dataset_id_event)


    def add_custom_object(self, name, object):
        '''
        Save the pickled version of the custom object
        '''
        if not isinstance(name, str):
            LOG.warning('Custom object name should be a string')
            return

        if not self.rest:
            print("Please instantiate the ModelChimp Tracker to store custom objects")
            return

        if not self.tracking:
            return

        compressed_object, filesize = self.__get_compressed_picke(object)
        result = {
            "name": name,
            "filesize": filesize,
            "project": self.rest.project_id,
            "ml_model": self.rest.model_id,
        }
        custom_object_url = 'api/experiment-custom-object/create/'


        print("Uploading custom object: %s" % name)
        save_request = self.rest.post(custom_object_url, data=result,
                        files={'custom_object_file': compressed_object})

        if save_request.status_code == 201:
            print("%s: custom object was successfully saved" % name)
        else:
            print("Custom object could not be saved.")


    def pull_custom_object(self, id):
        pull_object_url = 'api/experiment-custom-object/retrieve/%s/?custom-object-id=%s' % (self.rest.project_id, id)

        if not isinstance(id, str):
            LOG.warning('Custom object id should be a string')
            return

        # Check the id is of correct pattern
        if not is_uuid4_pattern(id):
            LOG.warning('Given custom object id is of wrong pattern. Please, insert the correct id')
            return

        if not self.tracking:
            return

        print("Downloading custom object with the id: %s" % id)
        request = self.rest.get(pull_object_url)

        if request.status_code == 400:
            print("Unable to retrieve custom object. Is it a valid custom object id?")

        custom_object = request.content
        custom_object = zlib.decompress(custom_object, 31)
        custom_object = pickle.loads(custom_object)

        return custom_object


    def add_custom_plot(self, name="exportedPlot.png", plt=None):
        '''
        Save the custom Mat plot
        '''
        if not isinstance(name, str):
            LOG.warning('Custom plot name should be a string')
            return

        if not self.rest:
            print("Please instantiate the ModelChimp Tracker to store custom plots")
            return

        if not self.tracking:
            return

        axes = plt.gca()
        if axes.has_data() is False:
            LOG.warning("Empty plot")
            return

        #Export the matplot as an image
        filepath = ("./" + name + ".svg").strip()
        plt.savefig(filepath, bbox_inches="tight", format="svg")
        imageFile = open(filepath, 'rb')
        filesize = os.path.getsize(filepath)

        result = {
            "name": name,
            "filesize": filesize,
            "project": self.rest.project_id,
            "ml_model": self.rest.model_id,
        }
        mat_plot_url = 'api/experiment-mat-plot/create/'

        print("Uploading custom plot: %s" % name)
        save_request = self.rest.post(mat_plot_url, data=result,
                        files={'mat_plot_file': imageFile})
        imageFile.close()

        if save_request.status_code == 201:
            print("%s: custom plot was successfully saved" % name)
        else:
            print("Custom plot could not be saved.")

        if os.path.exists(filepath):
            print("Removing temporary file.")
            os.remove(filepath)


    def pull_params(self, experiment_id):
        pull_params_url = 'api/experiment-pull-param/?experiment-id=' + experiment_id

        if not isinstance(experiment_id, str):
            LOG.warning('experiment_id should be a string')
            return

        if not self.tracking:
            return

        request = self.rest.get(pull_params_url)

        if request.status_code == 400:
            print("Have you provided the correct experiment id?")
            return

        if request.status_code == 403:
            print("You don't have permission for this experiment")
            return

        params = json.loads(request.text)

        return params


    def add_image(self, filepath, metric_dict=None, custom_file_name=None, epoch=None):
        '''
        Upload images that need to tracked corresponding to an experiment
        '''
        url = 'api/experiment-images/add-image/'

        if not os.path.isfile(filepath):
            LOG.warning('Image file does not exist at %s' % (filepath))
            return

        if metric_dict and not isinstance(metric_dict, dict):
            LOG.warning('metric_dict should be a dictionary for file: %s' % (filepath))
            return

        if metric_dict:
            for k in metric_dict:
                if not isinstance(metric_dict[k], (int,float)):
                    LOG.warning("Metric - %s is not a number" % (k,))
                    del(metric_dict[k])

        if custom_file_name and not isinstance(custom_file_name, str):
            LOG.warning('custom_file_name should be a string for file: %s' % (filepath))
            return

        if epoch and not isinstance(epoch, int):
            LOG.warning('epoch should be a dictionary for file: %s' % (filepath))
            return

        if not self.rest:
            print("Please instantiate the ModelChimp Tracker to store images")
            return

        if not self.tracking:
            return

        result = {
            "custom_file_name": custom_file_name,
            "metric_dict": json.dumps(metric_dict),
            "epoch": epoch,
            "project": self.rest.project_id,
            "ml_model": self.rest.model_id,
        }

        print("Uploading image: %s" % filepath)
        with open(filepath, 'rb') as f:
            save_request = self.rest.post(url, data=result,
                            files={'experiment_image': f})

        if save_request.status_code != 201:
            print("Image could not be saved: %s" % (filepath))


    def add_model_params(self, model, model_name=None):
        '''
        Extract the parameters out of a model object.
        Currently, only for scikit objects.

        Parameters
        ----------
        model : Model object whose parameters needs to be
            extracted
        model_name(optional) : Name of model for which the
            model parameters wil be stored. The name will
            be prefixed to each of the model parameter.

        Returns
        -------
        None
        '''

        # Check the parameters
        if model_name and not isinstance(model_name, str):
            LOG.warning('add_model_params: model_name should be a string')
            return

        if not isinstance(model, tuple(library_base_class)):
            LOG.warning('add_model_params: model is not supported')
            return

        if not self.tracking:
            return

        # Extrack the parameter of the models
        params = model.get_params()

        # Prefix the parameter with the model_name if present
        result = {}
        if model_name:
            for k in params.keys():
                new_key_name = "%s__%s" % (model_name, k)
                result[new_key_name] = params[k]
        else:
            result = params

        # Add to the queue
        self.add_multiple_params(result)


    def __get_compressed_picke(self, obj):
        pickled_obj = cloudpickle.dumps(obj,-1)
        z = zlib.compressobj(-1,zlib.DEFLATED,31)
        filesize =  sys.getsizeof(pickled_obj)
        gzip_compressed_pickle = z.compress(pickled_obj) + z.flush()

        return (gzip_compressed_pickle, filesize)
