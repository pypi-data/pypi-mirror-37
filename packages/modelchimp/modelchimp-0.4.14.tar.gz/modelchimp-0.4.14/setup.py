from setuptools import setup,find_packages

setup(
  name = 'modelchimp',
  packages = find_packages(),
  version = '0.4.14',
  description = 'Python client to upload the machine learning models data to the model chimp cloud',
  author = 'Samir Madhavan',
  author_email = 'samir.madhavan@gmail.com',
  url = 'https://www.modelchimp.com',
  keywords = ['modelchimp', 'ai', 'datascience'],
  install_requires=[
          'requests',
          'future',
          'six',
          'websocket-client',
          'pytz',
          'cloudpickle'
      ],
  classifiers = [],
)
