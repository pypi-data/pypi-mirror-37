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

This module contains the code related to offline feature

"""
import json
import logging
import os
import os.path
import tempfile
import zipfile
from os.path import dirname, join
from zipfile import ZipFile

from jsonschema import validate

from ._logging import OFFLINE_EXPERIMENT_END, OFFLINE_SENDER_ENDS, OFFLINE_SENDER_STARTS
from ._reporting import EXPERIMENT_CREATED
from .comet import OfflineStreamer, generate_guid
from .config import get_config
from .connection import RestServerConnection, WebSocketConnection, get_backend_address
from .experiment import BaseExperiment
from .feature_toggles import FeatureToggles, get_feature_toggle_overrides
from .file_uploader import upload_file_thread
from .utils import local_timestamp

LOGGER = logging.getLogger(__name__)


class OfflineExperiment(BaseExperiment):
    def __init__(
        self,
        project_name=None,
        team_name=None,
        workspace=None,
        log_code=True,
        log_graph=True,
        auto_param_logging=True,
        auto_metric_logging=True,
        parse_args=True,
        auto_output_logging="default",
        log_env_details=True,
        log_git_metadata=True,
        disabled=False,
        offline_directory=None,
    ):
        """
        Creates a new experiment on the Comet.ml frontend.
        Args:
            project_name: Optional. Send your experiment to a specific project. Otherwise will be sent to `Uncategorized Experiments`.
                             If project name does not already exists Comet.ml will create a new project.
            team_name: Deprecated. Use workspace instead.
            workspace: Optional. Attach an experiment to a project that belongs to this workspace
            log_code: Default(True) - allows you to enable/disable code logging
            log_graph: Default(True) - allows you to enable/disable automatic computation graph logging.
            auto_param_logging: Default(True) - allows you to enable/disable hyper parameters logging
            auto_metric_logging: Default(True) - allows you to enable/disable metrics logging
            parse_args: Default(True) - allows you to enable/disable automatic parsing of CLI arguments
            auto_output_logging: Default("native") - allows you to select
                which output logging mode to use. The default is `"native"`
                which will log all output even when it originated from a C
                native library. You can also pass `"simple"` which will work
                only for output made by Python code. If you want to disable
                automatic output logging, you can pass `None`.
            log_env_details: Default(True) - log various environment
                informations in order to identify where the script is running
            log_git_metadata: Default(True) - allow you to enable/disable the
                automatic collection of git details
            disabled: Default(False) - allows you to disable all network
                communication with the Comet.ml backend. It is useful when you
                just needs to works on your machine-learning scripts and need
                to relaunch them several times at a time.
            offline_directory: the directory used to save the offline archive
                for the experiment.
        """
        self.tmpdir = tempfile.mkdtemp()
        self.config = get_config()

        if offline_directory is None:
            offline_directory = self.config["comet.offline_directory"]

        if offline_directory is None:
            raise ValueError("OfflineExperiment needs an offline directory")

        self.offline_directory = offline_directory

        # Temporary workaround
        self.api_key = "offline"

        # Start and ends time
        self.start_time = None
        self.stop_time = None

        super(OfflineExperiment, self).__init__(
            project_name,
            team_name,
            workspace,
            log_code,
            log_graph,
            auto_param_logging,
            auto_metric_logging,
            parse_args,
            auto_output_logging,
            log_env_details,
            log_git_metadata,
            disabled,
        )

        if disabled is not True:
            self._start()

            if self.alive is True:
                self._report(event_name=EXPERIMENT_CREATED)

    def _start(self):
        self.start_time = local_timestamp()
        super(OfflineExperiment, self)._start()

    def _write_experiment_meta_file(self):
        meta_file_path = join(self.tmpdir, "experiment.json")
        meta = {
            "experiment_id": self.id,
            "project_name": self.project_name,
            "workspace": self.workspace,
            "log_code": self.log_code,
            "log_graph": self.log_graph,
            "auto_param_logging": self.auto_param_logging,
            "auto_metric_logging": self.auto_metric_logging,
            "parse_args": self.parse_args,
            "auto_output_logging": self.auto_output_logging,
            "disabled": self.disabled,
            "log_env_details": self.log_env_details,
            "log_git_metadata": self.log_git_metadata,
            "feature_toggles_overrides": get_feature_toggle_overrides(),
            "start_time": self.start_time,
            "stop_time": self.stop_time,
        }
        with open(meta_file_path, "w") as f:
            json.dump(meta, f)

    def _mark_as_ended(self):
        LOGGER.info("Starting saving the offline archive")
        self.stop_time = local_timestamp()

        self._write_experiment_meta_file()

        # ZIP the saved informations
        mode = 0o700
        try:
            os.mkdir(self.offline_directory, mode)
        except os.error:
            pass

        file_path = self._offline_zip_path()
        zipfile = ZipFile(file_path, "w")

        for file in os.listdir(self.tmpdir):
            zipfile.write(os.path.join(self.tmpdir, file), file)

        zipfile.close()

        # Display the full command to upload the offline experiment
        LOGGER.info(OFFLINE_EXPERIMENT_END, file_path)

    def _offline_zip_path(self):
        return os.path.join(self.offline_directory, "%s.zip" % self.id)

    def _setup_streamer(self):
        """
        Initialize the streamer and feature flags.
        """
        # Initiate the streamer
        self.streamer = OfflineStreamer(self.tmpdir, 0)

        # Start streamer thread.
        self.streamer.start()

        self.feature_toggles = FeatureToggles({}, self.config)

        # Mark the experiment as alive
        return True

    def _report(self, *args, **kwrags):
        # TODO WHAT TO DO WITH REPORTING?
        pass


def validate_experiment_file(experiment_content):
    with open(
        join(dirname(__file__), "schemas/offline-experiment.schema.json")
    ) as schema_file:
        schema = json.load(schema_file)

    return validate(experiment_content, schema)


def validate_ws_msg(ws_msg):
    with open(
        join(dirname(__file__), "schemas/offline-ws-msg.schema.json")
    ) as schema_file:
        schema = json.load(schema_file)

    return validate(ws_msg, schema)


def validate_file_upload_msg(file_upload_msg):
    with open(
        join(dirname(__file__), "schemas/offline-file-upload-msg.schema.json")
    ) as schema_file:
        schema = json.load(schema_file)

    return validate(file_upload_msg, schema)


def unzip_offline_archive(offline_archive_path):
    temp_dir = tempfile.mkdtemp()

    zip_file = zipfile.ZipFile(offline_archive_path, mode="r")

    # Extract the archive
    zip_file.extractall(temp_dir)

    return temp_dir


class OfflineSender(object):
    def __init__(self, api_key, offline_dir):
        self.config = get_config()
        self.api_key = api_key
        self.offline_dir = offline_dir
        self.counter = 0

        self.server_address = get_backend_address()

        self._read_experiment_file()

        self.connection = RestServerConnection(
            self.api_key, self.experiment_id, None, self.server_address
        )
        self.ws_connection = None
        self.focus_link = None
        self.upload_threads = []

    def send(self):
        self._handshake()

        self._status_report_start()

        LOGGER.info(OFFLINE_SENDER_STARTS)

        self._send_messages()

        self._status_report_end()

        self._send_start_ends_time()

    def _read_experiment_file(self):
        with open(join(self.offline_dir, "experiment.json")) as experiment_file:
            metadata = json.load(experiment_file)

        validate_experiment_file(metadata)

        self.experiment_id = generate_guid()
        self.project_name = metadata["project_name"]
        self.workspace = metadata["workspace"]
        self.start_time = metadata["start_time"]
        self.stop_time = metadata["stop_time"]

    def _handshake(self):
        run_id_results = self.connection.get_run_id(self.project_name, self.workspace)

        (
            self.run_id,
            self.ws_url,
            self.project_id,
            self.is_github,
            self.focus_link,
            self.upload_limit,
            feature_toggles,
            initial_offset,
        ) = run_id_results

        self.ws_connection = WebSocketConnection(self.ws_url, self.connection)
        self.ws_connection.start()
        self.ws_connection.wait_for_connection()

    def _send_messages(self):
        i = 0
        with open(join(self.offline_dir, "messages.json")) as messages_files:
            for i, line in enumerate(messages_files):
                message = json.loads(line)

                LOGGER.debug("Message %r", message)

                message_type = message["type"]

                if message_type == "ws_msg":
                    self._process_ws_msg(message)
                elif message_type == "file_upload":
                    self._process_upload_message(message)

        LOGGER.debug("Done sending %d messages", i)

    def _process_ws_msg(self, message):
        message = message["payload"]

        validate_ws_msg(message)

        # Inject api key and run_id
        message["apiKey"] = self.api_key
        message["runId"] = self.run_id
        message["projectId"] = self.project_id
        message["experimentKey"] = self.experiment_id

        # Todo this piece of code mimic format_messages_for_ws but
        # format_messages_for_ws accepts a list of messages objects
        # instead of a list of dicts
        if message["stdout"]:
            to_send = json.dumps([{"stdout": message}])
        else:
            to_send = json.dumps([{"log_data": message}])
        self.ws_connection.send(to_send)

    def _process_upload_message(self, message):
        message = message["payload"]

        validate_file_upload_msg(message)

        # Compute the url from the upload type
        url = self.connection.get_upload_url(message["upload_type"])

        additional_params = message["additional_params"]
        additional_params["runId"] = self.run_id

        upload_thread = upload_file_thread(
            project_id=self.project_id,
            experiment_id=self.experiment_id,
            file_path=join(self.offline_dir, message["file_path"]),
            upload_endpoint=url,
            api_key=self.api_key,
            additional_params=additional_params,
            clean=True,
        )
        self.upload_threads.append(upload_thread)
        LOGGER.debug("Processing uploading message done")
        LOGGER.debug("Upload threads %s", self.upload_threads)

    def _status_report_start(self):
        self.connection.update_experiment_status(
            self.run_id, self.project_id, True, offline=True
        )

    def _status_report_end(self):
        self.connection.update_experiment_status(
            self.run_id, self.project_id, False, offline=True
        )

    def _send_start_ends_time(self):
        self.connection.offline_experiment_start_end_time(
            self.run_id, self.start_time, self.stop_time
        )

    def _get_experiment_url(self):
        if self.focus_link:
            return self.focus_link + self.experiment_id

        return ""

    def close(self):
        if self.ws_connection is not None:
            self.ws_connection.close()
            self.ws_connection.wait_for_finish()

        for thread in self.upload_threads:
            thread.join()
        LOGGER.debug("Upload threads %r", self.upload_threads)

        LOGGER.info(OFFLINE_SENDER_ENDS, self._get_experiment_url())
