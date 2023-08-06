from slackclient import SlackClient
from  chatqhelper import debug
import os, json, time
from functools import wraps
from chatqhelper.mqtt import MqttClient
from chatqhelper.common import constants
from queue import Queue
import datetime

logger = debug.logger("chatqhelper.notifier")

class SlackNotifier():
    """
    requires environment variable SLACK_NOTIFIER_TOKEN
    provides functions:
        - slack_message
    """
    _client = SlackClient(os.environ.get('SLACK_NOTIFIER_TOKEN')) if os.environ.get('SLACK_NOTIFIER_TOKEN') else None
    def __init__(self, token=None):
        # partial singleton, only create a new client if the token is given.
        self._client = SlackClient(token) if token else self.__class__._client
        self._message_queue = []
    
    def notify(self, message, channel, username=''):
        """
        post a message to slack channel
        args:
            - message: string, the text to post
            - channel: string, channel to post the message to
            - username: notifier name, default to service name (hostname of the container)
        """
        sc = self._client
        if not sc:
            logger.warning('invalid slack client or token. message not set')
            return

        res = sc.api_call(
            'chat.postMessage',
            channel=channel, text=message,
            username=username or constants.SERVICE_NAME)
        if not res.get('ok'):
            logger.error(res)

    def attach(self, attachments, channel, username=''):
        """
        post a message to slack channel
        args:
            - message: string, the text to post
            - channel: string, channel to post the message to
            - username: notifier name, default to service name (hostname of the container)
        """
        sc = self._client
        if not sc:
            logger.warning('invalid slack client or token. message not set')
            return

        res = sc.api_call(
            'chat.postMessage',
            channel=channel, attachments=attachments,
            username=username or constants.SERVICE_NAME)
        if not res.get('ok'):
            logger.error(res)


class SlackErrorNotifier():
    INTERNAL_ERR = 'Internal Error'
    CLIENT_ERR = 'Client Error'

    _notifier = SlackNotifier()
    _error_stack = []

    @classmethod
    def notify(cls, error_msg, defer=False):
        if defer:
            cls._error_stack.append(error_msg)
        else:
            cls._notify([error_msg])

    @classmethod
    def defer_notify(cls, error_msg):
        cls.notify(error_msg, defer=True)

    @classmethod
    def _get_error_stack(cls, size=20):
        errors = cls._error_stack[:20]
        cls._error_stack = cls._error_stack[20:]
        return errors

    @staticmethod
    def _error_msg_to_attachment(error_msg):
        code = error_msg.get('code', 500)
        color = 'warning' if 400 <= code < 500 else 'danger'
        source_topic = error_msg.get('source_topic')
        exception = error_msg.get('exception')
        message = error_msg.get('message')
        source_payload = error_msg.get('source_payload')
        tb = error_msg.get('traceback')
        service = error_msg.get('service', '')
        container = error_msg.get('hostname', '')

        attachment = {
            'author_name': service,
            'pretext': exception + ': ' + message,
            'color': color,
            'text': '*payload*\n```{}```\n*traceback*\n```{}```'.format(json.dumps(source_payload, indent=4), tb),
            'footer': container,
            'ts': datetime.datetime.utcnow().timestamp()
        }

        if source_topic:
            attachment.update({
                'title': source_topic,
                'title_link': 'https://chatq.gitbook.io/chatq-development-documentation/chatq/message-bus-topic-paths/chat-project#'+source_topic.replace('/', '-'),
            })

        return attachment

    @classmethod
    def _notify(cls, errors=[]):
        if not errors:
            errors = cls._get_error_stack()

        if not isinstance(errors, list):
            errors = [errors]

        attachments = [cls._error_msg_to_attachment(err) for err in errors]
        if attachments:
            cls._notifier.attach(
                attachments=attachments,
                channel=constants.SLACK_ERR_CHANNEL)
