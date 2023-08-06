from setuptools import setup, find_packages
import os

setup(
      name='chatqhelper',
      version=os.environ['RELEASE_VERSION'],
      description='chatqhelper',
      url='https://github.com/ChatQSG/chatq-helping-hand',
      author='ChatQ',
      author_email='',
      packages=find_packages(),
      install_requires=[
            'paho-mqtt==1.3.1',
            'schedule==0.5.0',
            'gspread==3.0.1',
            'google-api-python-client==1.7.4',
            'oauth2client==4.1.3',
            'slackclient==1.3.0'
      ],
      zip_safe=False
)