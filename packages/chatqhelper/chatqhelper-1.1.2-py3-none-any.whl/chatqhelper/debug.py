import logging, sys
import traceback


def logger(name):
    # Setup log handler
    log_formatter = logging.Formatter('%(name)s:%(asctime)s [%(levelname)s] %(message)s')
    log_handler = logging.StreamHandler(stream=sys.stdout)
    log_handler.setFormatter(log_formatter)
    log_handler.setLevel(logging.DEBUG)

    # Setup logger
    logger = logging.getLogger(name)
    logger.addHandler(log_handler)
    logger.setLevel(logging.DEBUG)
    return logger


def log_traceback(logger):
    tb = traceback.format_exc()
    logger.exception(tb)
    return tb
