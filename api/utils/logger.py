import datetime
import logging
import os

log_format = '%(levelname)s : %(asctime)s - %(module)s/%(funcName)s - %(message)s'

curr_dt = datetime.datetime.utcnow().replace(microsecond=0)

def get_logger(module):
    formatter = logging.Formatter(log_format) # "%(asctime)s %(levelname)s %(message)s"
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    file_handler = logging.FileHandler(os.getcwd() + f'/logs/log{curr_dt.strftime("%Y-%m-%d_%H%M%S")}.log')
    file_handler.setFormatter(formatter)

    custom_logger = logging.getLogger(module)
    custom_logger.setLevel(logging.DEBUG)

    custom_logger.addHandler(handler)
    custom_logger.addHandler(file_handler)

    return custom_logger
