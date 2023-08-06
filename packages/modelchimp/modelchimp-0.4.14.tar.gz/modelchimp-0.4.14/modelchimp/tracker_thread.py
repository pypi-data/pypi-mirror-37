from threading import Thread
import time
from .event_queue import event_queue
import json
import queue
from .connection_thread import WSConnectionThread
from .enum import ClientEvent, ExperimentStatus

class TrackerThread(Thread):
    def __init__(self, websocket_connection, rest, key, code_file):
        Thread.__init__(self)
        self.stopped = False
        self.daemon = True
        self.key = key
        self.web_socket = websocket_connection
        self.rest = rest
        self.code_file = code_file
        self.beat_interval = 10
        self.last_beat_snapshot = time.time()


    def run(self):
        while not self.stopped:
            self.run_once()

    def run_once(self):
        try:
            if self.web_socket.is_connected():
                self.add_heart_beat()

                event = event_queue.get(10)
                self.handle_message(event)

            # Exit now if should stop
            if self.stopped:
                return
        except queue.Empty:
            pass

    def stop(self):
        self.stopped = True
        self._end()


    def handle_message(self, event):
        event['key'] = self.key
        self.web_socket.send(event)

    def add_heart_beat(self):
        current_beat = time.time()

        if current_beat > (self.last_beat_snapshot + self.beat_interval):
            event_queue.put({
                'type' : ClientEvent.HEART_BEAT,
            })
            self.last_beat_snapshot = current_beat

    def _end(self):
        print('Experiment has ended. Closing connection with ModelChimp.')

        while True:
            try:
                if self.web_socket.is_connected():
                    event = event_queue.get_nowait()
                    self.handle_message(event)
                else:
                    break
            except queue.Empty:
                self.web_socket.send({'type': ClientEvent.COMPLETED,
                                        'key': self.key,
                                        'value': ExperimentStatus.COMPLETED})
                break
        self.web_socket.stop()
