# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

import logging
import os
import requests
import re

from abc import ABCMeta, abstractmethod
from azureml._base_sdk_common.service_discovery import get_history_service_url
from azureml._project.project_engine import ProjectEngineClient

from azureml.exceptions import ProjectSystemException

module_logger = logging.getLogger(__name__)

_PROJECT_FILE_ACCOUNT_ID = "AccountId"
_PROJECT_FILE_PROJECT_ID = "Id"
_PROJECT_FILE_FIELDS = [_PROJECT_FILE_ACCOUNT_ID, _PROJECT_FILE_PROJECT_ID]


def create_project_context(auth, subscription_id=None, resource_group=None,
                           workspace=None, project_name=None):
    """
    Creates the project context.
    :param auth: Authentication object.
    :type auth: azureml.core.authentication.AbstractAuthentication
    :param subscription_id: subscription id
    :type subscription_id: str
    :param resource_group: resource group name
    :type resource_group: str
    :param workspace: workspace name
    :type workspace: str
    :param project_name: project name
    :type project_name: str
    :return: A project context
    :rtype: ProjectContext
    """
    if resource_group or workspace or project_name:
        if not (subscription_id and resource_group and workspace and project_name):
            raise ProjectSystemException("Missing parameters error.\nyou must supply values for subscription_id, "
                                         "resource group, workspace and project.")
        project_context = ARMProjectContext(auth, subscription_id=subscription_id,
                                            resource_group=resource_group,
                                            workspace=workspace, project_name=project_name)
    else:
        project_context = get_engine_project_context(auth, os.getcwd())

    if not project_context:
        raise ProjectSystemException("Current directory is not an Azure Machine Learning project directory")

    return project_context


def get_engine_project_context(auth, project_path):
    """
    Returns the project context using the project information on disk, specified by project_path
    :param auth: auth object.
    :rtype auth: azureml.core.authentication.AbstractAuthentication
    :param project_path: The project path
    :type project_path: str
    :return: The project context.
    :rtype: ProjectContext
    """
    project_scope = ProjectEngineClient.get_project_scope_by_path(project_path)
    if not project_scope:
        return None

    return ARMProjectContext(auth,
                             re.search(r'/subscriptions/([^/]+)', project_scope).group(1),
                             re.search(r'/resourceGroups/([^/]+)', project_scope).group(1),
                             re.search(r'/workspaces/([^/]+)', project_scope).group(1),
                             re.search(r'/projects/([^/]+)', project_scope).group(1))


class ProjectMetadataFactory(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def create_project_metadata(self):
        pass


class ProjectContext(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_workspace_uri_path(self):
        pass

    def get_auth(self):
        """
        :return: Returns auth object.
        :rtype: azureml.core.authentication.AbstractAuthentication
        """
        pass

    @abstractmethod
    def get_history_service_ui(self):
        pass

    @abstractmethod
    def get_cloud_execution_service_address(self):
        pass


class ARMProjectContext(ProjectContext):
    def __init__(self, auth, subscription_id, resource_group, workspace, project_name):
        """

        :param auth: auth object.
        :type auth: azureml.core.authentication.AbstractAuthentication
        :param subscription_id:
        :param resource_group:
        :param workspace:
        :param project_name:
        :type project_name: str
        """
        self._auth = auth

        self._subscription_id = subscription_id
        self._resource_group = resource_group
        self._workspace = workspace
        self._project_name = project_name

    @property
    def subscription(self):
        return self._subscription_id

    @property
    def resource_group(self):
        return self._resource_group

    @property
    def workspace(self):
        return self._workspace

    @property
    def project(self):
        return self._project_name

    def get_workspace_uri_path(self):
        return "/subscriptions/{}/resourceGroups/{}/providers/Microsoft.MachineLearningServices" \
               "/workspaces/{}".format(self.subscription, self.resource_group, self.workspace)

    def get_experiment_uri_path(self):
        return self.get_workspace_uri_path() + "/experiments/{}".format(self.project)

    def get_history_service_ui(self):
        try:
            return get_history_service_url(
                self._auth, "/subscriptions/{}/resourceGroups/{}/providers/Microsoft.MachineLearningServices"
                            "/workspaces/{}".format(self.subscription, self.resource_group, self.workspace))
        except requests.exceptions.RequestException as response_exception:
            # Cloud project was deleted and user trying to use local project directory
            if response_exception.response.status_code == 404:
                raise ProjectSystemException("Local folder is not linked to a Machine Learning project in Azure")
            else:
                from azureml._base_sdk_common.common import get_http_exception_response_string
                raise ProjectSystemException(get_http_exception_response_string(
                    response_exception.response))

    def get_cloud_execution_service_address(self):
        return self.get_history_service_ui()

    def get_auth(self):
        return self._auth
