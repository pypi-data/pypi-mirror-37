from slackclient import SlackClient
from  chatqhelper import debug, scheduler
import os, json, time
from functools import wraps
from chatqhelper.mqtt import MqttClient
from chatqhelper.notifiers import ErrorStreamHandler, notify_on_err
from chatqhelper.common import constants

logger = debug.logger("chatqhelper.notifier")

class SlackNotifier():
    def __init__(self, token=None, username=None):
        if not token:
            token = os.environ.get('SLACK_NOTIFIER_TOKEN')
        self._client = None if not token else SlackClient(token)
        # username is the service where the message is sent
        self._username = username or constants.SERVICE_NAME
    
    def slack_message(self, message, channel, notifier_name=''):
        sc = self._client
        if not sc:
            logger.warning('invalid slack client or token. message not set')
            return
        res = sc.api_call(
            'chat.postMessage',
            channel=channel, text=message,
            username=notifier_name or self._username)
        if not res.get('ok'):
            logger.error(res)

class SlackErrorStreamHandler(ErrorStreamHandler):
    _slack_notifier = SlackNotifier()
    @classmethod
    def handle(cls, error, notifier_name=''):
        client = cls._slack_notifier
        client.slack_message(
            message=str(error), 
            channel=constants.SLACK_ERR_CHANNEL,
            notifier_name=notifier_name
        )

slack_err_notifier = notify_on_err(stream=SlackErrorStreamHandler)