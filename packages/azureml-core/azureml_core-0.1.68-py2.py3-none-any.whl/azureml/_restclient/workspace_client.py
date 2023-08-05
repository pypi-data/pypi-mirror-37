# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# ---------------------------------------------------------
"""Access workspace client"""
from .clientbase import ClientBase, PAGINATED_KEY


class WorkspaceClient(ClientBase):
    """
    Run History APIs

    :param host: The base path for the server to call.
    :type host: str
    :param auth: Client authentication
    :type auth: azureml.core.authentication.AbstractAuthentication
    :param subscription_id:
    :type subscription_id: str
    :param resource_group_name:
    :type resource_group_name: str
    :param workspace_name:
    :type workspace_name: str
    """
    OLD_ROUTE = "old"
    NEW_ROUTE = "new"

    def __init__(self,
                 host,
                 auth,
                 subscription_id,
                 resource_group,
                 workspace_name,
                 **kwargs):
        """
        Constructor of the class.
        """
        self._subscription_id = subscription_id
        self._resource_group = resource_group
        self._workspace_name = workspace_name
        host = host if host else self.get_cluster_url(auth)
        self._workspace_arguments = [self._subscription_id,
                                     self._resource_group,
                                     self._workspace_name]
        super(WorkspaceClient, self).__init__(host, auth, **kwargs)
        self._custom_headers = {}
        self.api_route = WorkspaceClient.NEW_ROUTE

    @classmethod
    def create(cls, workspace, host=None, **kwargs):
        """create a new workspace client"""
        return cls(host,
                   workspace._auth_object,
                   workspace.subscription_id,
                   workspace.resource_group,
                   workspace.name,
                   **kwargs)

    def get_workspace_uri_path(self):
        """
        :param workspace_object:
        :type workspace_object: azureml.core.workspace.Workspace
        :return:
        """
        return ("/subscriptions/{}/resourceGroups/{}/providers"
                "/Microsoft.MachineLearningServices"
                "/workspaces/{}").format(self._subscription_id,
                                         self._resource_group,
                                         self._workspace_name)

    def get_cluster_url(self, auth):
        """get service url"""
        from azureml._base_sdk_common.service_discovery import get_history_service_url
        from requests.exceptions import RequestException
        from azureml.exceptions import ProjectSystemException

        try:
            return get_history_service_url(auth, self.get_workspace_uri_path())
        except RequestException as response_exception:
            if response_exception.response.status_code == 404:
                raise ProjectSystemException(("Local folder is not linked"
                                              "to a Machine Learning",
                                              "project in Azure"))
            else:
                raise ProjectSystemException(str(response_exception.response))

    def _execute_with_workspace_arguments(self, func, *args, **kwargs):
        if not callable(func):
            raise TypeError('Argument is not callable')

        if self._custom_headers:
            kwargs["custom_headers"] = self._custom_headers

        args_list = []
        args_list.extend(self._workspace_arguments)
        if args:
            args_list.extend(args)
        is_paginated = kwargs.pop(PAGINATED_KEY, False)
        if is_paginated:
            return self._call_paginated_api(func, *args_list, **kwargs)
        else:
            return self._call_api(func, *args_list, **kwargs)

    def _combine_with_workspace_paginated_dto(self, func, count_to_download=0, *args, **kwargs):
        return self._combine_paginated_base(self._execute_with_workspace_arguments,
                                            func,
                                            count_to_download,
                                            *args,
                                            **kwargs)

    def list_experiments(self):
        """
        list all experiments
        :return: a generator of ~_restclient.models.ExperimentDto
        """
        if self.api_route == WorkspaceClient.OLD_ROUTE:
            self._logger.debug("Experiment calls do not support old routes, calling experiment route")
        return self._execute_with_workspace_arguments(self._client.experiment.list,
                                                      is_paginated=True)

    def get_experiment(self, experiment_name, is_async=False):
        """
        list all experiments in a workspace
        :return: a generator of ~_restclient.models.ExperimentDto
        :param is_async bool: execute request asynchronously
        :return:
            If is_async parameter is True,
            the request is called asynchronously.
            The method returns azureml._async_task.AsyncTask object
            If parameter is_async is False or missing,
            return: ~_restclient.models.ExperimentDto
        """
        if self.api_route == WorkspaceClient.OLD_ROUTE:
            self._logger.debug("Experiment calls do not support old routes, calling experiment route")
        return self._execute_with_workspace_arguments(self._client.experiment.get,
                                                      experiment_name=experiment_name,
                                                      is_async=is_async)
