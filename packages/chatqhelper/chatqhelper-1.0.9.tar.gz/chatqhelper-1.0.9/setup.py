from setuptools import setup
import os

setup(
      name='chatqhelper',
      version=os.environ['RELEASE_VERSION'],
      description='chatqhelper',
      url='https://github.com/ChatQSG/chatq-helping-hand',
      author='ChatQ',
      author_email='',
      packages=['chatqhelper'],
      install_requires=[
            'paho-mqtt==1.3.1',
            'schedule==0.5.0'
      ],
      zip_safe=False
)