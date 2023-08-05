# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

import os
import warnings
from azureml._async import WorkerPool
from azureml._logging import ChainedIdentity
from azureml._restclient import RunHistoryClient
from azureml._restclient.artifacts_client import ArtifactsClient
from azureml._restclient.clientbase import ClientBase
from azureml._restclient.constants import RUN_ORIGIN


class RunHistoryService(ChainedIdentity):
    def __init__(self, project_context, logger):
        super(RunHistoryService, self).__init__(_parent_logger=logger)
        self._pool = WorkerPool(_parent_logger=logger)
        self._client = RunHistoryClient(project_context.get_history_service_ui(),
                                        project_context.get_auth(),
                                        project_context.subscription,
                                        project_context.resource_group,
                                        project_context.workspace,
                                        project_context.project,
                                        workerpool=self._pool,
                                        _parent_logger=logger)

        self._artifact_client = ArtifactsClient(project_context.get_history_service_ui(),
                                                project_context.get_auth(),
                                                project_context.subscription,
                                                project_context.resource_group,
                                                project_context.workspace,
                                                workerpool=self._pool,
                                                _parent_logger=logger)

        self._project_path = '{0}{1}'.format(project_context.get_history_service_ui(),
                                             project_context.get_experiment_uri_path())

    def __del__(self):
        if self._pool is not None:
            self._pool.shutdown()

    def get_runs(self, last=0):
        self._logger.info("Listing runs at: {0}".format(self._project_path))
        res = self._client.get_runs(last)
        return self._get_dict_result(res)

    def get_runs_by_parent_id(self, parent_id=None):
        self._logger.info("Listing runs by parent id at: {0}".format(self._project_path))
        res = self._client.get_runs_by_parent_id(parent_id=parent_id)
        return self._get_dict_result(res)

    def get_metrics_by_run_ids(self, run_ids):
        self._logger.info("Listing metrics by run ids at: {0}".format(self._project_path))
        res = self._client.get_metrics_by_run_ids(run_ids=run_ids)
        return self._get_dict_result(res)

    def get_run(self, run_id):
        self._logger.info("Listing run {0} at: {1}".format(run_id, self._project_path))
        run_dto = self._client.get_run(run_id)
        return RunHistoryClient.dto_to_dictionary(run_dto)

    def list_attachments(self, run_id):
        self._logger.info(
            "Listing run attachments at: {0}".format(self._project_path))
        res = self._artifact_client.get_artifact_by_run_id(RUN_ORIGIN, run_id)
        return self._get_dict_result(res)

    def get_run_attachment_content(self, run_id, attachment_name):
        self._logger.info("Getting run attachment {1} for run {2} at: {0}".format(
            self._project_path, attachment_name, run_id))

        artifact_uri_dto = self._artifact_client.get_artifact_uri(RUN_ORIGIN, run_id, attachment_name)
        if not artifact_uri_dto:
            warnings.warn("Cannot find the artifact '{0}' with run_id '{1}'".format(
                attachment_name, run_id))
            return

        artifact_uri = getattr(artifact_uri_dto, 'content_uri')
        is_text_file = attachment_name.endswith('.txt') or attachment_name.endswith(
            '.log') or attachment_name.endswith('.csv')
        if not is_text_file:
            self._logger.info(
                'file {0} maybe not text file, decoding to text format anyway'.format(attachment_name))

        return self._artifact_client.peek_artifact_content(artifact_uri)

    def download_run_attachment(self, run_id, file_name, save_to, overwrite):
        self._logger.info("Downloading run attachment {0} for run {1} at: {2}".format(
            file_name, run_id, self._project_path))

        new_file_path = os.path.join(save_to, file_name)
        head, tail = os.path.split(new_file_path)
        if os.path.exists(head):
            if os.path.exists(new_file_path) and not overwrite:
                self._logger.error(
                    'Found existing file {0} in {1}'.format(tail, head))
                return None
        else:
            os.makedirs(head)

        new_file_path = os.path.join(head, tail)

        self._artifact_client.download_artifact(RUN_ORIGIN, run_id, file_name, new_file_path)
        return new_file_path

    def list_metrics(self, run_id):
        self._logger.info("Listing run_metrics of run {0} at: {1}".format(
            run_id, self._project_path))
        res = self._client.get_metrics(run_id)
        return self._get_dict_result(res)

    def _get_dict_result(self, res_as_generator):
        return list(map(ClientBase.dto_to_dictionary, res_as_generator))
