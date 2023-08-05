# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Access a experiment client"""
import copy

from .workspace_client import WorkspaceClient
from .clientbase import PAGINATED_KEY


class ExperimentClient(WorkspaceClient):
    """
    Experiment APIs

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
    :param project_name:
    :type project_name: str
    """

    def __init__(self,
                 host,
                 auth,
                 subscription_id,
                 resource_group,
                 workspace_name,
                 project_name,
                 **kwargs):
        """
        Constructor of the class.
        """
        super(ExperimentClient, self).__init__(host, auth, subscription_id,
                                               resource_group, workspace_name,
                                               **kwargs)
        self._project_name = project_name
        self._project_arguments = copy.deepcopy(self._workspace_arguments)
        self._project_arguments.append(self._project_name)

    @classmethod
    def create(cls, workspace, experiment_name, host=None, **kwargs):
        """Create a project client"""
        return cls(host,
                   workspace._auth_object,
                   workspace.subscription_id,
                   workspace.resource_group,
                   workspace.name,
                   experiment_name,
                   **kwargs)

    def _execute_with_project_arguments(self, func, *args, **kwargs):
        if not callable(func):
            raise TypeError('Argument is not callable')

        if self._custom_headers:
            kwargs["custom_headers"] = self._custom_headers
        args_list = []
        args_list.extend(self._project_arguments)
        if args:
            args_list.extend(args)
        is_paginated = kwargs.pop(PAGINATED_KEY, False)
        if is_paginated:
            return self._call_paginated_api(func, *args_list, **kwargs)
        else:
            return self._call_api(func, *args_list, **kwargs)

    def _combine_with_project_paginated_dto(self, func, count_to_download=0, *args, **kwargs):
        return self._combine_paginated_base(self._execute_with_project_arguments,
                                            func,
                                            count_to_download,
                                            *args,
                                            **kwargs)
