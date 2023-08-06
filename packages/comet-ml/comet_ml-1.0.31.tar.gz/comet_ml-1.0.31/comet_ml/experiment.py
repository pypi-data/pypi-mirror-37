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

This module contains comet base Experiment code

"""
from __future__ import print_function

import atexit
import inspect
import logging
import os
import os.path
import shutil
import sys
import tempfile
import traceback
from collections import defaultdict
from contextlib import contextmanager
from os.path import basename
import io

import six

from ._logging import (
    EXPERIMENT_OPTIMIZER_API_KEY_MISMTACH_WARNING,
    LOG_FIGURE_TOO_BIG,
    LOG_IMAGE_OS_ERROR,
    LOG_IMAGE_TOO_BIG,
    METRIC_ARRAY_WARNING,
)
from ._reporting import EXPERIMENT_CREATION_FAILED, GIT_PATCH_GENERATION_FAILED
from .comet import (
    Message,
    UploadFileMessage,
    config,
    generate_guid,
    get_cmd_args_dict,
    save_matplotlib_figure,
)
from .config import DEFAULT_UPLOAD_SIZE_LIMIT, get_config
from .console import get_std_logger
from .env_logging import get_env_details
from .feature_toggles import GIT_PATCH, GPU_MONITOR
from .file_uploader import compress_git_patch
from .git_logging import find_git_patch, get_git_metadata
from .gpu_logging import (
    DEFAULT_GPU_MONITOR_INTERVAL,
    GPULoggingThread,
    convert_gpu_details_to_metrics,
    get_gpu_static_info,
    get_initial_gpu_metric,
    is_gpu_details_available,
)
from .utils import is_list_like

LOGGER = logging.getLogger(__name__)


class BaseExperiment(object):
    """
    Experiment is a unit of measurable research that defines a single run with some data/parameters/code/results.

    Creating an Experiment object in your code will report a new experiment to your Comet.ml project. Your Experiment
    will automatically track and collect many things and will also allow you to manually report anything.

    You can create multiple objects in one script (such as when looping over multiple hyper parameters).

    """

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
        log_git_patch=True,
        disabled=False,
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
            log_git_patch: Default(True) - allow you to enable/disable the
                automatic collection of git patch
            disabled: Default(False) - allows you to disable all network
                communication with the Comet.ml backend. It is useful when you
                just needs to works on your machine-learning scripts and need
                to relaunch them several times at a time.
        """
        self.config = get_config()

        self.project_name = project_name

        if team_name is not None:
            LOGGER.warning(
                "The team_name argument is deprecated and will be removed by 10/1/18. Please use the workspace "
                "argument instead. See additional information here: https://www.comet.ml/docs/workspaces/"
            )

        self.workspace = workspace if workspace is not None else team_name

        self.params = {}
        self.metrics = {}
        self.others = {}

        self.log_code = log_code
        self.log_graph = log_graph
        self.auto_param_logging = auto_param_logging
        self.auto_metric_logging = auto_metric_logging
        self.parse_args = parse_args
        ## Default is "native" for regular environments, None for Jupyter:
        if auto_output_logging == "default":
            if self._in_jupyter_environment():
                self.auto_output_logging = None
            elif self._in_ipython_environment():
                self.auto_output_logging = None
            else:
                self.auto_output_logging = "native"
        else:
            self.auto_output_logging = auto_output_logging
        self.log_env_details = log_env_details
        self.log_git_metadata = log_git_metadata
        self.log_git_patch = log_git_patch
        self.disabled = disabled

        # Generate a unique identifier for this experiment.
        self.id = self._get_experiment_key()

        self.alive = False
        self.is_github = False
        self.focus_link = None
        self.upload_limit = DEFAULT_UPLOAD_SIZE_LIMIT

        self.streamer = None
        self.logger = None
        self.gpu_thread = None
        self.run_id = None
        self.project_id = None

        # If set to True, wrappers should only run the original code
        self.disabled_monkey_patching = False

        # Experiment state
        self.context = None
        self.curr_step = None

        self.figure_counter = 0

        self.feature_toggles = {}

        # Storage area for use by loggers
        self._storage = defaultdict(dict)

        self.optimization_id = self._get_optimization_id_for_api_key(self.api_key)

        # Cleanup old experiment before replace it
        if config.experiment is not None and config.experiment is not self:
            config.experiment._on_end(wait=False)

        config.experiment = self

    def clean(self):
        """ Clean the experiment loggers, useful in case you want to debug
        your scripts with IPDB.
        """
        self._on_end(wait=False)

    def end(self):
        """
        Use to indicate that the experiment is complete. Useful in
        Jupyter environments to signal comel.ml that the experiment
        has ended.

        In Jupyter, this will also upload the commands that created
        the experiment, from the beginning to the end of this
        session. See the Code tab at Comet.ml.
        """
        if self._in_jupyter_environment():
            source_code = self._get_jupyter_source_code()
            self.set_code(source_code)
        self._on_end(wait=True)

    def display(self, *args, **kwargs):
        """ Do nothing in the common case
        """
        pass

    def _get_experiment_key(self):
        return generate_guid()

    def _on_start(self):
        """ Called when the Experiment is started
        """
        self._mark_as_started()

    def _mark_as_started(self):
        pass

    def _mark_as_ended(self):
        pass

    def _on_end(self, wait=True):
        """ Called when the Experiment is replaced by another one or at the
        end of the script
        """
        LOGGER.debug("Experiment on_end called, wait %s", wait)

        successful_clean = True

        if self.logger is not None:
            LOGGER.debug("Cleaning STDLogger")
            self.logger.clean()

        if self.gpu_thread is not None:
            self.gpu_thread.close()
            if wait is True:
                LOGGER.debug("GPU THREAD before join")
                self.gpu_thread.join(2)
                LOGGER.debug("GPU THREAD after join")

        if self.streamer is not None:
            LOGGER.debug("Closing streamer")
            self.streamer.close()
            if wait is True:
                successful_clean = self.streamer.wait_for_finish()

        self._mark_as_ended()

        return successful_clean

    def _start(self):

        try:
            self.alive = self._setup_streamer()

            if not self.alive:
                LOGGER.debug("Experiment is not alive, exiting")
                return

            # Register the cleaning method to be called when the script ends
            atexit.register(self._on_end)

        except Exception:
            tb = traceback.format_exc()
            LOGGER.error("Run will not be logged", exc_info=True)
            self._report(event_name=EXPERIMENT_CREATION_FAILED, err_msg=tb)
            return None

        try:
            self._setup_std_logger()
        except Exception:
            LOGGER.error("Failed to setup the std logger", exc_info=True)

        try:
            self.filename = self._get_filename()
            self.set_filename(self.filename)
        except Exception:
            LOGGER.error("Failed to set run file name", exc_info=True)

        try:
            self.set_pip_packages()
        except Exception:
            LOGGER.error("Failed to set run pip packages", exc_info=True)

        try:
            if self.parse_args:
                self.set_cmd_args()
        except Exception:
            LOGGER.error("Failed to set run cmd args", exc_info=True)

        try:
            if self.log_code:
                self.set_code(self._get_source_code())
        except Exception:
            LOGGER.error("Failed to set run source code", exc_info=True)

        try:
            if self.log_env_details:
                self._log_env_details()
        except Exception:
            LOGGER.error("Failed to log environment details", exc_info=True)

        try:
            if is_gpu_details_available():
                self._start_gpu_thread()
            else:
                LOGGER.debug("GPU details unavailable, don't start the GPU thread")
        except Exception:
            LOGGER.error("Failed to start the GPU tracking thread", exc_info=True)

        try:
            if self.log_git_metadata:
                self.set_git_metadata()
        except Exception:
            LOGGER.error("Failed to log git metadata", exc_info=True)

        try:
            if self.log_git_patch:
                self._upload_git_patch()
        except Exception:
            tb = traceback.format_exc()
            self._report(event_name=GIT_PATCH_GENERATION_FAILED, err_msg=tb)
            LOGGER.error("Failed to log git patch", exc_info=True)

        self._on_start()

    def _report(self, *args, **kwargs):
        """ Do nothing, could be overridden by subclasses
        """
        pass

    def _setup_streamer(self):
        """
        Do the necessary work to create mandatory objects, like the streamer
        and feature flags
        """
        raise NotImplementedError()

    def _setup_std_logger(self):
        # Override default sys.stdout and feed to streamer.
        self.logger = get_std_logger(self.auto_output_logging, self.streamer)
        if self.logger is not None:
            self.logger.set_experiment(self)

    def _create_message(self):
        """
        Utility wrapper around the Message() constructor
        Returns: Message() object.

        """
        return Message(
            self.api_key,
            self.id,
            self.run_id,
            self.project_id,
            context=self.context,
            optimization_id=self.optimization_id,
        )

    def get_metric(self, name):
        return self.metrics[name]

    def get_parameter(self, name):
        return self.params[name]

    def get_other(self, name):
        return self.others[name]

    def get_key(self):
        """
        Returns the experiment key, useful for using with the ExistingExperiment class
        Returns: Experiment Key (String)
        """
        return self.id

    def log_other(self, key, value):
        """
        Reports key,value to the `Other` tab on Comet.ml. Useful for reporting datasets attributes,
        datasets path, unique identifiers etc.

        See [`log_parameter`](#experimentlog_parameter)

        Args:
            key: Any type of key (str,int,float..)
            value: Any type of value (str,int,float..)

        Returns: None

        """
        if self.alive:
            message = self._create_message()
            message.set_log_other(key, value)
            self.streamer.put_messge_in_q(message)

        self.others[key] = value

    def log_html(self, html):
        """
        Reports any HTML blob to the `HTML` tab on Comet.ml. Useful for creating your own rich reports.
        The HTML will be rendered as an Iframe. Inline CSS/JS supported.
        Args:
            html: Any html string. for example:
            ```
            experiment.log_html('<a href="www.comet.ml"> I love Comet.ml </a>')
            ```

        Returns: None

        """
        if self.alive:
            message = self._create_message()
            message.set_html(html)
            self.streamer.put_messge_in_q(message)

    def log_html_url(self, url, text=None, label=None):
        """
        Easy to use method to add a link to a URL in the `HTML` tab
        on comet.ml.

        Args:
            url: a link to a file or notebook, for example
            text: text to use a clickable word or phrase (optional; uses url if not given)
            label: text that preceeds the link

        Examples:

        >>> experiment.log_html_url("https://my-company.com/file.txt")

        Adds html similar to:

        <a href="https://my-company.com/file.txt">https://my-company.com/file.txt</a>

        >>> experiment.log_html_url("https://my-company.com/file.txt", "File")

        Adds html similar to:

        <a href="https://my-company.com/file.txt">File</a>

        >>> experiment.log_html_url("https://my-company.com/file.txt", "File", "Label")

        Adds html similar to:

        Label: <a href="https://my-company.com/file.txt">File</a>

        """
        text = text if text is not None else url
        if label:
            self.log_html(
                """<div><b>%s</b>: <a href="%s" target="_blank">%s</a></div>"""
                % (label, url, text)
            )
        else:
            self.log_html(
                """<div><a href="%s" target="_blank">%s</a></div>""" % (url, text)
            )

    def set_step(self, step):
        """
        Sets the current step in the training process. In Deep Learning each step is after feeding a single batch
         into the network. This is used to generate correct plots on comet.ml. You can also pass the step directly when reporting [log_metric](#experimentlog_metric), and [log_parameter](#experimentlog_parameter).

        Args:
            step: Integer value

        Returns: None

        """

        if step is not None:
            self.curr_step = step

    def log_epoch_end(self, epoch_cnt, step=None):
        """
        Logs that the  epoch finished. required for progress bars.

        Args:
            epoch_cnt: integer

        Returns: None

        """
        self.set_step(step)

        if self.alive:
            message = self._create_message()
            message.set_param("curr_epoch", epoch_cnt, step=self.curr_step)
            self.streamer.put_messge_in_q(message)

    def log_metric(self, name, value, step=None):
        """
        Logs a general metric (i.e accuracy, f1).

        e.g.
        ```
        y_pred_train = model.predict(X_train)
        acc = compute_accuracy(y_pred_train, y_train)
        experiment.log_metric("accuracy", acc)
        ```

        See also [`log_multiple_metrics`](#experimentlog_multiple_metrics)


        Args:
            name: String - name of your metric
            value: Float/Integer/Boolean/String
            step: Optional. Used as the X axis when plotting on comet.ml

        Returns: None

        """
        LOGGER.debug("Log metric: %s %r %r", name, value, step)

        self.set_step(step)

        if self.alive:
            message = self._create_message()

            if is_list_like(value):
                # Try to get the first value of the Array
                try:
                    if len(value) != 1:
                        raise TypeError()

                    if not isinstance(
                        value[0], (six.integer_types, float, six.string_types, bool)
                    ):
                        raise TypeError()

                    value = value[0]

                except (TypeError):
                    LOGGER.warning(METRIC_ARRAY_WARNING, value)
                    value = str(value)

            message.set_metric(name, value, self.curr_step)
            self.streamer.put_messge_in_q(message)

        # save state.
        self.metrics[name] = value

    def log_parameter(self, name, value, step=None):
        """
        Logs a single hyperparameter. For additional values that are not hyper parameters it's encouraged to use [log_other](#experimentlog_other).

        See also [`log_multiple_params`](#experimentlog_multiple_params).


        Args:
            name: String - name of your parameter
            value: Float/Integer/Boolean/String/List
            step: Optional. Used as the X axis when plotting on comet.ml

        Returns: None

        """
        self.set_step(step)

        if name in self.params and self.params[name] == value:
            return

        if self.alive:
            message = self._create_message()

            # Check if we have a list-like object or a string
            if is_list_like(value):
                message.set_params(name, value, self.curr_step)
            else:
                message.set_param(name, value, self.curr_step)

            self.streamer.put_messge_in_q(message)

        self.params[name] = value

    def log_figure(self, figure_name=None, figure=None):
        """
        Logs the global Pyplot figure or the passed one and upload its svg
        version to the backend.

        Args:
            figure_name: Optional. String - name of the figure
            figure: Optional. The figure you want to log. If not set, the
                    global pyplot figure will be logged and uploaded
        """
        if self.alive is False:
            return

        try:
            filename = save_matplotlib_figure(figure)
        except Exception:
            LOGGER.warning("Failing to save the matplotlib figure")
            # An error occured
            return

        # Check the filesize
        file_size = os.path.getsize(filename)
        if file_size > self.upload_limit:
            LOGGER.error(LOG_FIGURE_TOO_BIG, file_size, self.upload_limit)
            return

        # Pass additional url params
        figure_number = self.figure_counter
        self.figure_counter += 1
        url_params = {
            "step": self.curr_step,
            "figCounter": figure_number,
            "context": self.context,
            "runId": self.run_id,
        }

        if figure_name is not None:
            url_params["figName"] = figure_name

        self._file_upload(filename, "visualization", url_params)

    def log_image(self, file_path, file_name=None):
        """
        Logs the image located at given file_path. Images are displayed on the Graphics tab on Comet.ml

        Args:
            file_path: String - the file path of the image you wants to log
            file_name: String - Optional. A custom file name to be displayed
            on the dashboard. If not provided the filename from the `file_path` argument will be used.
        """
        if self.alive is False:
            return

        # Check the file size before reading it
        try:
            file_size = os.path.getsize(file_path)
            if file_size > self.upload_limit:
                LOGGER.error(LOG_IMAGE_TOO_BIG, file_path, file_size, self.upload_limit)
                return

        except OSError:
            LOGGER.error(LOG_IMAGE_OS_ERROR, file_path)
            return

        # Take the filename as a figure name if it wasn't provided
        if file_name is None:
            file_name = os.path.basename(file_path)

        # Prepare parameters
        figure_number = self.figure_counter
        self.figure_counter += 1
        url_params = {
            "step": self.curr_step,
            "context": self.context,
            "runId": self.run_id,
            "figName": file_name,
            "figCounter": figure_number,
        }

        self._file_upload(file_path, "visualization", url_params, copy_to_tmp=True)

    def log_current_epoch(self, value):
        if self.alive:
            message = self._create_message()
            message.set_metric("curr_epoch", value)
            self.streamer.put_messge_in_q(message)

    def log_multiple_params(self, dic, prefix=None, step=None):
        """
        Logs a dictionary of multiple parameters.
        See also [log_parameter](#experimentlog_parameter).

        e.g:
        ```
        experiment = Experiment(api_key="MY_API_KEY")
        params = {
            "batch_size":64,
            "layer1":"LSTM(128)",
            "layer2":"LSTM(128)",
            "MAX_LEN":200
        }

        experiment.log_multiple_params(params)
        ```
        """
        self.set_step(step)

        if self.alive:
            for k in sorted(dic):
                if prefix is not None:
                    self.log_parameter(prefix + "_" + str(k), dic[k], self.curr_step)
                else:
                    self.log_parameter(k, dic[k], self.curr_step)

    def log_multiple_metrics(self, dic, prefix=None, step=None):
        """
        Logs a key,value dictionary of metrics.
        See also [`log_metric`](#experimentlog_metric)
        """
        self.set_step(step)

        if self.alive:
            for k in sorted(dic):
                if prefix is not None:
                    self.log_metric(prefix + "_" + str(k), dic[k], self.curr_step)
                else:
                    self.log_metric(k, dic[k], step)

    def log_dataset_hash(self, data):
        try:
            import hashlib

            data_hash = hashlib.md5(str(data).encode("utf-8")).hexdigest()
            self.log_parameter("dataset_hash", data_hash[:12])
        except Exception:
            LOGGER.warning("Failed to create dataset hash")

    def set_code(self, code):
        """
        Sets the current experiment script's code. Should be called once per experiment.
        Args:
            code: String. Experiment source code.
        """
        if self.alive and code is not None:
            message = self._create_message()
            message.set_code(code)
            self.streamer.put_messge_in_q(message)

    def set_model_graph(self, graph):
        """
        Sets the current experiment computation graph.
        Args:
            graph: String. Usually JSON represented graph.
        """
        if self.alive:

            LOGGER.debug("Set model graph called")

            if type(graph).__name__ == "Graph":  # Tensorflow Graph Definition
                from google.protobuf import json_format

                graph_def = graph.as_graph_def()
                graph = json_format.MessageToJson(graph_def)

            message = self._create_message()
            message.set_graph(graph)
            self.streamer.put_messge_in_q(message)

    def set_filename(self, fname):
        """
        Sets the current experiment filename.
        Args:
            fname: String. script's filename.
        """
        if self.alive:
            message = self._create_message()
            message.set_filename(fname)
            self.streamer.put_messge_in_q(message)

    def set_name(self, name):
        """
        Set a name for the experiment. Useful for filtering and searching on Comet.ml.
        Will shown by default under the `Other` tab.
        Args:
            name: String. A name for the experiment.
        """
        self.log_other("Name", name)

    def set_pip_packages(self):
        """
        Reads the installed pip packages using pip's CLI and reports them to server as a message.
        Returns: None

        """
        if self.alive:
            try:
                import pkg_resources

                installed_packages = [d for d in pkg_resources.working_set]
                installed_packages_list = sorted(
                    ["%s==%s" % (i.key, i.version) for i in installed_packages]
                )
                message = self._create_message()
                message.set_installed_packages(installed_packages_list)
                self.streamer.put_messge_in_q(message)
            except Exception:
                LOGGER.warning("Failing to collect the installed pip packages")

    def set_cmd_args(self):
        if self.alive:
            args = get_cmd_args_dict()
            LOGGER.debug("Command line arguments %r", args)
            if args is not None:
                for k, v in args.items():
                    self.log_parameter(k, v)

    # Context context-managers

    @contextmanager
    def train(self):
        """
        A context manager to mark the beginning and the end of the training
        phase. This allows you to provide a namespace for metrics/params.
        For example:

        ```
        experiment = Experiment(api_key="MY_API_KEY")
        with experiment.train():
            model.fit(x_train, y_train)
            accuracy = compute_accuracy(model.predict(x_train),y_train) # returns the train accuracy
            experiment.log_metric("accuracy",accuracy) # this will be logged as train accuracy based on the context.
        ```

        """
        # Save the old context and set the new one
        old_context = self.context
        self.context = "train"

        yield self

        # Restore the old one
        self.context = old_context

    @contextmanager
    def validate(self):
        """
        A context manager to mark the beginning and the end of the validating
        phase. This allows you to provide a namespace for metrics/params.
        For example:

        ```
        with experiment.validate():
            pred = model.predict(x_validation)
            val_acc = compute_accuracy(pred, y_validation)
            experiment.log_metric("accuracy", val_acc) # this will be logged as validation accuracy based on the context.
        ```


        """
        # Save the old context and set the new one
        old_context = self.context
        self.context = "validate"

        yield self

        # Restore the old one
        self.context = old_context

    @contextmanager
    def test(self):
        """
        A context manager to mark the beginning and the end of the testing phase. This allows you to provide a namespace for metrics/params.
        For example:

        ```
        with experiment.test():
            pred = model.predict(x_test)
            test_acc = compute_accuracy(pred, y_test)
            experiment.log_metric("accuracy", test_acc) # this will be logged as test accuracy based on the context.
        ```

        """
        # Save the old context and set the new one
        old_context = self.context
        self.context = "test"

        yield self

        # Restore the old one
        self.context = old_context

    def get_keras_callback(self):
        """
        Returns an instance of Comet.ml's Keras callback. This callback is already added to your Keras `model.fit()` callbacks list automatically, to report model training metrics to Comet.ml.


        e.g:
        ```
        experiment = Experiment(api_key="MY_API_KEY")
        comet_callback = experiment.get_keras_callback()
        ```

        Returns: Comet.ml Keras callback.

        """
        if self.alive:
            from comet_ml.frameworks import KerasCallback

            return KerasCallback(
                self,
                log_params=self.auto_param_logging,
                log_metrics=self.auto_metric_logging,
                log_graph=self.log_graph,
            )

        from comet_ml.frameworks import EmptyKerasCallback

        return EmptyKerasCallback()

    def disable_mp(self):
        """ Disabling the auto-collection of metrics and monkey-patching of
        the Machine Learning frameworks.
        """
        self.disabled_monkey_patching = True

    def _get_jupyter_source_code(self):
        """
        Get the Jupyter source code from the history. Assumes that this
        method is run in a jupyter environment.

        Returns the command-history as a string that lead to this point.
        """

        def in_format(n):
            return "_i%s" % n

        import IPython

        ipy = IPython.get_ipython()
        source = io.StringIO()
        n = 1
        while in_format(n) in ipy.ns_table["user_local"]:
            source.write("# %%%% In [%s]:\n" % n)
            source.write(ipy.ns_table["user_local"][in_format(n)])
            source.write("\n\n")
            n += 1
        return source.getvalue()

    def _get_source_code(self):
        """Inspects the stack to detect calling script. Reads source code
        from disk and logs it.
        """
        if self._in_jupyter_environment():
            return None  # upload it with experiment.end()
        else:
            for frame in inspect.stack(context=1):
                module = inspect.getmodule(frame[0])
                if module.__name__ not in ("comet_ml.experiment", "comet_ml"):
                    filename = module.__file__.rstrip("cd")
                    with open(filename) as f:
                        return f.read()

        LOGGER.warning("Failed to find source code module")

    def _in_jupyter_environment(self):
        """
        Check to see if code is running in a Jupyter environment,
        including jupyter notebook, lab, or console.
        """
        try:
            import IPython
        except Exception:
            return False

        ipy = IPython.get_ipython()
        if ipy is None or not hasattr(ipy, "kernel"):
            return False
        else:
            return True

    def _in_ipython_environment(self):
        """
        Check to see if code is running in an IPython environment.
        """
        try:
            import IPython
        except Exception:
            return False

        ipy = IPython.get_ipython()
        if ipy is None:
            return False
        else:
            return True

    def _get_filename(self):
        """
        Get the filename of the executing code, if possible.
        """
        if self._in_jupyter_environment():
            return "Jupyter interactive"
        elif sys.argv:
            pathname = os.path.dirname(sys.argv[0])
            abs_path = os.path.abspath(pathname)
            filename = os.path.basename(sys.argv[0])
            full_path = os.path.join(abs_path, filename)
            return full_path

        return None

    def set_git_metadata(self):
        if self.alive:
            current_path = os.getcwd()

            git_metadata = get_git_metadata(current_path)

            if git_metadata:
                message = self._create_message()
                message.set_git_metadata(git_metadata)
                self.streamer.put_messge_in_q(message)

    def _upload_git_patch(self):
        if not self.alive:
            return

        if not self.feature_toggles[GIT_PATCH]:
            LOGGER.debug("Git patch uploading turned off by feature toggle")
            return

        current_path = os.getcwd()
        git_patch = find_git_patch(current_path)
        if not git_patch:
            LOGGER.debug("Git patch is empty, nothing to upload")
            return

        archive, zip_path = compress_git_patch(git_patch)
        self._file_upload(zip_path, "git-patch")
        LOGGER.debug("Git patch upload launched")

    def _log_env_details(self):
        if self.alive:
            message = self._create_message()
            message.set_env_details(get_env_details())
            self.streamer.put_messge_in_q(message)

    def _get_optimization_id_for_api_key(self, api_key):
        if config.optimizer is not None:
            if config.optimizer.api_key == api_key:
                return config.optimizer.id

            else:
                LOGGER.warning(EXPERIMENT_OPTIMIZER_API_KEY_MISMTACH_WARNING)
        return None

    def _start_gpu_thread(self):
        if not self.alive:
            return

        if not self.feature_toggles[GPU_MONITOR]:
            LOGGER.debug("GPU monitoring turned off by feature toggle")
            return

        # First sends the static info as a message
        gpu_static_info = get_gpu_static_info()
        message = self._create_message()
        message.set_gpu_static_info(gpu_static_info)
        self.streamer.put_messge_in_q(message)

        # Them sends the one-time metrics
        one_time_gpu_metrics = get_initial_gpu_metric()
        metrics = convert_gpu_details_to_metrics(one_time_gpu_metrics)
        for metric in metrics:
            self.log_metric(metric["name"], metric["value"])

        # Now starts the thread that will be called recurrently
        self.gpu_thread = GPULoggingThread(
            DEFAULT_GPU_MONITOR_INTERVAL, self._log_gpu_details
        )
        self.gpu_thread.start()

        # Connect the streamer and the gpu thread
        self.streamer.on_gpu_monitor_interval = self.gpu_thread.update_internal

    def _log_gpu_details(self, gpu_details):
        metrics = convert_gpu_details_to_metrics(gpu_details)
        for metric in metrics:
            self.log_metric(metric["name"], metric["value"])

    def _file_upload(
        self, file_path, upload_type, url_params=None, file_name=None, copy_to_tmp=False
    ):
        # If we cannot remove the uploaded file or need the file content will
        # be frozen to the time the upload call is made, pass copy_to_tmp with
        # True value
        if copy_to_tmp is True:
            # Ensure we pass the correct file_name
            if file_name is None:
                file_name = basename(file_path)

            tmpfile = tempfile.NamedTemporaryFile(delete=False)
            shutil.copyfile(file_path, tmpfile.name)
            file_path = tmpfile.name

        upload_message = UploadFileMessage(
            file_path,
            file_name,
            upload_type,
            url_params,
            self.project_id,
            self.id,
            self.api_key,
        )
        self.streamer.put_messge_in_q(upload_message)
