# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

""" script_run.py for handling script runs. """
from __future__ import print_function
import sys
import time
import os
import re

from azureml.core.run import Run
from azureml.core.runconfig import RunConfiguration
from azureml.exceptions import ExperimentExecutionException, UserErrorException
from azureml._restclient.utils import create_session_with_retry

RUN_STARTING = "Starting"
RUN_PROVISIONING = "Provisioning"
RUN_PREPARING = "Preparing"
RUN_QUEUED = "Queued"
RUN_RUNNING = "Running"

# TODO These states don't exist in history service yet!
RUN_FINALIZING = "Finalizing"
RUN_CANCELREQUESTED = "CancelRequested"


class ScriptRun(Run):
    """
    An experiment run class.
    :param experiment: The experiment object
    :type experiment: azureml.core.experiment.Experiment
    :param run_id: Run id.
    :type run_id: str
    :param directory: The source directory
    :type directory: str
    :param _run_config:
    :type _run_config: RunConfiguration
    :param kwargs:
    :type kwargs: dict
    """

    RUN_TYPE = "azureml.scriptrun"

    def __init__(self, experiment, run_id, directory=None, _run_config=None, **kwargs):
        """
        The constructor method
        """
        from azureml._project.project import Project
        super(ScriptRun, self).__init__(experiment, run_id, **kwargs)
        project_object = Project(experiment=experiment, directory=directory, _disable_service_check=True)
        if _run_config is not None:
            self._run_config_object = RunConfiguration._get_run_config_object(directory, _run_config)
        else:
            # Get it from experiment in the cloud.
            self._run_config_object = RunConfiguration._get_runconfig_using_runid(experiment, run_id)
        self._project_object = project_object

    def wait_for_completion(self, show_output=False, wait_post_processing=False):
        """
        Waits for the completion of this run.
        Returns the status object after the wait.
        :param show_output: show_output=True shows the run output on sys.stdout.
        :type show_output: bool
        :param wait_post_processing: wait_post_processing=True waits for the post processing to
        complete after the run completes.
        :type wait_post_processing: bool
        :return: The status object.
        :rtype: dict
        """

        if show_output:
            try:
                self._stream_run_output(file_handle=sys.stdout, wait_post_processing=wait_post_processing)
            except KeyboardInterrupt:
                error_message = "The output streaming for the run interrupted.\n" \
                                "But the run is still executing on the compute target. \n" \
                                "To cancel the run, execute: " \
                                "az ml run cancel -r {0} -t {1} " \
                                "-p {2}".format(self._run_id, self._run_config_object.target,
                                                self._project_object.project_directory)

                raise ExperimentExecutionException(error_message)
        else:
            running_states = [RUN_STARTING, RUN_PREPARING, RUN_RUNNING, RUN_PROVISIONING, RUN_QUEUED]
            if wait_post_processing:
                running_states.append(RUN_FINALIZING)
                running_states.append(RUN_CANCELREQUESTED)

            current_status = None
            while current_status is None or current_status in running_states:
                time.sleep(1)
                current_status = self.get_status()

        return self.get_details()

    def cancel(self):
        """
        Cancels the ongoing run.
        """
        from azureml._execution import _commands
        _commands.cancel(self._project_object, self._run_config_object, self._run_id)

    def clean(self):
        """
        Removes the files corresponding to the current run on the target specified in the
        run configuration.
        :return: List of files deleted.
        :rtype: list
        """
        from azureml._execution import _commands
        return _commands.clean(self._project_object, self._run_config_object, run_id=self._run_id)

    def get_diagnostics(self, destination=None):
        """
        Returns the diagnostics for the run.

        :param destination: The destination path to store the diagnostics zip. If unspecified then the diagnostics
        zip would be stored in the project directory.
        :type destination: str
        :return: True if the diagnostics retrieval was successful.
        :rtype: bool
        """
        from azureml._execution import _commands
        if destination:
            head, tail = os.path.split(destination)
            if not os.path.exists(head):
                raise UserErrorException("{} directory doesn't exist.".format(head))
            if not tail.endswith(".zip"):
                raise UserErrorException("{} name is not suffixed with .zip".format(tail))

        return _commands.get_diagnostics(self._project_object, self._run_config_object, self._run_id,
                                         destination=destination)

    def get_details_with_logs(self):
        """
        :return: Returns the status for the run with log file contents
        :rtype: dict
        """
        from azureml._execution import _commands

        details = self.get_details()
        log_files = details["logFiles"]
        session = create_session_with_retry()

        for log_name in log_files:
            content = _commands._get_content_from_uri(log_files[log_name], session)
            log_files[log_name] = content
        return details

    @staticmethod
    def _from_run_dto(experiment, run_dto):
        """
        :param experiment:
        :type experiment: azureml.core.experiment.Experiment
        :param run_dto:
        :type run_dto: object
        :return: Returns the run
        :rtype: ScriptRun
        """
        return ScriptRun(experiment, run_dto.run_id)

    # For distributed jobs, the names will be like 60-control_log_rank_0.txt
    # We want to get the highest number in front (60-...) - the number in front is the priority.
    # but also the lowest number in back (rank_0) - lower ranks are usually more "primary"
    # (and if there aren't any ranks in the filenames, just return the latest one)
    @staticmethod
    def _get_last_log_primary_instance(logs):
        """
        :param logs:
        :type logs: list
        :return: Returns the last log primary instance.
        :rtype:
        """
        primary_ranks = ["rank_0", "worker_0"]
        rank_match_re = re.compile("(.*)_(.*?_.*?)\.txt")
        last_log_name = logs[-1]

        last_log_match = rank_match_re.match(last_log_name)
        if not last_log_match:
            return last_log_name

        last_log_prefix = last_log_match.group(1)
        matching_logs = sorted(filter(lambda x: x.startswith(last_log_prefix), logs))

        # we have some specific ranks that denote the primary, use those if found
        for log_name in matching_logs:
            match = rank_match_re.match(log_name)
            if not match:
                continue
            if match.group(2) in primary_ranks:
                return log_name

        # no definitively primary instance, just return the highest sorted
        return matching_logs[0]

    def _stream_run_output(self, file_handle=sys.stdout, wait_post_processing=False):
        """
        Streams the experiment run output to the specified file handle.
        By default the the file handle points to stdout
        :param file_handle: A file handle to stream the output to.
        :type file_handle: file
        :param wait_post_processing:
        :type wait_post_processing: bool
        :return:
        :rtype: list
        """

        from azureml._execution import _commands

        def incremental_print(log, printed, fileout):
            """
            :param log:
            :type log: dict
            :param printed:
            :type printed: int
            :param fileout:
            :type fileout: TestIOWrapper
            :return:
            :rtype: int
            """
            count = 0
            for line in log.splitlines():
                if count >= printed:
                    print(line, file=fileout)
                    printed += 1
                count += 1

            return printed

        def get_logs(status):
            """
            :param status:
            :type status: dict
            :return:
            :rtype: list
            """
            logs = [x for x in status["logFiles"] if re.match("azureml-logs/[\d]{2}.+\.txt", x)]
            logs.sort()
            return logs

        file_handle.write("RunId: {}\n".format(self._run_id))

        printed = 0
        current_log = None
        running_states = [RUN_STARTING, RUN_PREPARING, RUN_RUNNING, RUN_PROVISIONING, RUN_QUEUED]
        if wait_post_processing:
            running_states.append(RUN_FINALIZING)
            running_states.append(RUN_CANCELREQUESTED)

        self._current_details = self.get_details()
        session = create_session_with_retry()

        # TODO: Temporary solution to wait for all the logs to be printed in the finalizing state.
        while self._current_details["status"] in running_states or self._current_details["status"] == RUN_FINALIZING:
            file_handle.flush()
            time.sleep(1)
            self._current_details = self.get_details()  # TODO use FileWatcher

            # Check whether there is a higher priority log than the one we are currently streaming (current_log)
            available_logs = get_logs(self._current_details)
            # next_log is the log we should be following now, based on the available logs we just got
            next_log = ScriptRun._get_last_log_primary_instance(available_logs) if available_logs else None
            # if next_log != current_log, we need to switch to streaming next_log
            if available_logs and current_log != next_log:
                printed = 0
                current_log = next_log
                file_handle.write("\n")
                file_handle.write("Streaming " + current_log + "\n")
                file_handle.write("=" * (len(current_log) + 10) + "\n")
                file_handle.write("\n")

            if current_log:
                content = _commands._get_content_from_uri(self._current_details["logFiles"][current_log], session)
                printed = incremental_print(content, printed, file_handle)

                # TODO: Temporary solution to wait for all the logs to be printed in the finalizing state.
                if (self._current_details["status"] not in running_states and
                    self._current_details["status"] == RUN_FINALIZING and
                        "The experiment completed successfully. Finalizing run..." in content):
                    break

        file_handle.write("\n")
        file_handle.write("Execution Summary\n")
        file_handle.write("=================\n")
        file_handle.write("RunId: {}\n".format(self.id))
        file_handle.write("\n")
        file_handle.flush()


Run.add_type_provider(ScriptRun.RUN_TYPE, ScriptRun._from_run_dto)
