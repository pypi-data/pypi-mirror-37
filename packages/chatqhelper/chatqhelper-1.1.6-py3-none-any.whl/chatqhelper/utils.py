import dateutil.parser
import datetime
import traceback
from chatqhelper.common import constants


def chunks(items, size):
    for i in range(0, len(items), size):
        yield items[i:i + size]


def str_to_ts(timestr):
    return dateutil.parser.parse(timestr).replace(tzinfo=datetime.timezone.utc).timestamp()

def err_to_dict(err):
    return {
        'exception': str(err.__class__.__name__),
        'message': str(err),
        'code': getattr(err, 'code', 500),
        'traceback': traceback.format_exc(),
        'service': constants.SERVICE_NAME,
        'hostname': constants.HOSTNAME
        }
