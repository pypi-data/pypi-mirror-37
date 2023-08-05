# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Init for telemetry package"""

import json
import logging
import os
from logging.handlers import RotatingFileHandler
from os.path import expanduser, join, dirname


AML_INTERNAL_LOGGER_NAMESPACE = "azureml.telemetry"
INSTRUMENTATION_KEY = '38e39c8b-2fbb-4a95-aa50-0c66384962a7'

# application insight logger name
LOGGER_NAME = 'ApplicationInsightLogger'
TELEMETRY_LOG_FILE_NAME = 'telemetry.log'
SEND_DIAGNOSTICS_KEY = 'send_diagnostics'
DIAGNOSTICS_VERBOSITY_KEY = 'diagnostics_verbosity'

# app insights logging
telemetry_handler = None

global_diagnostics_properties = {}


def _get_file_path():
    """
    getter for telemetry file path
    :return: telemetry file path
    :rtype: str
    """
    file_path = join(expanduser("~"), ".azureml", "telemetry.json")
    dir_name = dirname(file_path)
    try:
        os.mkdir(os.path.abspath(dir_name))
    except OSError:
        # Ignoring error if the path already exists.
        pass

    return file_path


def set_diagnostics_collection(send_diagnostics=True, verbosity=logging.INFO):
    """
    enable/disable diagnostics collection
    :param send_diagnostics: send diagnostics
    :type bool
    :param verbosity: diagnostics verbosity
    :type logging(const)
    :return: telemetry file path
    :rtype: str
    """
    file_path = _get_file_path()
    try:
        with open(file_path, "w+") as config_file:
            json.dump({SEND_DIAGNOSTICS_KEY: send_diagnostics,
                       DIAGNOSTICS_VERBOSITY_KEY: logging.getLevelName(verbosity)}, config_file, indent=4)
    except OSError as e:
        raise UserErrorException("Could not write the config file to: {}\n{}".format(file_path, str(e)))


def get_diagnostics_collection_info():
    """
    gets the current diagnostics collection status
    :return: usage statistics config
    :rtype: dict
    """
    file_path = _get_file_path()
    config = {}
    try:
        with open(file_path, 'r') as config_file:
            config = json.load(config_file)
    except OSError:
        config = {SEND_DIAGNOSTICS_KEY: False, DIAGNOSTICS_VERBOSITY_KEY: logging.getLevelName(logging.NOTSET)}

    return config.get(SEND_DIAGNOSTICS_KEY, False), config.get(DIAGNOSTICS_VERBOSITY_KEY,
                                                               logging.getLevelName(logging.NOTSET))


def add_diagnostics_properties(properties):
    """
    adds additional diagnostics properties
    :param properties:
    :type dict
    """
    global global_diagnostics_properties
    global_diagnostics_properties.update(properties)


def set_diagnostics_properties(properties):
    """
    sets the diagnostics properties
    :param properties:
    :type dict
    """
    global global_diagnostics_properties
    global_diagnostics_properties.clear()
    global_diagnostics_properties.update(properties)


def get_telemetry_log_handler(instrumentation_key=INSTRUMENTATION_KEY):
    """
    gets the telemetry log handler if enabled otherwise return null handler
    :param instrumentation_key
    :type str
    :return: telemetry handler if enabled else null log handler
    :rtype: logging.handler
    """
    diagnostics_enabled, verbosity = get_diagnostics_collection_info()
    if diagnostics_enabled:
        global telemetry_handler
        if telemetry_handler is None:
            app_insights_file_logger = logging.getLogger(AML_INTERNAL_LOGGER_NAMESPACE).getChild(__name__)
            app_insights_file_logger.propagate = False
            app_insights_file_handler = RotatingFileHandler(TELEMETRY_LOG_FILE_NAME, maxBytes=100000, backupCount=2)
            app_insights_file_logger.setLevel(logging.CRITICAL)
            app_insights_file_logger.addHandler(app_insights_file_handler)

            from azureml.telemetry.logging_handler import get_appinsights_log_handler
            global global_diagnostics_properties
            telemetry_handler = get_appinsights_log_handler(instrumentation_key, app_insights_file_logger,
                                                            properties=global_diagnostics_properties)
            telemetry_handler.setLevel(verbosity)
            return telemetry_handler
        return telemetry_handler

    return logging.NullHandler()


class UserErrorException(Exception):
    """
    Class for the user exceptions
    """
    def __init__(self, exception_message, **kwargs):
        """
        Initialize the user exception
        :param exception_message: exception message
        :param kwargs: arguments
        """
        super(UserErrorException, self).__init__(exception_message, **kwargs)
