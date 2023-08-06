# -*- coding: utf-8 -*-
# *******************************************************
#   ____                     _               _
#  / ___|___  _ __ ___   ___| |_   _ __ ___ | |
# | |   / _ \| '_ ` _ \ / _ \ __| | '_ ` _ \| |
# | |__| (_) | | | | | |  __/ |_ _| | | | | | |
#  \____\___/|_| |_| |_|\___|\__(_)_| |_| |_|_|
#
#  Sign up for free at http://www.comet.ml
#  Copyright (C) 2015-2019 Comet ML INC
#  This file can not be copied and/or distributed without the express
#  permission of Comet ML Inc.
# *******************************************************

"""
Author: Boris Feld

This module contains logging configuration for Comet

"""
import json
import logging
from copy import copy

import requests
from comet_ml.json_encoder import NestedEncoder

MSG_FORMAT = "COMET %(levelname)s: %(message)s"
FILE_MSG_FORMAT = "[%(process)d-%(processName)s:%(thread)d] %(relativeCreated)d COMET %(levelname)s [%(filename)s:%(lineno)d]: %(message)s"

GO_TO_DOCS_MSG = " \nFor more details, please refer to: https://www.comet.ml/docs/python-sdk/warnings-errors"

INTERNET_CONNECTION_ERROR = (
    "Failed to establish connection to Comet server. Please check your internet connection. "
    "Your experiment would not be logged" + GO_TO_DOCS_MSG
)

INVALID_WORKSPACE_NAME = "Workspace %s doesn't exist."

INVALID_PROJECT_NAME = "project_name argument can't be empty."

INVALID_API_KEY = (
    "The given api key %s is invalid, please check it against the dashboard. "
    "Your experiment would not be logged" + GO_TO_DOCS_MSG
)

METRIC_ARRAY_WARNING = (
    "Cannot safely convert %r object to a scalar value, using it string"
    " representation for logging."
)

EXPERIMENT_OPTIMIZER_API_KEY_MISMTACH_WARNING = (
    "WARNING: Optimizer and Experiments API keys mismatch. Please use"
    " the same API key for both."
)


PARSING_ERR_MSG = """We failed to parse your parameter configuration file.

Type casting will be disabled for this run, please fix your configuration file.
"""

CASTING_ERROR_MESSAGE = """Couldn't cast parameter %r, returning raw value instead.
Please report it to comet.ml and use `.raw(%r)` instead of `[%r]` in the meantime."""

LOG_IMAGE_OS_ERROR = (
    "We failed to read file %s for uploading.\n"
    "Please double check the file path and permissions"
)

LOG_IMAGE_TOO_BIG = "File %s is bigger than the upload limit, %s > %s"

LOG_FIGURE_TOO_BIG = "Figure is bigger than the upload limit, %s > %s"

NATIVE_STD_WRAPPER_NOT_AVAILABLE = (
    "Native output logging mode is not available, fallbacking on basic output logging"
)

UNKOWN_STD_WRAPPER_SPEC = (
    "Unknown output logging mode: %s, fallbacking on basic output logging"
)

EXPERIMENT_LIVE = "Experiment is live on comet.ml %s\n"

OFFLINE_EXPERIMENT_END = (
    "To upload this offline experiment, run:\n" "    comet-offline-sender %s"
)

OFFLINE_SENDER_STARTS = "Starting the upload of the experiment"

OFFLINE_SENDER_ENDS = "The offline experiment has been uploaded on comet.ml %s\n"


class TracebackLessFormatter(logging.Formatter):
    def format(self, record):
        # Make a copy of the record to avoid altering it
        new_record = copy(record)

        # And delete exception informations so no traceback could be formatted
        # and displayed
        new_record.exc_info = None
        new_record.exc_text = None

        return super(TracebackLessFormatter, self).format(new_record)


WS_ON_OPEN_MSG = "WS Socket connection open"

WS_ON_CLOSE_MSG = "WS connection closed"


def shorten_record_name(record_name):
    """ Return the first part of the record (which can be None, comet or
    comet.connection)
    """
    if record_name is None:
        return record_name

    return record_name.split(".", 1)[0]


class HTTPHandler(logging.Handler):
    def __init__(self, url, api_key, experiment_key):
        super(HTTPHandler, self).__init__()
        self.url = url
        self.api_key = api_key
        self.experiment_key = experiment_key

    def mapLogRecord(self, record):
        return record.__dict__

    def emit(self, record):
        """
        Emit a record.

        Send the record to the Web server as JSON body
        """
        try:
            payload = {
                "apiKey": self.api_key,
                "record": self.mapLogRecord(record),
                "experimentKey": self.experiment_key,
                "levelname": record.levelname,
                "sender": record.name,
                "shortSender": shorten_record_name(record.name),
            }
            body = json.dumps(payload, cls=NestedEncoder)

            response = requests.post(
                self.url,
                data=body,
                headers={"Content-Type": "application/json;charset=utf-8"},
            )
            response.raise_for_status()
        except (KeyboardInterrupt, SystemExit):
            raise

        except:
            self.handleError(record)

    def handleError(self, record):
        # Hide errors to avoid bad interaction with console logging
        pass


def setup(config):
    root = logging.getLogger("comet_ml")
    root.setLevel(logging.DEBUG)

    # Don't send comet-ml to the application logger
    root.propagate = False

    # Add handler
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.setFormatter(TracebackLessFormatter(MSG_FORMAT))
    root.addHandler(console)

    # The std* logger might conflicts with the logging if a log record is
    # emitted for each WS message as it would results in an infinite loop. To
    # avoid this issue, all log records after the creation of a message should
    # be at a level lower than info as the console handler is set to info
    # level.

    # Add an additional file handler
    log_file_path = config["comet.logging.file"]
    log_file_level = config["comet.logging.file_level"]
    if log_file_path is not None:
        file_handler = logging.FileHandler(log_file_path)

        if log_file_level is not None:
            log_file_level = log_file_level.upper()
            file_handler.setLevel(log_file_level)
        else:
            file_handler.setLevel(logging.DEBUG)

        file_handler.setFormatter(logging.Formatter(FILE_MSG_FORMAT))
        root.addHandler(file_handler)


def setup_http_handler(url, api_key, experiment_key):
    root = logging.getLogger("comet_ml")

    http_handler = HTTPHandler(url, api_key, experiment_key)
    http_handler.setLevel(logging.INFO)
    root.addHandler(http_handler)

    return http_handler
