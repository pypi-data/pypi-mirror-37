# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Module for managing the ACI Webservices in Azure ML"""

import requests
from dateutil.parser import parse
from azureml._model_management._constants import MMS_WORKSPACE_API_VERSION
from azureml._model_management._constants import MMS_SYNC_TIMEOUT_SECONDS
from azureml._model_management._util import _get_mms_url
from azureml.core.image import Image
from azureml.core.webservice import Webservice
from azureml.core.webservice.webservice import WebserviceDeploymentConfiguration
from azureml.exceptions import WebserviceException


class AciWebservice(Webservice):
    """
    Class for AzureML ACI Webservices
    """
    _expected_payload_keys = ['name', 'description', 'kvTags', 'properties', 'createdTime', 'computeType',
                              'containerResourceRequirements', 'imageId', 'scoringUri', 'location',
                              'authEnabled', 'sslEnabled', 'appInsightsEnabled', 'sslCertificate',
                              'sslKey', 'cname', 'publicIp']
    _webservice_type = 'ACI'

    def _initialize(self, workspace, obj_dict):
        """

        :param workspace:
        :type workspace: azureml.core.workspace.Workspace
        :param obj_dict:
        :type obj_dict: dict
        :return:
        :rtype: None
        """
        if 'imageDetails' in obj_dict:
            image = Image.deserialize(workspace, obj_dict['imageDetails'])

        name = obj_dict['name']
        description = obj_dict['description']
        tags = obj_dict['kvTags']
        properties = obj_dict['properties']
        state = obj_dict['state'] if 'state' in obj_dict else None
        created_time = parse(obj_dict['createdTime'])
        updated_time = parse(obj_dict['updatedTime']) if 'updatedTime' in obj_dict else None
        error = obj_dict['error'] if 'error' in obj_dict else None
        compute_type = obj_dict['computeType']
        mms_endpoint = _get_mms_url(workspace) + '/services/{}'.format(name)
        container_resource_requirements = \
            ContainerResourceRequirements.deserialize(obj_dict['containerResourceRequirements'])
        image_id = obj_dict['imageId']
        scoring_uri = obj_dict['scoringUri']
        location = obj_dict['location']
        auth_enabled = obj_dict['authEnabled']
        ssl_enabled = obj_dict['sslEnabled']
        app_insights_enabled = obj_dict['appInsightsEnabled']
        ssl_certificate = obj_dict['sslCertificate']
        ssl_key = obj_dict['sslKey']
        cname = obj_dict['cname']
        public_ip = obj_dict['publicIp']
        super(AciWebservice, self)._initialize(name, description, tags, properties, state, created_time,
                                               updated_time, error, compute_type, workspace, mms_endpoint,
                                               None, workspace._auth)
        self.container_resource_requirements = container_resource_requirements
        self.image_id = image_id
        self.image = image
        self.location = location
        self.auth_enabled = auth_enabled
        self.ssl_enabled = ssl_enabled
        self.app_insights_enabled = app_insights_enabled
        self.ssl_certificate = ssl_certificate
        self.ssl_key = ssl_key
        self.cname = cname
        self.public_ip = public_ip
        self.scoring_uri = scoring_uri
        self.swagger_uri = '/'.join(scoring_uri.split('/')[:-1]) + '/swagger.json' if scoring_uri else None

    @staticmethod
    def deploy_configuration(cpu_cores=None, memory_gb=None, tags=None, properties=None, description=None,
                             location=None, auth_enabled=None, ssl_enabled=None, app_insights_enabled=None,
                             ssl_cert_pem_file=None, ssl_key_pem_file=None, ssl_cname=None):
        """
        Create a configuration object for deploying an ACI Webservice

        :param cpu_cores: The number of cpu cores to allocate for this Webservice. Can be a decimal
        :type cpu_cores: float
        :param memory_gb: The amount of memory (in GB) to allocate for this Webservice. Can be a decimal
        :type memory_gb: float
        :param tags: Dictionary of key value tags to give this Webservice
        :type tags: dict[str, str]
        :param properties: Dictionary of key value properties to give this Webservice. These properties cannot
            be changed after deployment, however new key value pairs can be added
        :type properties: dict[str, str]
        :param description: A description to give this Webservice
        :type description: str
        :param location: The Azure region to deploy this Webservice to. If not specified the Workspace location will
            be used. More details on available regions can be found here:
            https://azure.microsoft.com/en-us/global-infrastructure/services/?regions=all&products=container-instances
        :type location: str
        :param auth_enabled: Whether or not to enable auth for this Webservice
        :type auth_enabled: bool
        :param ssl_enabled: Whether or not to enable SSL for this Webservice
        :type ssl_enabled: bool
        :param app_insights_enabled: Whether or not to enable AppInsights for this Webservice
        :type app_insights_enabled: bool
        :param ssl_cert_pem_file: The cert file needed if SSL is enabled
        :type ssl_cert_pem_file: str
        :param ssl_key_pem_file: The key file needed if SSL is enabled
        :type ssl_key_pem_file: str
        :param ssl_cname: The cname for if SSL is enabled
        :type ssl_cname: str
        :return: A configuration object to use when deploying a Webservice object
        :rtype: AciServiceDeploymentConfiguration
        :raises: WebserviceException
        """
        config = AciServiceDeploymentConfiguration(cpu_cores, memory_gb, tags, properties, description, location,
                                                   auth_enabled, ssl_enabled, app_insights_enabled, ssl_cert_pem_file,
                                                   ssl_key_pem_file, ssl_cname)
        return config

    @staticmethod
    def _deploy(workspace, name, image, deployment_config):
        """

        :param workspace:
        :type workspace: azureml.core.workspace.Workspace
        :param name:
        :type name: str
        :param image:
        :type image: azureml.core.image.Image
        :param deployment_config:
        :type deployment_config: AciServiceDeploymentConfiguration | None
        :return:
        :rtype: AciWebservice
        """
        if not deployment_config:
            deployment_config = AciWebservice.deploy_configuration()
        elif not isinstance(deployment_config, AciServiceDeploymentConfiguration):
            raise WebserviceException('Error, provided deployment configuration must be of type '
                                      'AciServiceDeploymentConfiguration in order to deploy an ACI service.')
        deployment_config.validate_image(image)
        create_payload = AciWebservice._build_create_payload(name, image, deployment_config)
        return Webservice._deploy_webservice(workspace, name, create_payload, AciWebservice)

    @staticmethod
    def _build_create_payload(name, image, deploy_config):
        """

        :param name:
        :type name: str
        :param image:
        :type image: azureml.core.image.Image
        :param deploy_config:
        :type deploy_config: azureml.core.compute.AciServiceDeploymentConfiguration
        :return:
        :rtype: dict
        """
        import copy
        from azureml._model_management._util import aci_service_payload_template
        json_payload = copy.deepcopy(aci_service_payload_template)
        json_payload['name'] = name
        json_payload['imageId'] = image.id
        json_payload['kvTags'] = deploy_config.tags
        json_payload['properties'] = deploy_config.properties
        json_payload['description'] = deploy_config.description
        json_payload['containerResourceRequirements']['cpu'] = deploy_config.cpu_cores
        json_payload['containerResourceRequirements']['memoryInGB'] = deploy_config.memory_gb
        json_payload['location'] = deploy_config.location
        if deploy_config.auth_enabled is None:
            del (json_payload['authEnabled'])
        else:
            json_payload['authEnabled'] = deploy_config.auth_enabled
        if deploy_config.ssl_enabled is None:
            del (json_payload['sslEnabled'])
        else:
            json_payload['sslEnabled'] = deploy_config.ssl_enabled
        if deploy_config.app_insights_enabled is None:
            del (json_payload['appInsightsEnabled'])
        else:
            json_payload['appInsightsEnabled'] = deploy_config.app_insights_enabled
        try:
            with open(deploy_config.ssl_cert_pem_file, 'r') as cert_file:
                cert_data = cert_file.read()
            json_payload['sslCertificate'] = cert_data
        except Exception:
            del (json_payload['sslCertificate'])
        try:
            with open(deploy_config.ssl_key_pem_file, 'r') as key_file:
                key_data = key_file.read()
            json_payload['sslKey'] = key_data
        except Exception:
            del (json_payload['sslKey'])
        if deploy_config.ssl_cname is None:
            del (json_payload['cname'])
        else:
            json_payload['cname'] = deploy_config.ssl_cname

        return json_payload

    def wait_for_deployment(self, show_output=False):
        """
        Automatically poll on the running Webservice deployment.

        :param show_output: Option to print more verbose output
        :type show_output: bool
        :raises: WebserviceException
        """
        try:
            operation_state, error = self._wait_for_deployment(show_output)
            print('ACI service creation operation finished, operation "{}"'.format(operation_state))
            if operation_state == 'Failed':
                if error and 'statusCode' in error and 'message' in error:
                    print('Service creation failed with\n'
                          'StatusCode: {}\n'
                          'Message: {}'.format(error['statusCode'], error['message']))
                else:
                    print('Service creation failed, unexpected error response:\n'
                          '{}'.format(error))
            self.update_deployment_state()
        except WebserviceException as e:
            if e.message == 'No operation endpoint':
                self.update_deployment_state()
                print('Long running operation information not known, unable to poll. '
                      'Current state is {}'.format(self.state))
            else:
                raise e

    def update_deployment_state(self):
        """
        Perform an in-place update of the properties of the object based on the current state of the
        corresponding cloud object. Primarily useful for manual polling of deployment state.
        """
        service = AciWebservice(self.workspace, name=self.name)
        self.error = service.error
        self.state = service.state
        self.updated_time = service.updated_time
        self.container_resource_requirements = service.container_resource_requirements
        self.image = service.image
        self.image_id = service.image_id
        self.scoring_uri = service.scoring_uri
        self.tags = service.tags
        self.properties = service.properties
        self.description = service.description
        self.location = service.location
        self.auth_enabled = service.auth_enabled
        self.ssl_enabled = service.ssl_enabled
        self.app_insights_enabled = service.app_insights_enabled
        self.ssl_certificate = service.ssl_certificate
        self.ssl_key = service.ssl_key
        self.cname = service.cname
        self.public_ip = service.public_ip

    def run(self, input_data):
        """
        Call this Webservice with the provided input

        :param input_data: The input to call the Webservice with
        :type input_data: varies
        :return: The result of calling the Webservice
        :rtype: dict
        :raises: WebserviceException
        """
        headers = {'Content-Type': 'application/json'}
        if self.auth_enabled:
            try:
                service_keys = self.get_keys()
            except WebserviceException as e:
                raise WebserviceException('Error attempting to retrieve service keys for use with scoring:\n'
                                          '{}'.format(e.message))
            headers['Authorization'] = 'Bearer ' + service_keys[0]

        resp = requests.post(self.scoring_uri, headers=headers, data=input_data)

        if resp.status_code == 200:
            return resp.json()
        else:
            raise WebserviceException('Received bad response from service:\n'
                                      'Response Code: {}\n'
                                      'Headers: {}\n'
                                      'Content: {}'.format(resp.status_code, resp.headers, resp.content))

    def update(self, image=None, tags=None, properties=None, description=None, auth_enabled=None, ssl_enabled=None,
               ssl_cert_pem_file=None, ssl_key_pem_file=None, ssl_cname=None, app_insights_enabled=None):
        """
        Update the Webservice with provided properties. Values left as None will remain unchanged in this Webservice

        :param image: A new Image to deploy to the Webservice
        :type image: azureml.core.image.Image
        :param tags: Dictionary of key value tags to give this Webservice. Will replace existing tags.
        :type tags: dict[str, str]
        :param properties: Dictionary of key value properties to add to existing properties dictionary
        :type properties: dict[str, str]
        :param description: A description to give this Webservice
        :type description: str
        :param auth_enabled: Enable or disable auth for this Webservice
        :type auth_enabled: bool
        :param ssl_enabled: Whether or not to enable SSL for this Webservice
        :type ssl_enabled: bool
        :param ssl_cert_pem_file: The cert file needed if SSL is enabled
        :type ssl_cert_pem_file: str
        :param ssl_key_pem_file: The key file needed if SSL is enabled
        :type ssl_key_pem_file: str
        :param ssl_cname: The cname for if SSL is enabled
        :type ssl_cname: str
        :param app_insights_enabled: Whether or not to enable AppInsights for this Webservice
        :type app_insights_enabled: bool
        :return:
        :rtype: None
        """
        if not image and tags is None and properties is None and not description and auth_enabled is None \
           and ssl_enabled is None and not ssl_cert_pem_file and not ssl_key_pem_file and not ssl_cname \
           and app_insights_enabled is None:
            raise WebserviceException('No parameters provided to update.')

        cert_data = ""
        key_data = ""
        if ssl_enabled or (ssl_enabled is None and self.ssl_enabled):
            if not ssl_cert_pem_file or not ssl_key_pem_file or not ssl_cname:
                raise WebserviceException('SSL is enabled, you must provide a SSL certificate, key, and cname.')
            else:
                try:
                    with open(ssl_cert_pem_file, 'r') as cert_file:
                        cert_data = cert_file.read()
                    with open(ssl_key_pem_file, 'r') as key_file:
                        key_data = key_file.read()
                except (IOError, OSError) as exc:
                    raise WebserviceException("Error while reading ssl information:\n{}".format(exc))

        headers = {'Content-Type': 'application/json-patch+json'}
        headers.update(self._auth.get_authentication_header())
        params = {'api-version': MMS_WORKSPACE_API_VERSION}

        patch_list = []
        if image:
            patch_list.append({'op': 'replace', 'path': '/imageId', 'value': image.id})
        if tags is not None:
            patch_list.append({'op': 'replace', 'path': '/kvTags', 'value': tags})
        if properties is not None:
            patch_list.append({'op': 'replace', 'path': '/properties', 'value': properties})
        if description:
            patch_list.append({'op': 'replace', 'path': '/description', 'value': description})
        if auth_enabled is not None:
            patch_list.append({'op': 'replace', 'path': '/authEnabled', 'value': auth_enabled})
        if ssl_enabled is not None:
            patch_list.append({'op': 'replace', 'path': '/sslEnabled', 'value': ssl_enabled})
        if ssl_cert_pem_file and ssl_enabled or ssl_cert_pem_file and self.ssl_enabled:
            patch_list.append({'op': 'replace', 'path': '/sslCertificate', 'value': cert_data})
        if ssl_key_pem_file and ssl_enabled or ssl_key_pem_file and self.ssl_enabled:
            patch_list.append({'op': 'replace', 'path': '/sslKey', 'value': key_data})
        if ssl_cname and ssl_enabled or ssl_cname and self.ssl_enabled:
            patch_list.append({'op': 'replace', 'path': '/cname', 'value': ssl_cname})
        if app_insights_enabled is not None:
            patch_list.append({'op': 'replace', 'path': '/appInsightsEnabled', 'value': app_insights_enabled})
        resp = requests.patch(self._mms_endpoint, headers=headers, params=params, json=patch_list,
                              timeout=MMS_SYNC_TIMEOUT_SECONDS)

        if resp.status_code == 200:
            self.update_deployment_state()
        elif resp.status_code == 202:
            if 'Operation-Location' in resp.headers:
                operation_location = resp.headers['Operation-Location']
            else:
                raise WebserviceException('Missing response header key: Operation-Location')
            create_operation_status_id = operation_location.split('/')[-1]
            base_url = '/'.join(self._mms_endpoint.split('/')[:-2])
            operation_url = base_url + '/operations/{}'.format(create_operation_status_id)
            self._operation_endpoint = operation_url
            self.update_deployment_state()
        else:
            raise WebserviceException('Received bad response from Model Management Service:\n'
                                      'Response Code: {}\n'
                                      'Headers: {}\n'
                                      'Content: {}'.format(resp.status_code, resp.headers, resp.content))

    def add_tags(self, tags):
        """
        Add key value pairs to this Webservice's tags dictionary

        :param tags: The dictionary of tags to add
        :type tags: dict[str, str]
        :raises: WebserviceException
        """
        updated_tags = self._add_tags(tags)
        self.tags = updated_tags
        self.update(tags=updated_tags)

        print('Image tag add operation complete.')

    def remove_tags(self, tags):
        """
        Remove the specified keys from this Webservice's dictionary of tags.

        :param tags: The list of keys to remove
        :type tags: list[str]
        """
        updated_tags = self._remove_tags(tags)
        self.tags = updated_tags
        self.update(tags=updated_tags)

        print('Image tag remove operation complete.')

    def add_properties(self, properties):
        """
        Add key value pairs to this Webservice's properties dictionary.

        :param properties: The dictionary of properties to add
        :type properties: dict[str, str]
        """
        updated_properties = self._add_properties(properties)
        self.properties = updated_properties
        self.update(properties=updated_properties)

        print('Image tag properties operation complete.')

    def serialize(self):
        """
        Convert this Webservice into a json serialized dictionary.

        :return: The json representation of this Webservice
        :rtype: dict
        """
        properties = super(AciWebservice, self).serialize()
        container_resource_requirements = self.container_resource_requirements.serialize() \
            if self.container_resource_requirements else None
        image = self.image.serialize() if self.image else None
        aci_properties = {'containerResourceRequirements': container_resource_requirements, 'imageId': self.image_id,
                          'imageDetails': image, 'scoringUri': self.scoring_uri, 'location': self.location,
                          'authEnabled': self.auth_enabled, 'sslEnabled': self.ssl_enabled,
                          'appInsightsEnabled': self.app_insights_enabled, 'sslCertificate': self.ssl_certificate,
                          'sslKey': self.ssl_key, 'cname': self.cname, 'publicIp': self.public_ip}
        properties.update(aci_properties)
        return properties

    @staticmethod
    def deserialize(workspace, webservice_payload):
        """
        Convert a json object into a AciWebservice object. Will fail if the provided workspace is not the workspace the
        Webservice is registered under.

        :param workspace: The workspace object the AciWebservice is registered under
        :type workspace: azureml.core.workspace.Workspace
        :param webservice_payload: A json object to convert to a Webservice object
        :type webservice_payload: dict
        :return: The AciWebservice representation of the provided json object
        :rtype: AciWebservice
        """
        AciWebservice._validate_get_payload(webservice_payload)
        webservice = AciWebservice(None, None)
        webservice._initialize(workspace, webservice_payload)
        return webservice

    @staticmethod
    def _validate_get_payload(payload):
        """

        :param payload:
        :type payload: dict
        :return:
        :rtype: None
        """
        if 'computeType' not in payload:
            raise WebserviceException('Invalid webservice payload, missing computeType:\n'
                                      '{}'.format(payload))
        if payload['computeType'] != AciWebservice._webservice_type:
            raise WebserviceException('Invalid payload for ACI webservice, computeEnvironmentType is not "ACI":\n'
                                      '{}'.format(payload))
        for service_key in AciWebservice._expected_payload_keys:
            if service_key not in payload:
                raise WebserviceException('Invalid ACI webservice payload, missing "{}":\n'
                                          '{}'.format(service_key, payload))


class ContainerResourceRequirements(object):
    """
    Class containing details for the resource requirements for the Webservice
    """
    _expected_payload_keys = ['cpu', 'memoryInGB']

    def __init__(self, cpu, memory_in_gb):
        """
        Initialize the container resource requirements

        :param cpu: The number of cpu cores to allocate for this Webservice. Can be a decimal
        :type cpu: float
        :param memory_in_gb: The amount of memory (in GB) to allocate for this Webservice. Can be a decimal
        :type memory_in_gb: float
        """
        self.cpu = cpu
        self.memory_in_gb = memory_in_gb

    def serialize(self):
        """
        Convert this ContainerResourceRequirements into a json serialized dictionary.

        :return: The json representation of this ContainerResourceRequirements
        :rtype: dict
        """
        return {'cpu': self.cpu, 'memoryInGB': self.memory_in_gb}

    @staticmethod
    def deserialize(payload_obj):
        """
        Convert a json object into a ContainerResourceRequirements object.

        :param payload_obj: A json object to convert to a ContainerResourceRequirements object
        :type payload_obj: dict
        :return: The ContainerResourceRequirements representation of the provided json object
        :rtype: ContainerResourceRequirements
        """
        for payload_key in ContainerResourceRequirements._expected_payload_keys:
            if payload_key not in payload_obj:
                raise WebserviceException('Invalid webservice payload, missing {} for containerResourceReservation:\n'
                                          '{}'.format(payload_key, payload_obj))

        return ContainerResourceRequirements(payload_obj['cpu'], payload_obj['memoryInGB'])


class AciServiceDeploymentConfiguration(WebserviceDeploymentConfiguration):
    """
    Service deployment configuration object for services deployed to ACI.

    :param cpu_cores: The number of cpu cores to allocate for this Webservice. Can be a decimal
    :type cpu_cores: float
    :param memory_gb: The amount of memory (in GB) to allocate for this Webservice. Can be a decimal
    :type memory_gb: float
    :param tags: Dictionary of key value tags to give this Webservice
    :type tags: dict[str, str]
    :param properties: Dictionary of key value properties to give this Webservice. These properties cannot
        be changed after deployment, however new key value pairs can be added
    :type properties: dict[str, str]
    :param description: A description to give this Webservice
    :type description: str
    :param location: The Azure region to deploy this Webservice to. If not specified the Workspace location will
        be used. More details on available regions can be found here:
        https://azure.microsoft.com/en-us/global-infrastructure/services/?regions=all&products=container-instances
    :type location: str
    :param auth_enabled: Whether or not to enable auth for this Webservice
    :type auth_enabled: bool
    :param ssl_enabled: Whether or not to enable SSL for this Webservice
    :type ssl_enabled: bool
    :param app_insights_enabled: Whether or not to enable AppInsights for this Webservice
    :type app_insights_enabled: bool
    :param ssl_cert_pem_file: The cert file needed if SSL is enabled
    :type ssl_cert_pem_file: str
    :param ssl_key_pem_file: The key file needed if SSL is enabled
    :type ssl_key_pem_file: str
    :param ssl_cname: The cname for if SSL is enabled
    :type ssl_cname: str
    """
    webservice_type = AciWebservice

    def __init__(self, cpu_cores=None, memory_gb=None, tags=None, properties=None, description=None, location=None,
                 auth_enabled=None, ssl_enabled=None, app_insights_enabled=None, ssl_cert_pem_file=None,
                 ssl_key_pem_file=None, ssl_cname=None):
        """
        Create a configuration object for deploying an ACI Webservice

        :param cpu_cores: The number of cpu cores to allocate for this Webservice. Can be a decimal
        :type cpu_cores: float
        :param memory_gb: The amount of memory (in GB) to allocate for this Webservice. Can be a decimal
        :type memory_gb: float
        :param tags: Dictionary of key value tags to give this Webservice
        :type tags: dict[str, str]
        :param properties: Dictionary of key value properties to give this Webservice. These properties cannot
            be changed after deployment, however new key value pairs can be added
        :type properties: dict[str, str]
        :param description: A description to give this Webservice
        :type description: str
        :param location: The Azure region to deploy this Webservice to. If not specified the Workspace location will
            be used. More details on available regions can be found here:
            https://azure.microsoft.com/en-us/global-infrastructure/services/?regions=all&products=container-instances
        :type location: str
        :param auth_enabled: Whether or not to enable auth for this Webservice
        :type auth_enabled: bool
        :param ssl_enabled: Whether or not to enable SSL for this Webservice
        :type ssl_enabled: bool
        :param app_insights_enabled: Whether or not to enable AppInsights for this Webservice
        :type app_insights_enabled: bool
        :param ssl_cert_pem_file: The cert file needed if SSL is enabled
        :type ssl_cert_pem_file: str
        :param ssl_key_pem_file: The key file needed if SSL is enabled
        :type ssl_key_pem_file: str
        :param ssl_cname: The cname for if SSL is enabled
        :type ssl_cname: str
        :raises: WebserviceException
        """
        super(AciServiceDeploymentConfiguration, self).__init__(AciWebservice)
        self.cpu_cores = cpu_cores
        self.memory_gb = memory_gb
        self.tags = tags
        self.properties = properties
        self.description = description
        self.location = location
        self.auth_enabled = auth_enabled
        self.ssl_enabled = ssl_enabled
        self.app_insights_enabled = app_insights_enabled
        self.ssl_cert_pem_file = ssl_cert_pem_file
        self.ssl_key_pem_file = ssl_key_pem_file
        self.ssl_cname = ssl_cname
        self.validate_configuration()

    def validate_configuration(self):
        """
        Checks that the specified configuration values are valid. Will raise a WebserviceException if validation
        fails.

        :raises: WebserviceException
        """
        if self.cpu_cores and self.cpu_cores <= 0:
            raise WebserviceException('Invalid configuration, cpu_cores must be positive.')
        if self.memory_gb and self.memory_gb <= 0:
            raise WebserviceException('Invalid configuration, memory_gb must be positive.')
        if self.ssl_enabled:
            if not self.ssl_cert_pem_file or not self.ssl_key_pem_file or not self.ssl_cname:
                raise WebserviceException('SSL is enabled, you must provide a SSL certificate, key, and cname.')
