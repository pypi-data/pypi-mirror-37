import dateutil.parser
import datetime


def chunks(items, size):
    for i in range(0, len(items), size):
        yield items[i:i + size]


def str_to_ts(timestr):
    dateutil.parser.parse(timestr).replace(tzinfo=datetime.timezone.utc).timestamp()