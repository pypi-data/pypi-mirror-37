# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""
Auto ML common logging module.
"""
import logging

from azureml.telemetry import AML_INTERNAL_LOGGER_NAMESPACE, get_telemetry_log_handler
from logging.handlers import RotatingFileHandler
from threading import Lock

CRITICAL = logging.CRITICAL
ERROR = logging.ERROR
WARNING = logging.WARNING
INFO = logging.INFO
DEBUG = logging.DEBUG
NOTSET = logging.NOTSET

file_logging_handlers = {}
file_loggers = {}
log_cache_lock = Lock()

null_logger = logging.getLogger('automl_non_logger')
null_logger.addHandler(logging.NullHandler())
null_logger.propagate = False


def get_logger(log_file_name=None, verbosity=DEBUG):
    """
     Creates the logger with telemetry hook
     :param log_file_name: log file name
     :param verbosity: logging verbosity
     :return logger if log file name is provided otherwise null logger
     :rtype
     """
    if log_file_name is None:
        return null_logger

    with log_cache_lock:
        if (log_file_name, verbosity) in file_loggers:
            return file_loggers[(log_file_name, verbosity)]

        if log_file_name not in file_logging_handlers:
            fh = RotatingFileHandler(log_file_name, maxBytes=1000000, backupCount=1)
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(lineno)d : %(message)s')
            fh.setFormatter(formatter)
            file_logging_handlers[log_file_name] = fh

        # Create a high level logger at specified verbosity level
        logger_name = '%s_%s' % (log_file_name, str(verbosity))
        file_logger = logging.getLogger(AML_INTERNAL_LOGGER_NAMESPACE).getChild(logger_name)
        file_logger.addHandler(file_logging_handlers[log_file_name])
        file_logger.setLevel(verbosity)
        telemetry_handler = get_telemetry_log_handler()
        file_logger.addHandler(telemetry_handler)

        file_logger.propagate = False
        file_loggers[(log_file_name, verbosity)] = file_logger

        return file_logger


def cleanup_log_map(log_file_name=None, verbosity=DEBUG):
    """
    Cleanup log map
    :param log_file_name: log file name
    :param verbosity: log verbosity
    :return:
    """
    with log_cache_lock:
        file_loggers.pop((log_file_name, verbosity), None)


def _log_system_info(logger, prefix_message=None):
    """
    Logging cpu, memory and OS info.

    :param logger: logger object
    :param prefix_message: string that in the prefix in the log
    :return: None
    """
    if prefix_message is None:
        prefix_message = ''

    try:
        import psutil
        logger.info("{}CPU logical cores: {}, CPU cores: {}, virtual memory: {}, swap memory: {}.".format(
            prefix_message,
            psutil.cpu_count(), psutil.cpu_count(logical=False),
            psutil.virtual_memory().total, psutil.swap_memory().total)
        )
    except ImportError:
        logger.warning("psutil not found, skipping logging cpu and memory")

    import platform
    logger.info("{}Platform information: {}.".format(prefix_message, platform.platform()))
