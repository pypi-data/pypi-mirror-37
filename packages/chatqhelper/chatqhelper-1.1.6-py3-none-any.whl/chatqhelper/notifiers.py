from chatqhelper import debug, utils
from chatqhelper.mqtt import MqttErrorPublisher
from chatqhelper.slack import SlackErrorNotifier
from chatqhelper.common import constants
import traceback
from functools import wraps


def notify_on_err(stream=None):
    """
    stream: handler object
    """
    def decorator(function):
        @wraps(function)
        def try_cach(*args, **kwargs):
            try:
                return function(*args, **kwargs)
            except Exception as e:
                if issubclass(stream, ErrorStreamHandler):
                    stream.handle(e)
                raise e
        return try_cach
    return decorator


class ErrorStreamHandler():
    @classmethod
    def handle(cls, error, client=None):
        pass


class MqttErrorStreamHandler(ErrorStreamHandler):
    # brand new class publisher with new client
    _mqtt_publisher = MqttErrorPublisher()
    @classmethod
    def handle(cls, error):
        error = utils.err_to_dict(error)
        cls._mqtt_publisher.publish(error)


class SlackErrorStreamHandler(ErrorStreamHandler):
    @classmethod
    def handle(cls, error):
        error_msg = utils.err_to_dict(error)
        SlackErrorNotifier.notify(error_msg)
