# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Module including ContainerImage class and ContainerImageConfig class"""

import json
import requests
import os
import uuid

from .image import Image, ImageConfig, Asset, TargetRuntime
from dateutil.parser import parse
from azureml.core.model import Model
from azureml.exceptions import WebserviceException

from azureml._model_management._constants import SUPPORTED_RUNTIMES
from azureml._model_management._constants import UNDOCUMENTED_RUNTIMES
from azureml._model_management._constants import WORKSPACE_RP_API_VERSION
from azureml._model_management._constants import DOCKER_IMAGE_TYPE, WEBAPI_IMAGE_FLAVOR
from azureml._model_management._constants import ARCHITECTURE_AMD64
from azureml._model_management._util import add_sdk_to_requirements
from azureml._model_management._util import upload_dependency
from azureml._model_management._util import wrap_execution_script
from azureml._model_management._util import _get_mms_url
from azureml._model_management._util import get_docker_client
from azureml._model_management._util import pull_docker_image
from azureml._model_management._util import start_docker_container
from azureml._model_management._util import get_docker_port
from azureml._model_management._util import container_health_check
from azureml._model_management._util import container_scoring_call
from azureml._model_management._util import cleanup_container
from azureml._model_management._util import validate_path_exists_or_throw


class ContainerImage(Image):
    """
    Class for container images. Currently only for Docker
    """

    _image_type = DOCKER_IMAGE_TYPE
    _image_flavor = WEBAPI_IMAGE_FLAVOR

    _expected_payload_keys = ['assets', 'createdTime', 'creationState', 'description', 'driverProgram', 'id',
                              'imageLocation', 'imageType', 'modelIds', 'name', 'kvTags', 'properties',
                              'targetRuntime', 'version']

    _log_aml_debug = True

    def _initialize(self, workspace, obj_dict):
        """
        Initializes the ContainerImage object

        :param workspace:
        :type workspace: azureml.core.workspace.Workspace
        :param obj_dict:
        :type obj_dict: dict
        :return:
        :rtype: None
        :raises: None
        """
        self.assets = None
        self.created_time = None
        self.creation_state = None
        self.description = None
        self.driver_program = None
        self.id = None
        self.image_build_log_uri = None
        self.image_location = None
        self.image_type = None
        self.image_flavor = None
        self.model_ids = None
        self.name = None
        self.tags = None
        self.properties = None
        self.target_runtime = None
        self.version = None
        self.workspace = None
        self.models = None
        self._operation_endpoint = None
        self._mms_endpoint = None
        self._auth = None

        self._validate_get_payload(obj_dict)
        assets = [Asset.deserialize(asset_payload) for asset_payload in obj_dict['assets']]
        created_time = parse(obj_dict['createdTime'])
        target_runtime = TargetRuntime.deserialize(obj_dict['targetRuntime'])
        image_build_log_uri = obj_dict['imageBuildLogUri'] if 'imageBuildLogUri' in obj_dict else None
        image_id = obj_dict['id']
        models = []
        if 'modelDetails' in obj_dict:
            models = [Model.deserialize(workspace, model_payload) for model_payload in obj_dict['modelDetails']]

        # for back-compat. 298627 tracks removing this code once API ships to all DCs
        # https://msdata.visualstudio.com/DefaultCollection/Vienna/_workitems/edit/298627
        self.image_flavor = ContainerImage._image_flavor
        if 'imageFlavor' in obj_dict:
            self.image_flavor = obj_dict['imageFlavor']

        self.assets = assets
        self.created_time = created_time
        self.creation_state = obj_dict['creationState']
        self.description = obj_dict['description']
        self.driver_program = obj_dict['driverProgram']
        self.id = image_id
        self.image_build_log_uri = image_build_log_uri
        self.image_location = obj_dict['imageLocation']
        self.image_type = obj_dict['imageType']
        self.model_ids = obj_dict['modelIds']
        self.name = obj_dict['name']
        self.tags = obj_dict['kvTags']
        self.properties = obj_dict['properties']
        self.target_runtime = target_runtime
        self.version = obj_dict['version']
        self.workspace = workspace
        self._mms_endpoint = _get_mms_url(workspace) + '/images/{}'.format(image_id)
        self._auth = workspace._auth
        self.models = models

    @staticmethod
    def image_configuration(execution_script, runtime, conda_file=None, docker_file=None, schema_file=None,
                            dependencies=None, enable_gpu=None, tags=None, properties=None, description=None):
        """
        Creates and returns a Container image configuration

        :param execution_script: Path to local file that contains the code to run for the image
        :type execution_script: str
        :param runtime: Which runtime to use for the image. Current supported runtimes are 'spark-py' and 'python'
        :type runtime: str
        :param conda_file: Path to local file containing a conda environment definition to use for the image
        :type conda_file: str
        :param docker_file: Path to local file containing additional Docker steps to run when setting up the image
        :type docker_file: str
        :param schema_file: Path to local file containing a webservice schema to use when the image is deployed
        :type schema_file: str
        :param dependencies: List of paths to additional files/folders that the image needs to run
        :type dependencies: list[str]
        :param enable_gpu: Whether or not to enable GPU support in the image
        :type enable_gpu: bool
        :param tags: Dictionary of key value tags to give this image
        :type tags: dict[str, str]
        :param properties: Dictionary of key value properties to give this image. These properties cannot
            be changed after deployment, however new key value pairs can be added
        :type properties: dict[str, str]
        :param description: A description to give this image
        :type description: str
        :return: A configuration object to use when creating the image
        :rtype: azureml.core.image.container.ContainerImageConfig
        :raises: azureml.exceptions.WebserviceException
        """

        conf = ContainerImageConfig(execution_script, runtime, conda_file, docker_file, schema_file, dependencies,
                                    enable_gpu, tags, properties, description)

        return conf

    def run(self, input_data):
        """
        Runs the image locally and tests with the given input data. Must have Docker installed and running to work

        :param input_data: The input data to pass to the image when run
        :type input_data: varies
        :return: The results of running the image
        :rtype: varies
        :raises: azureml.exceptions.WebserviceException
        """
        if not input_data:
            raise WebserviceException('Error: You must provide input data.')

        keys_endpoint = 'https://management.azure.com/subscriptions/{}/resourceGroups/{}/providers/' \
                        'Microsoft.MachineLearningServices/workspaces/' \
                        '{}/listKeys'.format(self.workspace.subscription_id,
                                             self.workspace.resource_group,
                                             self.workspace.name)
        headers = self.workspace._auth.get_authentication_header()
        params = {'api-version': WORKSPACE_RP_API_VERSION}
        try:
            keys_resp = requests.post(keys_endpoint, headers=headers, params=params)
            keys_resp.raise_for_status()
        except requests.exceptions.HTTPError:
            raise WebserviceException('Unable to retrieve workspace keys to run image:\n'
                                      'Response Code: {}\n'
                                      'Headers: {}\n'
                                      'Content: {}'.format(keys_resp.status_code, keys_resp.headers,
                                                           keys_resp.content))
        content = keys_resp.content
        if isinstance(content, bytes):
            content = content.decode('utf-8')
        keys_dict = json.loads(content)
        try:
            username = keys_dict['containerRegistryCredentials']['username']
            passwords = keys_dict['containerRegistryCredentials']['passwords']
            password = passwords[0]['value']
        except KeyError:
            raise WebserviceException('Unable to retrieve workspace keys to run image, response '
                                      'payload missing container registry credentials.')

        client = get_docker_client(username, password, self.image_location)

        pull_docker_image(client, self.image_location, username, password)

        container_name = self.id + str(uuid.uuid4())[:8]
        container = start_docker_container(client, self.image_location, container_name)

        docker_port = get_docker_port(client, container_name, container)

        docker_url = container_health_check(docker_port, container)

        scoring_result = container_scoring_call(docker_port, input_data, container, docker_url)

        cleanup_container(container)
        return scoring_result


class ContainerImageConfig(ImageConfig):
    """
    Image config specific to Container deployments - requires execution script and runtime.

    :param execution_script: Path to local file that contains the code to run for the image
    :type execution_script: str
    :param runtime: Which runtime to use for the image. Current supported runtimes are 'spark-py' and 'python'
    :type runtime: str
    :param conda_file: Path to local file containing a conda environment definition to use for the image
    :type conda_file: str
    :param docker_file: Path to local file containing additional Docker steps to run when setting up the image
    :type docker_file: str
    :param schema_file: Path to local file containing a webservice schema to use when the image is deployed
    :type schema_file: str
    :param dependencies: List of paths to additional files/folders that the image needs to run
    :type dependencies: list[str]
    :param enable_gpu: Whether or not to enable GPU support in the image
    :type enable_gpu: bool
    :param tags: Dictionary of key value tags to give this image
    :type tags: dict[str, str]
    :param properties: Dictionary of key value properties to give this image. These properties cannot
        be changed after deployment, however new key value pairs can be added
    :type properties: dict[str, str]
    :param description: A description to give this image
    :type description: str
    """
    def __init__(self, execution_script, runtime, conda_file=None, docker_file=None, schema_file=None,
                 dependencies=None, enable_gpu=None, tags=None, properties=None, description=None):
        """
        Initialize the config object

        :param execution_script: Path to local file that contains the code to run for the image
        :type execution_script: str
        :param runtime: Which runtime to use for the image. Current supported runtimes are 'spark-py' and 'python'
        :type runtime: str
        :param conda_file: Path to local file containing a conda environment definition to use for the image
        :type conda_file: str
        :param docker_file: Path to local file containing additional Docker steps to run when setting up the image
        :type docker_file: str
        :param schema_file: Path to local file containing a webservice schema to use when the image is deployed
        :type schema_file: str
        :param dependencies: List of paths to additional files/folders that the image needs to run
        :type dependencies: list[str]
        :param enable_gpu: Whether or not to enable GPU support in the image
        :type enable_gpu: bool
        :param tags: Dictionary of key value tags to give this image
        :type tags: dict[str, str]
        :param properties: Dictionary of key value properties to give this image. These properties cannot
            be changed after deployment, however new key value pairs can be added
        :type properties: dict[str, str]
        :param description: A description to give this image
        :type description: str
        :raises: azureml.exceptions.WebserviceException
        """
        self.execution_script = execution_script
        self.runtime = runtime
        self.conda_file = conda_file
        self.docker_file = docker_file
        self.schema_file = schema_file
        self.dependencies = dependencies
        self.enable_gpu = enable_gpu
        self.tags = tags
        self.properties = properties
        self.description = description

        self.execution_script_path = os.path.abspath(os.path.dirname(self.execution_script))
        self.validate_configuration()

    def build_create_payload(self, workspace, name, model_ids):
        """
        Builds the creation payload for the Container image

        :param workspace: The workspace object to create the image in
        :type workspace: azureml.core.workspace.Workspace
        :param name: The name of the image
        :type name: str
        :param model_ids: A list of model IDs to package into the image
        :type model_ids: list[str]
        :return: Container image creation payload
        :rtype: dict
        :raises: azureml.exceptions.WebserviceException
        """
        import copy
        from azureml._model_management._util import image_payload_template
        json_payload = copy.deepcopy(image_payload_template)
        json_payload['name'] = name
        json_payload['kvTags'] = self.tags
        json_payload['imageFlavor'] = WEBAPI_IMAGE_FLAVOR
        json_payload['properties'] = self.properties
        json_payload['description'] = self.description
        json_payload['targetRuntime']['runtimeType'] = SUPPORTED_RUNTIMES[self.runtime.lower()]
        json_payload['targetRuntime']['targetArchitecture'] = ARCHITECTURE_AMD64

        if self.enable_gpu:
            json_payload['targetRuntime']['properties']['installCuda'] = self.enable_gpu
        requirements = add_sdk_to_requirements()
        (json_payload['targetRuntime']['properties']['pipRequirements'], _) = \
            upload_dependency(workspace, requirements)
        if self.conda_file:
            conda_file = self.conda_file.rstrip(os.sep)
            (json_payload['targetRuntime']['properties']['condaEnvFile'], _) = \
                upload_dependency(workspace, conda_file)
        if self.docker_file:
            docker_file = self.docker_file.rstrip(os.sep)
            (json_payload['dockerFileUri'], _) = upload_dependency(workspace, docker_file)

        if model_ids:
            json_payload['modelIds'] = model_ids

        if self.schema_file:
            self.schema_file = self.schema_file.rstrip(os.sep)

        self.execution_script = self.execution_script.rstrip(os.sep)

        driver_mime_type = 'application/x-python'
        if not self.dependencies:
            self.dependencies = []
        wrapped_execution_script = wrap_execution_script(self.execution_script, self.schema_file, self.dependencies,
                                                         ContainerImage._log_aml_debug)

        (driver_package_location, _) = upload_dependency(workspace, wrapped_execution_script)
        json_payload['assets'].append({'id': 'driver', 'url': driver_package_location, 'mimeType': driver_mime_type})

        if self.schema_file:
            self.dependencies.append(self.schema_file)

        for dependency in self.dependencies:
            (artifact_url, artifact_id) = upload_dependency(workspace, dependency, create_tar=True)

            new_asset = {'mimeType': 'application/octet-stream',
                         'id': artifact_id,
                         'url': artifact_url,
                         'unpack': True}
            json_payload['assets'].append(new_asset)

        return json_payload

    def validate_configuration(self):
        """
        Checks that the specified configuration values are valid. Will raise a WebserviceException if validation
        fails.

        :raises: WebserviceException
        """
        # The driver file must be in the current directory
        if not os.getcwd() == self.execution_script_path:
            raise WebserviceException('Unable to use a driver file not in current directory. '
                                      'Please navigate to the location of the driver file and try again.')

        validate_path_exists_or_throw(self.execution_script, "Driver file")

        execution_script_name, execution_script_extension = os.path.splitext(self.execution_script)
        if execution_script_extension != '.py':
            raise WebserviceException('Invalid driver type. Currently only Python drivers are supported.')

        if self.runtime.lower() not in SUPPORTED_RUNTIMES.keys():
            runtimes = '|'.join(x for x in SUPPORTED_RUNTIMES.keys() if x not in UNDOCUMENTED_RUNTIMES)
            raise WebserviceException('Provided runtime not supported. '
                                      'Possible runtimes are: {}'.format(runtimes))

        if self.conda_file:
            validate_path_exists_or_throw(self.conda_file, "Conda file")

        if self.docker_file:
            validate_path_exists_or_throw(self.docker_file, "Docker file")

        if self.dependencies:
            for dependency in self.dependencies:
                validate_path_exists_or_throw(dependency, "Dependency")

        if self.schema_file:
            validate_path_exists_or_throw(self.schema_file, "Schema file")
            schema_file_path = os.path.abspath(os.path.dirname(self.schema_file))
            common_prefix = os.path.commonprefix([self.execution_script_path, schema_file_path])
            if not common_prefix == self.execution_script_path:
                raise WebserviceException('Schema file must be in the same directory as the driver file, '
                                          'or in a subdirectory.')

    @staticmethod
    def deserialize(workspace, image_payload):
        """
        Convert a json object into a ContainerImage object. Will fail if the provided workspace is not the workspace
        the image is registered under.

        :param workspace: The workspace object the ContainerImage is registered under
        :type workspace: azureml.core.workspace.Workspace
        :param image_payload: A json object to convert to a ContainerImage object
        :type image_payload: dict
        :return: The ContainerImage representation of the provided json object
        :rtype: ContainerImage
        """
        ContainerImage._deserialize(workspace, image_payload)
