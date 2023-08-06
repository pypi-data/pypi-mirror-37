from  chatqhelper import debug, scheduler
import os, json, time
from functools import wraps


logger = debug.logger("chatqhelper.notifier")


class ErrorStreamHandler():
    @classmethod
    def handle(cls, error, client=None):
        pass


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
