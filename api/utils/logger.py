import logging

log_format = '%(asctime)s - %(module)s/%(funcName)s - %(levelname)s - %(message)s'


def logger_config(module):
    """
    Logger function. Extends Python loggin module and set a custom config.
    params: Module Name. e.i: logger_config(__name__).
    return: Custom logger_config Object.
    """
    formatter = logging.Formatter(log_format) # "%(asctime)s %(levelname)s %(message)s"
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    custom_logger = logging.getLogger(module)
    custom_logger.setLevel(logging.DEBUG)

    custom_logger.addHandler(handler)

    return custom_logger

# log_level = logging.DEBUG
# logger = logging.getLogger(__name__)
# logger.setLevel(log_level)
# formatter = logging.Formatter(
#     fmt=log_format,
#     datefmt='%Y-%m-%d %H:%M:%S'
# )
# handler = logging.StreamHandler(sys.stdout)
# handler.setFormatter(formatter)
# logger.addHandler(handler)