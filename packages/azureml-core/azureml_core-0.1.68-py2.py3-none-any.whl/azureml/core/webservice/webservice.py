# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Module for managing the abstract parent class for Webservices in Azure ML"""

try:
    from abc import ABCMeta

    ABC = ABCMeta('ABC', (), {})
except ImportError:
    from abc import ABC
from abc import abstractmethod
import copy
import json
import os
import requests
import sys
import time
from azureml.core.model import Model
from azureml.core.image import Image
from azureml.exceptions import WebserviceException
from azureml._model_management._constants import MMS_SYNC_TIMEOUT_SECONDS
from azureml._model_management._constants import MMS_WORKSPACE_API_VERSION
from azureml._model_management._constants import CLOUD_DEPLOYABLE_IMAGE_FLAVORS
from azureml._model_management._util import get_paginated_results
from azureml._model_management._util import _get_mms_url


class Webservice(ABC):
    """
    Class for AzureML Webservices. Webservice constructor is used to retrieve a cloud representation of a Webservice
    object associated with the provided workspace. Will return an instance of a child class corresponding to the
    specific type of the retrieved Webservice object.

    :param workspace: The workspace object containing the Webservice object to retrieve
    :type workspace: azureml.core.workspace.Workspace
    :param name: The name of the of the Webservice object to retrieve
    :type name: str
    """
    _webservice_type = None

    def __new__(cls, workspace, name):
        """
        Webservice constructor is used to retrieve a cloud representation of a Webservice object associated with the
        provided workspace. Will return an instance of a child class corresponding to the specific type of the
        retrieved Webservice object.

        :param workspace: The workspace object containing the Webservice object to retrieve
        :type workspace: azureml.core.workspace.Workspace
        :param name: The name of the of the Webservice object to retrieve
        :type name: str
        :return: An instance of a child of Webservice corresponding to the specific type of the retrieved
            Webservice object
        :rtype: Webservice
        :raises: WebserviceException
        """
        if workspace and name:
            service_payload = cls._get(workspace, name)
            if service_payload:
                service_type = service_payload['computeType']
                for child in Webservice.__subclasses__():
                    if service_type == child._webservice_type:
                        service = super(Webservice, cls).__new__(child)
                        service._initialize(workspace, service_payload)
                        return service
            else:
                raise WebserviceException('WebserviceNotFound: Webservice with name {} not found in provided '
                                          'workspace'.format(name))
        else:
            return super(Webservice, cls).__new__(cls)

    def __init__(self, workspace, name):
        """
        Webservice constructor is used to retrieve a cloud representation of a Webservice object associated with the
        provided workspace. Will return an instance of a child class corresponding to the specific type of the
        retrieved Webservice object.

        :param workspace: The workspace object containing the Webservice object to retrieve
        :type workspace: azureml.core.workspace.Workspace
        :param name: The name of the of the Webservice object to retrieve
        :type name: str
        :return: An instance of a child of Webservice corresponding to the specific type of the retrieved
            Webservice object
        :rtype: Webservice
        :raises: WebserviceException
        """
        pass

    @abstractmethod
    def _initialize(self, name, description, tags, properties, state, created_time, updated_time, error,
                    compute_type, workspace, mms_endpoint, operation_endpoint, auth):
        """

        :param name:
        :type name: str
        :param description:
        :type description: str
        :param tags:
        :type tags: dict[str, str]
        :param properties:
        :type properties: dict[str, str]
        :param state:
        :type state: str
        :param created_time:
        :type created_time: datetime.datetime
        :param updated_time:
        :type updated_time: datetime.datetime
        :param error:
        :type error: dict
        :param compute_type:
        :type compute_type: str
        :param workspace:
        :type workspace: azureml.core.workspace.Workspace
        :param mms_endpoint:
        :type mms_endpoint: str
        :param operation_endpoint:
        :type operation_endpoint: str
        :param auth:
        :type auth: azureml.core.authentication.AbstractAuthentication
        :return:
        :rtype: None
        """
        self.name = name
        self.description = description
        self.tags = tags
        self.properties = properties
        self.state = state
        self.created_time = created_time
        self.updated_time = updated_time
        self.error = error
        self.compute_type = compute_type
        self.workspace = workspace
        self._mms_endpoint = mms_endpoint
        self._operation_endpoint = operation_endpoint
        self._auth = auth

    @staticmethod
    def _get(workspace, name=None):
        """

        :param workspace:
        :type workspace: azureml.core.workspace.Workspace
        :param name:
        :type name: str
        :return:
        :rtype: dict
        """
        if not name:
            raise WebserviceException('Name must be provided')

        base_url = _get_mms_url(workspace)
        mms_url = base_url + '/services'

        headers = {'Content-Type': 'application/json'}
        headers.update(workspace._auth.get_authentication_header())
        params = {'api-version': MMS_WORKSPACE_API_VERSION, 'expand': 'true'}

        service_url = mms_url + '/{}'.format(name)

        resp = requests.get(service_url, headers=headers, params=params)
        if resp.status_code == 200:
            content = resp.content
            if isinstance(content, bytes):
                content = content.decode('utf-8')
            service_payload = json.loads(content)
            return service_payload
        elif resp.status_code == 404:
            return None
        else:
            raise WebserviceException('Received bad response from Model Management Service:\n'
                                      'Response Code: {}\n'
                                      'Headers: {}\n'
                                      'Content: {}'.format(resp.status_code, resp.headers, resp.content))

    @staticmethod
    def deploy(workspace, name, model_paths, image_config, deployment_config=None, deployment_target=None):
        """
        Deploy a Webservice from zero or more model files. This will register any models files provided and create an
        image in the process, all associated with the specified Workspace.

        :param workspace: A Workspace object to associate the Webservice with
        :type workspace: azureml.core.workspace.Workspace
        :param name: The name to give the deployed workspace. Must be unique to the workspace.
        :type name: str
        :param model_paths: A list of on disk paths to model files or folder. Can be an empty list.
        :type model_paths: list[str]
        :param image_config: An ImageConfig object used to determine required Image properties.
        :type image_config: azureml.core.image.image.ImageConfig
        :param deployment_config: A WebserviceDeploymentConfiguration used to configure the webservice. If one is not
            provided, an empty configuration object will be used based on the desired target.
        :type deployment_config: WebserviceDeploymentConfiguration
        :param deployment_target: A ComputeTarget to deploy the Webservice to. As ACI has no associated ComputeTarget,
            leave this parameter as None to deploy to ACI.
        :type deployment_target: azureml.core.compute.ComputeTarget
        :return: A Webservice object corresponding to the deployed webservice
        :rtype: Webservice
        :raises: WebserviceException
        """
        try:
            Webservice(workspace, name=name)
            raise WebserviceException('Error, there is already a service with name {} found in '
                                      'workspace {}'.format(name, workspace._workspace_name))
        except WebserviceException as e:
            if 'WebserviceNotFound' in e.message:
                pass
            else:
                raise e
        models = []
        for model_path in model_paths:
            model_name = os.path.basename(model_path.rstrip(os.sep))[:30]
            models.append(Model.register(workspace, model_path, model_name))
        return Webservice.deploy_from_model(workspace, name, models, image_config, deployment_config,
                                            deployment_target)

    @staticmethod
    def deploy_from_model(workspace, name, models, image_config, deployment_config=None, deployment_target=None):
        """
        Deploy a Webservice from zero or more model objects. This will create an image in the process, associated with
        the specified Workspace.

        :param workspace: A Workspace object to associate the Webservice with
        :type workspace: azureml.core.workspace.Workspace
        :param name: The name to give the deployed workspace. Must be unique to the workspace.
        :type name: str
        :param models: A list of model objects. Can be an empty list.
        :type models: list[str]
        :param image_config: An ImageConfig object used to determine required Image properties.
        :type image_config: azureml.core.image.image.ImageConfig
        :param deployment_config: A WebserviceDeploymentConfiguration used to configure the webservice. If one is not
            provided, an empty configuration object will be used based on the desired target.
        :type deployment_config: WebserviceDeploymentConfiguration
        :param deployment_target: A ComputeTarget to deploy the Webservice to. As ACI has no associated ComputeTarget,
            leave this parameter as None to deploy to ACI.
        :type deployment_target: azureml.core.compute.ComputeTarget
        :return: A Webservice object corresponding to the deployed webservice
        :rtype: Webservice
        :raises: WebserviceException
        """
        try:
            Webservice(workspace, name=name)
            raise WebserviceException('Error, there is already a service with name {} found in '
                                      'workspace {}'.format(name, workspace._workspace_name))
        except WebserviceException as e:
            if 'WebserviceNotFound' in e.message:
                pass
            else:
                raise e

        image = Image.create(workspace, name, models, image_config)
        image.wait_for_creation()
        if image.creation_state != 'Succeeded':
            raise WebserviceException('Error occurred creating image {} for service.'.format(image.id))
        return Webservice.deploy_from_image(workspace, name, image, deployment_config, deployment_target)

    @staticmethod
    def deploy_from_image(workspace, name, image, deployment_config=None, deployment_target=None):
        """
        Deploy a Webservice from an Image object.

        :param workspace: A Workspace object to associate the Webservice with
        :type workspace: azureml.core.workspace.Workspace
        :param name: The name to give the deployed workspace. Must be unique to the workspace.
        :type name: str
        :param image: An Image object to deploy.
        :type image: azureml.core.image.image.Image
        :param deployment_config: A WebserviceDeploymentConfiguration used to configure the webservice. If one is not
            provided, an empty configuration object will be used based on the desired target.
        :type deployment_config: WebserviceDeploymentConfiguration
        :param deployment_target: A ComputeTarget to deploy the Webservice to. As ACI has no associated ComputeTarget,
            leave this parameter as None to deploy to ACI.
        :type deployment_target: azureml.core.compute.ComputeTarget
        :return: A Webservice object corresponding to the deployed webservice
        :rtype: Webservice
        :raises: WebserviceException
        """
        if deployment_target is None:
            if deployment_config is None:
                for child in Webservice.__subclasses__():  # This is a hack to avoid recursive imports
                    if child._webservice_type == 'ACI':
                        return child._deploy(workspace, name, image, deployment_config)
            return deployment_config._webservice_type._deploy(workspace, name, image, deployment_config)

        else:
            if deployment_config is None:
                for child in Webservice.__subclasses__():  # This is a hack to avoid recursive imports
                    if child._webservice_type == 'AKS':
                        return child._deploy(workspace, name, image, deployment_config, deployment_target)

        return deployment_config._webservice_type._deploy(workspace, name, image, deployment_config, deployment_target)

    @staticmethod
    @abstractmethod
    def _deploy(workspace, name, image, deployment_config, deployment_target):
        """

        :param workspace:
        :type workspace: azureml.core.workspace.Workspace
        :param name:
        :type name: str
        :param image:
        :type image: azureml.core.image.image.Image
        :param deployment_config:
        :type deployment_config: WebserviceDeploymentConfiguration
        :param deployment_target:
        :type deployment_target: azureml.core.compute.ComputeTarget
        :return:
        :rtype: Webservice
        """
        pass

    @staticmethod
    def _deploy_webservice(workspace, name, webservice_payload, webservice_class):
        """

        :param workspace:
        :type workspace: azureml.core.workspace.Workspace
        :param name:
        :type name: str
        :param webservice_payload:
        :type webservice_payload: dict
        :param webservice_class:
        :type webservice_class: type[Webservice]
        :return:
        :rtype: Webservice
        """
        headers = {'Content-Type': 'application/json'}
        headers.update(workspace._auth.get_authentication_header())
        params = {'api-version': MMS_WORKSPACE_API_VERSION}
        base_url = _get_mms_url(workspace)
        mms_endpoint = base_url + '/services'

        print('Creating service')
        try:
            resp = requests.post(mms_endpoint, params=params, headers=headers, json=webservice_payload)
            resp.raise_for_status()
        except requests.exceptions.HTTPError:
            raise WebserviceException('Received bad response from Model Management Service:\n'
                                      'Response Code: {}\n'
                                      'Headers: {}\n'
                                      'Content: {}'.format(resp.status_code, resp.headers, resp.content))
        if resp.status_code != 202:
            raise WebserviceException('Error occurred creating service:\n'
                                      'Response Code: {}\n'
                                      'Headers: {}\n'
                                      'Content: {}'.format(resp.status_code, resp.headers, resp.content))

        if 'Operation-Location' in resp.headers:
            operation_location = resp.headers['Operation-Location']
        else:
            raise WebserviceException('Missing response header key: Operation-Location')
        create_operation_status_id = operation_location.split('/')[-1]
        operation_url = base_url + '/operations/{}'.format(create_operation_status_id)

        service = webservice_class(workspace, name=name)
        service._operation_endpoint = operation_url
        return service

    @abstractmethod
    def wait_for_deployment(self, show_output=False):
        """
        Automatically poll on the running Webservice deployment.

        :param show_output: Option to print more verbose output
        :type show_output: bool
        :raises: WebserviceException
        """
        pass

    def _wait_for_deployment(self, show_output):
        """

        :param show_output:
        :type show_output: bool
        :return:
        :rtype: (str, str)
        """
        if not self._operation_endpoint:
            raise WebserviceException('No operation endpoint')
        state, error = self._get_operation_state()
        current_state = state
        if show_output:
            sys.stdout.write('{}'.format(current_state))
            sys.stdout.flush()
        while state != 'Succeeded' and state != 'Failed' and state != 'Canceled' and state != 'TimedOut':
            time.sleep(5)
            state, error = self._get_operation_state()
            if show_output:
                sys.stdout.write('.')
                if state != current_state:
                    sys.stdout.write('\n{}'.format(state))
                    current_state = state
                sys.stdout.flush()
        return state, error

    def _get_operation_state(self):
        """

        :return:
        :rtype: str, str
        """
        headers = self._auth.get_authentication_header()
        params = {'api-version': MMS_WORKSPACE_API_VERSION}

        resp = requests.get(self._operation_endpoint, headers=headers, params=params, timeout=MMS_SYNC_TIMEOUT_SECONDS)
        try:
            resp.raise_for_status()
        except requests.exceptions.HTTPError:
            raise WebserviceException('Received bad response from Resource Provider:\n'
                                      'Response Code: {}\n'
                                      'Headers: {}\n'
                                      'Content: {}'.format(resp.status_code, resp.headers, resp.content))
        content = resp.content
        if isinstance(content, bytes):
            content = content.decode('utf-8')
        content = json.loads(content)
        state = content['state']
        error = content['error'] if 'error' in content else None
        return state, error

    @abstractmethod
    def update_deployment_state(self):
        """
        Perform an in-place update of the properties of the object based on the current state of the
        corresponding cloud object. Primarily useful for manual polling of deployment state.
        """
        pass

    @staticmethod
    def list(workspace, compute_type=None, image_name=None, image_id=None, model_name=None, model_id=None, tags=None,
             properties=None):
        """
        List the Webservices associated with the corresponding Workspace. Can be filtered with specific parameters.

        :param workspace: The Workspace object to list the Webservices in.
        :type workspace: azureml.core.workspace.Workspace
        :param compute_type: Filter to list only specific Webservice types. Options are 'ACI', 'AKS'.
        :type compute_type: str
        :param image_name: Filter list to only include Webservices deployed with the specific image name
        :type image_name: str
        :param image_id: Filter list to only include Webservices deployed with the specific image id
        :type image_id: str
        :param model_name: Filter list to only include Webservices deployed with the specific model name
        :type model_name: str
        :param model_id: Filter list to only include Webservices deployed with the specific model id
        :type model_id: str
        :param tags: Will filter based on the provided list, by either 'key' or '[key, value]'.
            Ex. ['key', ['key2', 'key2 value']]
        :type tags: list[str and/or list[str, str]]
        :param properties: Will filter based on the provided list, by either 'key' or '[key, value]'.
            Ex. ['key', ['key2', 'key2 value']]
        :type properties: list[str and/or list[str, str]]
        :return: A filtered list of Webservices in the provided Workspace
        :rtype: list[Webservice]
        :raises: WebserviceException
        """
        webservices = []
        headers = {'Content-Type': 'application/json'}
        headers.update(workspace._auth.get_authentication_header())
        params = {'api-version': MMS_WORKSPACE_API_VERSION, 'expand': 'true'}

        base_url = _get_mms_url(workspace)
        mms_workspace_url = base_url + '/services'

        if compute_type:
            if compute_type.upper() != 'ACI' and compute_type.upper() != 'AKS':
                raise WebserviceException('Invalid compute type "{}". Valid options are "ACI", '
                                          '"AKS" '.format(compute_type))
            params['computeType'] = compute_type
        if image_name:
            params['imageName'] = image_name
        if image_id:
            params['imageId'] = image_id
        if model_name:
            params['modelName'] = model_name
        if model_id:
            params['modelId'] = model_id
        if tags:
            tags_query = ""
            for tag in tags:
                if type(tag) is list:
                    tags_query = tags_query + tag[0] + "=" + tag[1] + ","
                else:
                    tags_query = tags_query + tag + ","
            tags_query = tags_query[:-1]
            params['tags'] = tags_query
        if properties:
            properties_query = ""
            for prop in properties:
                if type(prop) is list:
                    properties_query = properties_query + prop[0] + "=" + prop[1] + ","
                else:
                    properties_query = properties_query + prop + ","
            properties_query = properties_query[:-1]
            params['properties'] = properties_query

        try:
            resp = requests.get(mms_workspace_url, headers=headers, params=params, timeout=MMS_SYNC_TIMEOUT_SECONDS)
            resp.raise_for_status()
        except requests.Timeout:
            raise WebserviceException('Error, request to MMS timed out to URL: {}'.format(mms_workspace_url))
        except requests.exceptions.HTTPError:
            raise WebserviceException('Received bad response from Model Management Service:\n'
                                      'Response Code: {}\n'
                                      'Headers: {}\n'
                                      'Content: {}'.format(resp.status_code, resp.headers, resp.content))

        content = resp.content
        if isinstance(content, bytes):
            content = content.decode('utf-8')
        services_payload = json.loads(content)
        paginated_results = get_paginated_results(services_payload, headers)
        for service_dict in paginated_results:
            service_type = service_dict['computeType']
            service_obj = None
            for child in Webservice.__subclasses__():
                if service_type == child._webservice_type:
                    service_obj = child.deserialize(workspace, service_dict)
                    break
            if service_obj:
                webservices.append(service_obj)
        return webservices

    def _add_tags(self, tags):
        """

        :param tags:
        :type tags: dict[str, str]
        :return:
        :rtype: dict[str, str]
        """
        updated_tags = self.tags
        if updated_tags is None:
            return copy.deepcopy(tags)
        else:
            for key in tags:
                if key in updated_tags:
                    print("Replacing tag {} -> {} with {} -> {}".format(key, updated_tags[key], key, tags[key]))
                updated_tags[key] = tags[key]

        return updated_tags

    def _remove_tags(self, tags):
        """

        :param tags:
        :type tags: list[str]
        :return:
        :rtype: list[str]
        """
        updated_tags = self.tags
        if updated_tags is None:
            print('Model has no tags to remove.')
            return updated_tags
        else:
            if type(tags) is not list:
                tags = [tags]
            for key in tags:
                if key in updated_tags:
                    del updated_tags[key]
                else:
                    print('Tag with key {} not found.'.format(key))

        return updated_tags

    def _add_properties(self, properties):
        """

        :param properties:
        :type properties: dict[str, str]
        :return:
        :rtype: dict[str, str]
        """
        updated_properties = self.properties
        if updated_properties is None:
            return copy.deepcopy(properties)
        else:
            for key in properties:
                if key in updated_properties:
                    print("Replacing tag {} -> {} with {} -> {}".format(key, updated_properties[key],
                                                                        key, properties[key]))
                updated_properties[key] = properties[key]

        return updated_properties

    def get_logs(self, num_lines=5000):
        """
        Retrieve logs for this Webservice.

        :param num_lines: The maximum number of log lines to retrieve
        :type num_lines: int
        :return: The logs for this Webservice
        :rtype: str
        :raises: WebserviceException
        """
        headers = {'Content-Type': 'application/json'}
        headers.update(self.workspace._auth.get_authentication_header())
        params = {'api-version': MMS_WORKSPACE_API_VERSION, 'tail': num_lines}
        service_logs_url = self._mms_endpoint + '/logs'

        resp = requests.get(service_logs_url, headers=headers, params=params)
        if resp.status_code == 200:
            content = resp.content
            if isinstance(content, bytes):
                content = content.decode('utf-8')
            service_payload = json.loads(content)
            if 'content' not in service_payload:
                raise WebserviceException('Invalid response, missing "content":\n'
                                          '{}'.format(service_payload))
            else:
                return service_payload['content']
        else:
            raise WebserviceException('Received bad response from Model Management Service:\n'
                                      'Response Code: {}\n'
                                      'Headers: {}\n'
                                      'Content: {}'.format(resp.status_code, resp.headers, resp.content))

    @abstractmethod
    def run(self, input):
        """
        Call this Webservice with the provided input

        :param input: The input to call the Webservice with
        :type input: varies
        :return: The result of calling the Webservice
        :rtype: dict
        :raises: WebserviceException
        """
        pass

    def get_keys(self):
        """
        Retrieve auth keys for this Webservice

        :return: The auth keys for this Webservice
        :rtype: (str, str)
        :raises: WebserviceException
        """
        headers = self._auth.get_authentication_header()
        params = {'api-version': MMS_WORKSPACE_API_VERSION}
        list_keys_url = self._mms_endpoint + '/listkeys'

        try:
            resp = requests.post(list_keys_url, params=params, headers=headers)
            resp.raise_for_status()
        except requests.exceptions.HTTPError:
            raise WebserviceException('Received bad response from Model Management Service:\n'
                                      'Response Code: {}\n'
                                      'Headers: {}\n'
                                      'Content: {}'.format(resp.status_code, resp.headers, resp.content))

        content = resp.content
        if isinstance(content, bytes):
            content = content.decode('utf-8')
        keys_content = json.loads(content)
        if 'primaryKey' not in keys_content:
            raise WebserviceException('Invalid response key: primaryKey')
        if 'secondaryKey' not in keys_content:
            raise WebserviceException('Invalid response key: secondaryKey')
        primary_key = keys_content['primaryKey']
        secondary_key = keys_content['secondaryKey']

        return primary_key, secondary_key

    def regen_key(self, key):
        """
        Regenerate one of the Webservice's keys. Must specify either 'Primary' or 'Secondary' key.

        :param key: Which key to regenerate. Options are 'Primary' or 'Secondary'
        :type key: str
        :raises: WebserviceException
        """
        headers = {'Content-Type': 'application/json'}
        headers.update(self._auth.get_authentication_header())
        params = {'api-version': MMS_WORKSPACE_API_VERSION}

        if not key:
            raise WebserviceException('Error, must specify which key with be regenerated: Primary, Secondary')
        key = key.capitalize()
        if key != 'Primary' and key != 'Secondary':
            raise WebserviceException('Error, invalid value provided for key: {}.\n'
                                      'Valid options are: Primary, Secondary'.format(key))
        keys_url = self._mms_endpoint + '/regenerateKeys'
        body = {'keyType': key}
        try:
            resp = requests.post(keys_url, params=params, headers=headers, json=body)
            resp.raise_for_status()
        except requests.ConnectionError:
            raise WebserviceException('Error connecting to {}.'.format(keys_url))
        except requests.exceptions.HTTPError:
            raise WebserviceException('Received bad response from Model Management Service:\n'
                                      'Response Code: {}\n'
                                      'Headers: {}\n'
                                      'Content: {}'.format(resp.status_code, resp.headers, resp.content))

        if 'Operation-Location' in resp.headers:
            operation_location = resp.headers['Operation-Location']
        else:
            raise WebserviceException('Missing operation location from response header, unable to determine status.')
        create_operation_status_id = operation_location.split('/')[-1]
        operation_endpoint = _get_mms_url(self.workspace) + '/operations/{}'.format(create_operation_status_id)
        operation_state = 'Running'
        while operation_state != 'Cancelled' and operation_state != 'Succeeded' and operation_state != 'Failed' \
                and operation_state != 'TimedOut':
            try:
                operation_resp = requests.get(operation_endpoint, params=params, headers=headers,
                                              timeout=MMS_SYNC_TIMEOUT_SECONDS)
                operation_resp.raise_for_status()
            except requests.ConnectionError:
                raise WebserviceException('Error connecting to {}.'.format(operation_endpoint))
            except requests.Timeout:
                raise WebserviceException('Error, request to {} timed out.'.format(operation_endpoint))
            except requests.exceptions.HTTPError:
                raise WebserviceException('Received bad response from Model Management Service:\n'
                                          'Response Code: {}\n'
                                          'Headers: {}\n'
                                          'Content: {}'.format(operation_resp.status_code, operation_resp.headers,
                                                               operation_resp.content))
            content = operation_resp.content
            if isinstance(content, bytes):
                content = content.decode('utf-8')
            content = json.loads(content)
            if 'state' in content:
                operation_state = content['state']
            else:
                raise WebserviceException('Missing state from operation response, unable to determine status')
            error = content['error'] if 'error' in content else None
        if operation_state != 'Succeeded':
            raise WebserviceException('Error, key regeneration operation "{}" with message '
                                      '"{}"'.format(operation_state, error))

    @abstractmethod
    def update(self, *args):
        """
        Update the Webservice. Possible options to update vary based on Webservice type

        :param args: Values to update
        :type args: varies
        :raises: WebserviceException
        """
        pass

    def delete(self):
        """
        Delete this Webservice from its associated workspace

        :raises: WebserviceException
        """
        headers = self._auth.get_authentication_header()
        params = {'api-version': MMS_WORKSPACE_API_VERSION}

        resp = requests.delete(self._mms_endpoint, headers=headers, params=params, timeout=MMS_SYNC_TIMEOUT_SECONDS)

        if resp.status_code == 200:
            self.state = 'Deleting'
        elif resp.status_code == 204:
            print('No service with name {} found to delete.'.format(self.name))
        else:
            raise WebserviceException('Received bad response from Model Management Service:\n'
                                      'Response Code: {}\n'
                                      'Headers: {}\n'
                                      'Content: {}'.format(resp.status_code, resp.headers, resp.content))

    @abstractmethod
    def serialize(self):
        """
        Convert this Webservice into a json serialized dictionary.

        :return: The json representation of this Webservice
        :rtype: dict
        """
        created_time = self.created_time.isoformat() if self.created_time else None
        updated_time = self.updated_time.isoformat() if self.updated_time else None
        return {'name': self.name, 'description': self.description, 'tags': self.tags,
                'properties': self.properties, 'state': self.state, 'createdTime': created_time,
                'updatedTime': updated_time, 'error': self.error, 'computeType': self.compute_type,
                'workspaceName': self.workspace.name}

    @staticmethod
    @abstractmethod
    def deserialize(workspace, webservice_payload):
        """
        Convert a json object into a Webservice object. Will fail if the provided workspace is not the workspace the
        Webservice is registered under.

        :param workspace: The workspace object the Webservice is registered under
        :type workspace: azureml.core.workspace.Workspace
        :param webservice_payload: A json object to convert to a Webservice object
        :type webservice_payload: dict
        :return: The Webservice representation of the provided json object
        :rtype: Webservice
        """
        pass

    @staticmethod
    @abstractmethod
    def _validate_get_payload(payload):
        """

        :param payload:
        :type payload: dict
        :return:
        :rtype:
        """
        pass


class WebserviceDeploymentConfiguration(ABC):
    """
    Parent class for all Webservice deployment configuration objects. These objects will be used to define the
    configuration parameters for deploying a Webservice on a specific target.
    """

    def __init__(self, type):
        """
        Initialize the configuration object

        :param type: The type of Webservice associated with this object
        :type type: class[Webservice]
        """
        self._webservice_type = type

    @abstractmethod
    def validate_configuration(self):
        """
        Checks that the specified configuration values are valid. Will raise a WebserviceException if validation
        fails.

        :raises: WebserviceException
        """
        pass

    @classmethod
    def validate_image(cls, image):
        """
        Checks that the image that is being deployed to the webservice is valid.
        Will raise a WebserviceException if validation fails.

        :param image: The image that will be deployed to the webservice.
        :type image: Image
        :raises: WebserviceException
        """
        if image is None:
            raise ValueError("Image is None")
        if image.creation_state != 'Succeeded':
            raise WebserviceException('Unable to create service with image {} in non "Succeeded" '
                                      'creation state.'.format(image.id))
        if image.image_flavor not in CLOUD_DEPLOYABLE_IMAGE_FLAVORS:
            raise ValueError('Deployment of {} images is not supported'.format(image.image_flavor))
