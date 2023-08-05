# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Module including Image base class, Asset class, and ImageConfig base class"""

import copy
import json
import os
import requests
import sys
import time
from azureml.core.model import Model
from azureml.exceptions import WebserviceException
from azureml._model_management._constants import MMS_WORKSPACE_API_VERSION
from azureml._model_management._constants import MMS_SYNC_TIMEOUT_SECONDS
from azureml._model_management._constants import DOCKER_IMAGE_TYPE, WEBAPI_IMAGE_FLAVOR
from azureml._model_management._constants import ARCHITECTURE_AMD64
from azureml._model_management._util import get_paginated_results
from azureml._model_management._util import _get_mms_url

try:
    from abc import ABCMeta

    ABC = ABCMeta('ABC', (), {})
except ImportError:
    from abc import ABC
from abc import abstractmethod


class Image(ABC):
    """
    Abstract parent class for AzureML images. Image constructor is used to retrieve a cloud representation of a Image
    object associated with the provided workspace. Will return an instance of a child class corresponding to the
    specific type of the retrieved Image object.

    :param workspace: The workspace object containing the image to retrieve
    :type workspace: azureml.core.workspace.Workspace
    :param name: The name of the image to retrieve. Will return the latest version, if it exists
    :type name: str
    :param id: The specific ID of the image to retrieve
    :type id: str
    :param tags: Will filter based on the provided list, by either 'key' or '[key, value]'.
        Ex. ['key', ['key2', 'key2 value']]
    :type tags: list[str and/or list[str, str]]
    :param properties: Will filter based on the provided list, by either 'key' or '[key, value]'.
        Ex. ['key', ['key2', 'key2 value']]
    :type properties: list[str and/or list[str, str]]
    :param version: When specified with name, will return the specific version of the image
    :type version: str
    """

    _expected_payload_keys = ['createdTime', 'creationState', 'description', 'id',
                              'imageLocation', 'imageType', 'modelIds', 'name', 'kvTags',
                              'properties', 'version']

    def __new__(cls, workspace, name=None, id=None, tags=None, properties=None, version=None):
        """
        Image constructor is used to retrieve a cloud representation of a Image object associated with the
        provided workspace. Will return an instance of a child class corresponding to the specific type of the
        retrieved Image object.

        :param workspace: The workspace object containing the image to retrieve
        :type workspace: azureml.core.workspace.Workspace
        :param name: The name of the image to retrieve. Will return the latest version, if it exists
        :type name: str
        :param id: The specific ID of the image to retrieve
        :type id: str
        :param tags: Will filter based on the provided list, by either 'key' or '[key, value]'.
            Ex. ['key', ['key2', 'key2 value']]
        :type tags: list[str and/or list[str, str]]
        :param properties: Will filter based on the provided list, by either 'key' or '[key, value]'.
            Ex. ['key', ['key2', 'key2 value']]
        :type properties: list[str and/or list[str, str]]
        :param version: When specified with name, will return the specific version of the image
        :type version: str
        :return: An instance of a child of Image corresponding to the specific type of the retrieved Image object
        :rtype: Image
        :raises: WebserviceException
        """
        if workspace:
            get_response_payload = cls._get(workspace, name, id, tags, properties, version)
            if get_response_payload:
                image_type = get_response_payload['imageType']

                # patch image_flavor for back-compat
                image_flavor = ""
                if 'imageFlavor' in get_response_payload:
                    image_flavor = get_response_payload['imageFlavor']
                if image_flavor == "" and image_type == DOCKER_IMAGE_TYPE:
                    image_flavor = WEBAPI_IMAGE_FLAVOR

                for child in Image.__subclasses__():
                    if image_type == child._image_type and image_flavor == child._image_flavor:
                        image = super(Image, cls).__new__(child)
                        image._initialize(workspace, get_response_payload)
                        return image
                raise WebserviceException("This SDK doesn't support images of type {0} [{1}]"
                                          .format(image_type, image_flavor))
            else:
                error_message = 'ImageNotFound: Image with '
                if id:
                    error_message += 'ID {}'.format(id)
                else:
                    error_message += 'name {}'.format(name)
                if tags:
                    error_message += ', tags {}'.format(tags)
                if properties:
                    error_message += ', properties {}'.format(properties)
                if version:
                    error_message += ', version {}'.format(version)
                error_message += ' not found in provided workspace'

                raise WebserviceException(error_message)
        return super(Image, cls).__new__(cls)

    def __init__(self, workspace, name=None, id=None, tags=None, properties=None, version=None):
        """
        Image constructor is used to retrieve a cloud representation of a Image object associated with the
        provided workspace. Will return an instance of a child class corresponding to the specific type of the
        retrieved Image object.

        :param workspace: The workspace object containing the image to retrieve
        :type workspace: azureml.core.workspace.Workspace
        :param name: The name of the image to retrieve. Will return the latest version, if it exists
        :type name: str
        :param id: The specific ID of the image to retrieve
        :type id: str
        :param tags: Will filter based on the provided list, by either 'key' or '[key, value]'.
            Ex. ['key', ['key2', 'key2 value']]
        :type tags: list[str and/or list[str, str]]
        :param properties: Will filter based on the provided list, by either 'key' or '[key, value]'.
            Ex. ['key', ['key2', 'key2 value']]
        :type properties: list[str and/or list[str, str]]
        :param version: When specified with name, will return the specific version of the image
        :type version: str
        :return: An instance of a child of Image corresponding to the specific type of the retrieved Image object
        :rtype: Image
        :raises: WebserviceException
        """
        pass

    def __repr__(self):
        """
        Returns the string representation of the Image object

        :return: String representation of the Image object
        :rtype: str
        """
        return "{}(workspace={}, name={}, id={}, tags={}, properties={}, " \
               "version={})".format(self.__class__.__name__,
                                    self.workspace.__repr__(),
                                    self.name,
                                    self.id,
                                    self.tags,
                                    self.properties,
                                    self.version)

    @abstractmethod
    def _initialize(self, workspace, obj_dict):
        """

        :param workspace:
        :type workspace: Workspace
        :param obj_dict:
        :type obj_dict: dict
        """
        pass

    @staticmethod
    def _get(workspace, name=None, id=None, tags=None, properties=None, version=None):
        """
        Gets the image with the given filtering criteria

        :param workspace:
        :type workspace: azureml.core.workspace.Workspace
        :param name:
        :type name: str
        :param id:
        :type id: str
        :param tags:
        :type tags: dict[str, str]
        :param properties:
        :type properties: dict[str, str]
        :param version:
        :type version: str
        :return: azureml.core.image.Image payload dictionary
        :rtype: dict
        :raises: azureml.exceptions.WebserviceException
        """
        if not name and not id:
            raise WebserviceException('Error, one of id or name must be provided.')

        headers = workspace._auth.get_authentication_header()
        params = {'api-version': MMS_WORKSPACE_API_VERSION, 'orderBy': 'CreatedAtDesc', 'count': 1, 'expand': 'true'}
        base_endpoint = _get_mms_url(workspace)
        mms_endpoint = base_endpoint + '/images'

        if id:
            image_url = mms_endpoint + '/{}'.format(id)
        else:
            image_url = mms_endpoint
            params['name'] = name
        if tags:
            tags_query = ""
            for tag in tags:
                if type(tag) is list:
                    tags_query = tags_query + tag[0] + "=" + tag[1] + ","
                else:
                    tags_query = tags_query + tag + ","
            tags_query = tags_query[:-1]
            params['kvTags'] = tags_query
        if properties:
            properties_query = ""
            for prop in properties:
                if type(prop) is list:
                    properties_query = properties_query + prop[0] + "=" + prop[1] + ","
                else:
                    properties_query = properties_query + prop + ","
            properties_query = properties_query[:-1]
            params['properties'] = properties_query
        if version:
            params['version'] = version

        resp = requests.get(image_url, headers=headers, params=params, timeout=MMS_SYNC_TIMEOUT_SECONDS)

        if resp.status_code == 200:
            content = resp.content
            if isinstance(content, bytes):
                content = content.decode('utf-8')
            image_payload = json.loads(content)
            if id:
                return image_payload
            else:
                paginated_results = get_paginated_results(image_payload, headers)
                if paginated_results:
                    return paginated_results[0]
                else:
                    return None
        elif resp.status_code == 404:
            return None
        else:
            raise WebserviceException('Received bad response from Model Management Service:\n'
                                      'Response Code: {}\n'
                                      'Headers: {}\n'
                                      'Content: {}'.format(resp.status_code, resp.headers, resp.content))

    @staticmethod
    def create(workspace, name, models, image_config):
        """
        Creates an image in the provided workspace.

        :param workspace: The workspace to associate with this image
        :type workspace: workspace: azureml.core.workspace.Workspace
        :param name: The name to associate with this image
        :type name: str
        :param models: A list of Model objects to package with this image. Can be an empty list
        :type models: list[azureml.core.model.Model]
        :param image_config: The image config object to use to configure this image
        :type image_config: azureml.core.image.image.ImageConfig
        :return: The created Image object
        :rtype: azureml.core.image.Image
        :raises: azureml.exceptions.WebserviceException
        """
        model_objs = []
        model_number = 1
        for model in models:
            if type(model) is str:
                try:
                    registered_model = Model(workspace, id=model)
                    model_objs.append(registered_model)
                except WebserviceException as e:
                    if 'ModelNotFound' in e.message:
                        if model.lower().startswith('http'):
                            model_name = '{}.model{}.httpmodel'.format(name[:10], model_number)
                        elif model.lower().startswith('wasb'):
                            model_name = '{}.model{}.wasbmodel'.format(name[:10], model_number)
                        else:
                            model_name = os.path.basename(model.rstrip(os.sep))[:30]
                        model_objs.append(Model.register(workspace, model, model_name, None, None, None))
                    else:
                        raise e

            elif type(model) is Model:
                model_objs.append(model)
            else:
                raise NotImplementedError('Models must either be of type azureml.core.model.Model or a str '
                                          'path to a file or folder.')
            model_number += 1
        model_ids = [model.id for model in model_objs]

        headers = {'Content-Type': 'application/json'}
        headers.update(workspace._auth.get_authentication_header())
        params = {'api-version': MMS_WORKSPACE_API_VERSION}
        base_endpoint = _get_mms_url(workspace)
        image_url = base_endpoint + '/images'

        json_payload = image_config.build_create_payload(workspace, name, model_ids)

        print('Creating image')
        resp = requests.post(image_url, params=params, headers=headers, json=json_payload)
        try:
            resp.raise_for_status()
        except requests.exceptions.HTTPError:
            raise WebserviceException('Received bad response from Model Management Service:\n'
                                      'Response Code: {}\n'
                                      'Headers: {}\n'
                                      'Content: {}'.format(resp.status_code, resp.headers, resp.content))
        if resp.status_code != 202:
            raise WebserviceException('Error occurred creating image:\n'
                                      'Response Code: {}\n'
                                      'Headers: {}\n'
                                      'Content: {}'.format(resp.status_code, resp.headers, resp.content))

        if 'Operation-Location' in resp.headers:
            operation_location = resp.headers['Operation-Location']
        else:
            raise WebserviceException('Missing response header key: Operation-Location')

        create_operation_status_id = operation_location.split('/')[-1]
        operation_url = base_endpoint + '/operations/{}'.format(create_operation_status_id)
        operation_headers = workspace._auth.get_authentication_header()

        operation_resp = requests.get(operation_url, params=params,
                                      headers=operation_headers, timeout=MMS_SYNC_TIMEOUT_SECONDS)
        try:
            operation_resp.raise_for_status()
        except requests.Timeout:
            raise WebserviceException('Error, request to {} timed out.'.format(operation_url))
        except requests.exceptions.HTTPError:
            raise WebserviceException('Received bad response from Model Management Service:\n'
                                      'Response Code: {}\n'
                                      'Headers: {}\n'
                                      'Content: {}'.format(operation_resp.status_code,
                                                           operation_resp.headers,
                                                           operation_resp.content))

        content = operation_resp.content
        if isinstance(content, bytes):
            content = content.decode('utf-8')
        operation_content = json.loads(content)
        if 'resourceLocation' in operation_content:
            image_id = operation_content['resourceLocation'].split('/')[-1]
        else:
            raise WebserviceException('Invalid operation payload, missing resourceLocation:\n'
                                      '{}'.format(operation_content))

        image = Image(workspace, id=image_id)
        image._operation_endpoint = operation_url
        return image

    def wait_for_creation(self, show_output=False):
        """
        Wait for the image to finish creating.

        :param show_output: Boolean option to print more verbose output
        :type show_output: bool
        """
        operation_state, error = self._get_operation_state(MMS_WORKSPACE_API_VERSION)
        current_state = operation_state
        if show_output:
            sys.stdout.write('{}'.format(current_state))
            sys.stdout.flush()
        while operation_state != 'Cancelled' and operation_state != 'Succeeded' and operation_state != 'Failed' \
                and operation_state != 'TimedOut':
            time.sleep(5)
            operation_state, error = self._get_operation_state(MMS_WORKSPACE_API_VERSION)
            if show_output:
                sys.stdout.write('.')
                if operation_state != current_state:
                    sys.stdout.write('\n{}'.format(operation_state))
                    current_state = operation_state
                sys.stdout.flush()
        print('Image creation operation finished for image {}, operation "{}"'.format(self.id, operation_state))
        if operation_state == 'Failed':
            if error and 'statusCode' in error and 'message' in error:
                print('Image creation failed with\n'
                      'StatusCode: {}\n'
                      'Message: {}'.format(error['statusCode'], error['message']))
            else:
                print('Image creation failed, unexpected error response:\n'
                      '{}'.format(error))
        self.update_creation_state()

    def _get_operation_state(self, api_version):
        """

        :param api_version:
        :type api_version: str
        :return:
        :rtype: (str, dict)
        """
        headers = {'Content-Type': 'application/json'}
        headers.update(self._auth.get_authentication_header())
        params = {'api-version': api_version}

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

    def update_creation_state(self):
        """
        Perform an in-place update of the properties of the object based on the current state of the
        corresponding cloud object. Primarily useful for manual polling of creation state.

        :raises: WeberviceException
        """
        headers = {'Content-Type': 'application/json'}
        headers.update(self._auth.get_authentication_header())
        params = {'api-version': MMS_WORKSPACE_API_VERSION}

        resp = requests.get(self._mms_endpoint, headers=headers, params=params, timeout=MMS_SYNC_TIMEOUT_SECONDS)

        if resp.status_code == 200:
            image = Image(self.workspace, id=self.id)
            self.assets = image.assets
            self.creation_state = image.creation_state
            self.description = image.description
            self.driver_program = image.driver_program
            self.image_build_log_uri = image.image_build_log_uri
            self.image_location = image.image_location
            self.image_type = image.image_type
            self.model_ids = image.model_ids
            self.tags = image.tags
            self.properties = image.properties
            self.target_runtime = image.target_runtime
            self.version = image.version
        elif resp.status_code == 404:
            raise WebserviceException('Error: image {} not found:\n'
                                      'Response Code: {}\n'
                                      'Headers: {}\n'
                                      'Content: {}'.format(self.id, resp.status_code, resp.headers, resp.content))
        else:
            raise WebserviceException('Received bad response from Model Management Service:\n'
                                      'Response Code: {}\n'
                                      'Headers: {}\n'
                                      'Content: {}'.format(resp.status_code, resp.headers, resp.content))

    @staticmethod
    def list(workspace, image_name=None, model_name=None, model_id=None, tags=None, properties=None):
        """
        List the Images associated with the corresponding Workspace. Can be filtered with specific parameters.

        :param workspace: The Workspace object to list the Images in.
        :type workspace: azureml.core.workspace.Workspace
        :param image_name: Filter list to only include Images deployed with the specific image name
        :type image_name: str
        :param model_name: Filter list to only include Images deployed with the specific model name
        :type model_name: str
        :param model_id: Filter list to only include Images deployed with the specific model id
        :type model_id: str
        :param tags: Will filter based on the provided list, by either 'key' or '[key, value]'.
            Ex. ['key', ['key2', 'key2 value']]
        :type tags: list[str and/or list[str, str]]
        :param properties: Will filter based on the provided list, by either 'key' or '[key, value]'.
            Ex. ['key', ['key2', 'key2 value']]
        :type properties: list[str and/or list[str, str]]
        :return: A filtered list of Images in the provided Workspace
        :rtype: list[Images]
        :raises: WebserviceException
        """
        headers = workspace._auth.get_authentication_header()
        params = {'api-version': MMS_WORKSPACE_API_VERSION, 'expand': 'true'}
        base_url = _get_mms_url(workspace)
        mms_url = base_url + '/images'

        if image_name:
            params['name'] = image_name
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
            resp = requests.get(mms_url, headers=headers, params=params, timeout=MMS_SYNC_TIMEOUT_SECONDS)
            resp.raise_for_status()
        except requests.Timeout:
            raise WebserviceException('Error, request to Model Management Service timed out to URL:\n'
                                      '{}'.format(mms_url))
        except requests.exceptions.HTTPError:
            raise WebserviceException('Received bad response from Model Management Service:\n'
                                      'Response Code: {}\n'
                                      'Headers: {}\n'
                                      'Content: {}'.format(resp.status_code, resp.headers, resp.content))

        content = resp.content
        if isinstance(content, bytes):
            content = content.decode('utf-8')
        image_payload = json.loads(content)
        paginated_results = get_paginated_results(image_payload, headers)

        return [Image.deserialize(workspace, image_dict) for image_dict in paginated_results]

    def update(self, tags):
        """
        Updates the image

        :param tags: A dictionary of tags to update the image with. Will overwrite any existing tags
        :type tags: dict[str, str]
        :raises: WebserviceException
        """
        headers = {'Content-Type': 'application/json-patch+json'}
        headers.update(self._auth.get_authentication_header())
        params = {'api-version': MMS_WORKSPACE_API_VERSION}

        patch_list = []
        self.tags = tags
        patch_list.append({'op': 'replace', 'path': '/kvTags', 'value': self.tags})

        resp = requests.patch(self._mms_endpoint, headers=headers, params=params, json=patch_list,
                              timeout=MMS_SYNC_TIMEOUT_SECONDS)

        if resp.status_code != 200:
            raise WebserviceException('Received bad response from Model Management Service:\n'
                                      'Response Code: {}\n'
                                      'Headers: {}\n'
                                      'Content: {}'.format(resp.status_code, resp.headers, resp.content))

    def add_tags(self, tags):
        """
        Adds tags to the image

        :param tags: A dictionary of tags to add
        :type tags: dict[str, str]
        :raises: WebserviceException
        """
        headers = {'Content-Type': 'application/json-patch+json'}
        headers.update(self._auth.get_authentication_header())
        params = {'api-version': MMS_WORKSPACE_API_VERSION}

        patch_list = []
        if self.tags is None:
            self.tags = copy.deepcopy(tags)
        else:
            for key in tags:
                if key in self.tags:
                    print("Replacing tag {} -> {} with {} -> {}".format(key, self.tags[key], key, tags[key]))
                self.tags[key] = tags[key]

        patch_list.append({'op': 'replace', 'path': '/kvTags', 'value': self.tags})

        resp = requests.patch(self._mms_endpoint, headers=headers, params=params, json=patch_list,
                              timeout=MMS_SYNC_TIMEOUT_SECONDS)

        if resp.status_code != 200:
            raise WebserviceException('Received bad response from Model Management Service:\n'
                                      'Response Code: {}\n'
                                      'Headers: {}\n'
                                      'Content: {}'.format(resp.status_code, resp.headers, resp.content))

        print('Image tag add operation complete.')

    def remove_tags(self, tags):
        """
        Removes tags from the image

        :param tags: A list of keys corresponding to tags to be removed
        :type tags: list[str]
        :raises: WebserviceException
        """
        headers = {'Content-Type': 'application/json-patch+json'}
        headers.update(self._auth.get_authentication_header())
        params = {'api-version': MMS_WORKSPACE_API_VERSION}

        patch_list = []
        if self.tags is None:
            print('Image has no tags to remove.')
            return
        else:
            if type(tags) is not list:
                tags = [tags]
            for key in tags:
                if key in self.tags:
                    del self.tags[key]
                else:
                    print('Tag with key {} not found.'.format(key))

        patch_list.append({'op': 'replace', 'path': '/kvTags', 'value': self.tags})

        resp = requests.patch(self._mms_endpoint, headers=headers, params=params, json=patch_list,
                              timeout=MMS_SYNC_TIMEOUT_SECONDS)

        if resp.status_code != 200:
            raise WebserviceException('Received bad response from Model Management Service:\n'
                                      'Response Code: {}\n'
                                      'Headers: {}\n'
                                      'Content: {}'.format(resp.status_code, resp.headers, resp.content))

        print('Image tag remove operation complete.')

    def add_properties(self, properties):
        """
        Adds properties to the image

        :param properties: A dictionary of properties to add
        :type properties: dict[str, str]
        :raises: WebserviceException
        """
        headers = {'Content-Type': 'application/json-patch+json'}
        headers.update(self._auth.get_authentication_header())
        params = {'api-version': MMS_WORKSPACE_API_VERSION}

        patch_list = []
        if self.properties is None:
            self.properties = copy.deepcopy(properties)
        else:
            for key in properties:
                if key in self.properties:
                    print("Replacing property {} -> {} with {} -> {}".format(key, self.properties[key],
                                                                             key, properties[key]))
                self.properties[key] = properties[key]

        patch_list.append({'op': 'add', 'path': '/properties', 'value': self.properties})

        resp = requests.patch(self._mms_endpoint, headers=headers, params=params, json=patch_list,
                              timeout=MMS_SYNC_TIMEOUT_SECONDS)

        if resp.status_code != 200:
            raise WebserviceException('Received bad response from Model Management Service:\n'
                                      'Response Code: {}\n'
                                      'Headers: {}\n'
                                      'Content: {}'.format(resp.status_code, resp.headers, resp.content))

        print('Image properties add operation complete.')

    def delete(self):
        """
        Deletes an image from it's corresponding workspace. Will fail if the image has been deployed to a still
        present webservice

        :raises: WebserviceException
        """
        headers = self._auth.get_authentication_header()
        params = {'api-version': MMS_WORKSPACE_API_VERSION}

        resp = requests.delete(self._mms_endpoint, headers=headers, params=params, timeout=MMS_SYNC_TIMEOUT_SECONDS)

        if resp.status_code == 200:
            self.creation_state = 'Deleting'
        else:
            raise WebserviceException('Received bad response from Model Management Service:\n'
                                      'Response Code: {}\n'
                                      'Headers: {}\n'
                                      'Content: {}'.format(resp.status_code, resp.headers, resp.content))

    def serialize(self):
        """
        Convert this Image into a json serialized dictionary.

        :return: The json representation of this Image
        :rtype: dict
        """
        assets = [asset.serialize() for asset in self.assets] if self.assets else None
        created_time = self.created_time.isoformat() if self.created_time else None
        target_runtime = self.target_runtime.serialize() if self.target_runtime else None
        models = [model.serialize() for model in self.models] if self.models else None

        return {'assets': assets, 'createdTime': created_time, 'creationState': self.creation_state,
                'description': self.description, 'driverProgram': self.driver_program, 'id': self.id,
                'imageBuildLogUri': self.image_build_log_uri, 'imageLocation': self.image_location,
                'imageType': self.image_type, 'modelIds': self.model_ids, 'modelDetails': models, 'name': self.name,
                'tags': self.tags, 'properties': self.properties, 'targetRuntime': target_runtime,
                'version': self.version, 'workspaceName': self.workspace.name}

    @classmethod
    def deserialize(cls, workspace, image_payload):
        """
        Convert a json object into a Image object. Will fail if the provided workspace is not the workspace
        the image is registered under.

        :param workspace: The workspace object the Image is registered under
        :type workspace: azureml.core.workspace.Workspace
        :param image_payload: A json object to convert to a Image object
        :type image_payload: dict
        :return: The Image representation of the provided json object
        :rtype: Image
        """
        image_type = image_payload['imageType']

        for child in Image.__subclasses__():
            if image_type == child._image_type:
                return child._deserialize(workspace, image_payload)

    @classmethod
    def _deserialize(cls, workspace, image_payload):
        """

        :param workspace:
        :type workspace: azureml.core.workspace.Workspace
        :param image_payload:
        :type image_payload: dict
        :return:
        :rtype: Image
        """
        cls._validate_get_payload(image_payload)
        image = cls(None)
        image._initialize(workspace, image_payload)
        return image

    @classmethod
    def _validate_get_payload(cls, payload):
        """

        :param payload:
        :type payload: dict
        :return:
        :rtype: None
        """
        for payload_key in cls._expected_payload_keys:
            if payload_key not in payload:
                raise WebserviceException('Invalid image payload, missing {} for image:\n'
                                          '{}'.format(payload_key, payload))

    @staticmethod
    @abstractmethod
    def image_configuration():
        """
        Abstract method for creating an image configuration object
        """
        pass


class Asset(object):
    """
    Asset class to be used for Image class
    """
    _expected_payload_keys = ['id', 'mimeType', 'unpack', 'url']

    def __init__(self, id, mime_type, unpack, url):
        """
        Initializes the Asset object for images

        :param id: The ID corresponding to the image asset
        :type id: str
        :param mime_type: The mime type of the asset
        :type mime_type: str
        :param unpack: Whether the asset needs to be unpacked as a part of image setup
        :type unpack: bool
        :param url: A URL pointer to where the asset is stored
        :type url: str
        """
        self.id = id
        self.mime_type = mime_type
        self.unpack = unpack
        self.url = url

    def serialize(self):
        """
        Convert this Asset into a json serialized dictionary.

        :return: The json representation of this Asset
        :rtype: dict
        """
        return {'id': self.id, 'mimeType': self.mime_type, 'unpack': self.unpack, 'url': self.url}

    @staticmethod
    def deserialize(payload_obj):
        """
        Convert a json object into an Asset object.

        :param payload_obj: A json object to convert to an Asset object
        :type payload_obj: dict
        :return: The Asset representation of the provided json object
        :rtype: Asset
        :raises: WebserviceException
        """
        for payload_key in Asset._expected_payload_keys:
            if payload_key not in payload_obj:
                raise WebserviceException('Invalid image payload, missing {} for asset:\n'
                                          '{}'.format(payload_key, payload_obj))

        return Asset(payload_obj['id'], payload_obj['mimeType'], payload_obj['unpack'], payload_obj['url'])


class ImageConfig(ABC):
    """
    Abstract class for image configuration objects
    """
    @abstractmethod
    def build_create_payload(self, workspace, name, model_ids):
        """
        Abstract method for building the creation payload associated with this configuration object

        :param workspace: The workspace associated with the image
        :type workspace: azureml.core.workspace.Workspace
        :param name: The name of the image
        :type name: str
        :param model_ids: A list of model IDs to be packaged with the image
        :type model_ids: list[str]
        :return: The creation payload to use for Image creation
        :rtype: dict
        """
        pass

    @abstractmethod
    def validate_configuration(self):
        """
        Checks that the specified configuration values are valid. Will raise a WebserviceException if validation
        fails.

        :raises: WebserviceException
        """
        pass


class TargetRuntime(object):
    """
    Target runtime object containing properties and the runtime type.
    """
    _expected_payload_keys = ['properties', 'runtimeType']

    def __init__(self, properties, runtime_type, targetArchitecture):
        """
        Initializes the TargetRuntime object

        :param properties: Dictionary of properties associated with the target runtime
        :type properties: dict[str, str]
        :param runtime_type: String representation of the runtime type
        :type runtime_type: str
        """
        self.properties = properties
        self.runtime_type = runtime_type
        self.targetArchitecture = targetArchitecture

    def serialize(self):
        """
        Convert this TargetRuntime into a json serialized dictionary.

        :return: The json representation of this TargetRuntime
        :rtype: dict
        """
        return {'properties': self.properties,
                'runtimeType': self.runtime_type,
                'targetArchitecture': self.targetArchitecture}

    @staticmethod
    def deserialize(payload_obj):
        """
        Convert a json object into a TargetRuntime object.

        :param payload_obj: A json object to convert to a TargetRuntime object
        :type payload_obj: dict
        :return: The TargetRuntime representation of the provided json object
        :rtype: TargetRuntime
        :raises: WebserviceException
        """
        for payload_key in TargetRuntime._expected_payload_keys:
            if payload_key not in payload_obj:
                raise WebserviceException('Invalid image payload, missing {} for targetRuntime:\n'
                                          '{}'.format(payload_key, payload_obj))

        targetArchitecture = ARCHITECTURE_AMD64
        if 'targetArchitecture' in payload_obj:
            targetArchitecture = payload_obj['targetArchitecture']

        return TargetRuntime(payload_obj['properties'], payload_obj['runtimeType'], targetArchitecture)
