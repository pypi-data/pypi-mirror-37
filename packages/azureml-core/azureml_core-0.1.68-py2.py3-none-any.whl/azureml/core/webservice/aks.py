# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Module for managing the AKS Webservices in Azure ML"""

import requests
from dateutil.parser import parse
from azureml._model_management._constants import MMS_WORKSPACE_API_VERSION
from azureml._model_management._util import _get_mms_url
from azureml.core.image import Image
from azureml.core.webservice import Webservice
from azureml.core.webservice.webservice import WebserviceDeploymentConfiguration
from azureml.exceptions import WebserviceException


class AksWebservice(Webservice):
    """
    Class for AzureML AKS Webservices
    """
    _expected_payload_keys = ['name', 'description', 'kvTags', 'properties', 'createdTime', 'computeType',
                              'appInsightsEnabled', 'authEnabled', 'autoScaler', 'computeName', 'authEnabled',
                              'containerResourceRequirements', 'dataCollection', 'imageId',
                              'maxConcurrentRequestsPerContainer', 'numReplicas', 'scoringTimeoutMs', 'scoringUri']
    _webservice_type = 'AKS'

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
        app_insights_enabled = obj_dict['appInsightsEnabled']
        auth_enabled = obj_dict['authEnabled']
        autoscaler = AutoScaler.deserialize(obj_dict['autoScaler'])
        compute_name = obj_dict['computeName']
        auth_enabled = obj_dict['authEnabled']
        container_resource_requirements = \
            ContainerResourceRequirements.deserialize(obj_dict['containerResourceRequirements'])
        created_time = parse(obj_dict['createdTime'])
        data_collection = DataCollection.deserialize(obj_dict['dataCollection'])
        deployment_status = obj_dict['deploymentStatus'] if 'deploymentStatus' in obj_dict else None
        state = obj_dict['state'] if 'state' in obj_dict else None
        description = obj_dict['description']
        error = obj_dict['error'] if 'error' in obj_dict else None
        compute_type = obj_dict['computeType']
        image_id = obj_dict['imageId']
        max_concurrent_requests_per_container = obj_dict['maxConcurrentRequestsPerContainer']
        name = obj_dict['name']
        mms_endpoint = _get_mms_url(workspace) + '/services/{}'.format(name)
        num_replicas = obj_dict['numReplicas']
        scoring_timeout_ms = obj_dict['scoringTimeoutMs']
        scoring_uri = obj_dict['scoringUri']
        tags = obj_dict['kvTags']
        properties = obj_dict['properties']
        updated_time = parse(obj_dict['updatedTime']) if 'updatedTime' in obj_dict else None
        super(AksWebservice, self)._initialize(name, description, tags, properties, state, created_time,
                                               updated_time, error, compute_type, workspace, mms_endpoint,
                                               None, workspace._auth)
        self.app_insights_enabled = app_insights_enabled
        self.auth_enabled = auth_enabled
        self.autoscaler = autoscaler
        self.compute_name = compute_name
        self.auth_enabled = auth_enabled
        self.container_resource_requirements = container_resource_requirements
        self.data_collection = data_collection
        self.image_id = image_id
        self.max_concurrent_requests_per_container = max_concurrent_requests_per_container
        self.num_replicas = num_replicas
        self.scoring_timeout_ms = scoring_timeout_ms
        self.image = image
        self.deployment_status = deployment_status
        self.scoring_uri = scoring_uri
        self.swagger_uri = '/'.join(scoring_uri.split('/')[:-1]) + '/swagger.json' if scoring_uri else None

    @staticmethod
    def deploy_configuration(autoscale_enabled=None, autoscale_min_replicas=None, autoscale_max_replicas=None,
                             autoscale_refresh_seconds=None, autoscale_target_utilization=None,
                             collect_model_data=None, auth_enabled=None, cpu_cores=None, memory_gb=None,
                             enable_app_insights=None, scoring_timeout_ms=None, replica_max_concurrent_requests=None,
                             num_replicas=None, primary_key=None, secondary_key=None, tags=None, properties=None,
                             description=None):
        """
        Create a configuration object for deploying to an AKS compute target

        :param autoscale_enabled: Whether or not to enable autoscaling for this Webservice
        :type autoscale_enabled: bool
        :param autoscale_min_replicas: The minimum number of containers to use when autoscaling this Webservice
        :type autoscale_min_replicas: int
        :param autoscale_max_replicas: The maximum number of containers to use when autoscaling this Webservice
        :type autoscale_max_replicas: int
        :param autoscale_refresh_seconds: How often the autoscaler should attempt to scale this Webservice
        :type autoscale_refresh_seconds: int
        :param autoscale_target_utilization: The target utilization (in percent out of 100) the autoscaler should
            attempt to maintain for this Webservice
        :type autoscale_target_utilization: int
        :param collect_model_data: Whether or not to enable model data collection for this Webservice
        :type collect_model_data: bool
        :param auth_enabled: Whether or not to enable auth for this Webservice
        :type auth_enabled: bool
        :param cpu_cores: The number of cpu cores to allocate for this Webservice. Can be a decimal
        :type cpu_cores: float
        :param memory_gb: The amount of memory (in GB) to allocate for this Webservice. Can be a decimal
        :type memory_gb: float
        :param enable_app_insights: Whether or not to enable Application Insights logging for this Webservice
        :type enable_app_insights: bool
        :param scoring_timeout_ms: A timeout to enforce for scoring calls to this Webservice
        :type scoring_timeout_ms: int
        :param replica_max_concurrent_requests: The number of maximum concurrent requests per node to allow for this
            Webservice
        :type replica_max_concurrent_requests: int
        :param num_replicas: The number of containers to allocate for this Webservice
        :type num_replicas: int
        :param primary_key: A primary auth key to use for this Webservice
        :type primary_key: str
        :param secondary_key: A secondary auth key to use for this Webservice
        :type secondary_key: str
        :param tags: Dictionary of key value tags to give this Webservice
        :type tags: dict[str, str]
        :param properties: Dictionary of key value properties to give this Webservice. These properties cannot
            be changed after deployment, however new key value pairs can be added
        :type properties: dict[str, str]
        :param description: A description to give this Webservice
        :type description: str
        :return: A configuration object to use when deploying a Webservice object
        :rtype: AksServiceDeploymentConfiguration
        :raises: WebserviceException
        """
        config = AksServiceDeploymentConfiguration(autoscale_enabled, autoscale_min_replicas, autoscale_max_replicas,
                                                   autoscale_refresh_seconds, autoscale_target_utilization,
                                                   collect_model_data, auth_enabled, cpu_cores, memory_gb,
                                                   enable_app_insights, scoring_timeout_ms,
                                                   replica_max_concurrent_requests, num_replicas,
                                                   primary_key, secondary_key, tags, properties, description)
        return config

    @staticmethod
    def _deploy(workspace, name, image, deployment_config, deployment_target):
        """

        :param workspace:
        :type workspace: azureml.core.workspace.Workspace
        :param name:
        :type name: str
        :param image:
        :type image: azureml.core.image.Image
        :param deployment_config:
        :type deployment_config: AksServiceDeploymentConfiguration | None
        :param deployment_target:
        :type deployment_target: azureml.core.compute.AksCompute
        :return:
        :rtype: AksWebservice
        """
        if not deployment_target:
            raise WebserviceException("Must have a deployment target for an AKS web service.")
        if not deployment_config:
            deployment_config = AksWebservice.deploy_configuration()
        elif not isinstance(deployment_config, AksServiceDeploymentConfiguration):
            raise WebserviceException('Error, provided deployment configuration must be of type '
                                      'AksServiceDeploymentConfiguration in order to deploy an AKS service.')
        deployment_config.validate_image(image)
        create_payload = AksWebservice._build_create_payload(name, image, deployment_target, deployment_config)
        return Webservice._deploy_webservice(workspace, name, create_payload, AksWebservice)

    @staticmethod
    def _build_create_payload(name, image, target, config):
        """

        :param name:
        :type name: str
        :param image:
        :type image: azureml.core.image.Image
        :param target:
        :type target: azureml.core.compute.AksCompute
        :param config:
        :type config: azureml.core.compute.AksServiceDeploymentConfiguration
        :return:
        :rtype: dict
        """
        import copy
        from azureml._model_management._util import aks_service_payload_template
        json_payload = copy.deepcopy(aks_service_payload_template)
        json_payload['name'] = name
        json_payload['computeType'] = 'AKS'
        json_payload['computeName'] = target.name
        json_payload['imageId'] = image.id
        if config.description:
            json_payload['description'] = config.description
        else:
            del(json_payload['description'])
        if config.tags:
            json_payload['kvTags'] = config.tags
        if config.properties:
            json_payload['properties'] = config.properties
        else:
            del(json_payload['properties'])
        if config.num_replicas:
            json_payload['numReplicas'] = config.num_replicas
        else:
            del(json_payload['numReplicas'])
        if config.collect_model_data is None:
            del (json_payload['dataCollection'])
        else:
            json_payload['dataCollection']['storageEnabled'] = config.collect_model_data
        if config.enable_app_insights is None:
            del (json_payload['appInsightsEnabled'])
        else:
            json_payload['appInsightsEnabled'] = config.enable_app_insights
        if not config.autoscale_enabled:
            del (json_payload['autoScaler'])
        else:
            json_payload['autoScaler']['autoscaleEnabled'] = config.autoscale_enabled
            json_payload['autoScaler']['minReplicas'] = config.autoscale_min_replicas
            json_payload['autoScaler']['maxReplicas'] = config.autoscale_max_replicas
            json_payload['autoScaler']['targetUtilization'] = config.autoscale_target_utilization
            json_payload['autoScaler']['refreshPeriodInSeconds'] = config.autoscale_refresh_seconds
            if 'numReplicas' in json_payload:
                del (json_payload['numReplicas'])
        if config.auth_enabled is None:
            del(json_payload['authEnabled'])
        else:
            json_payload['authEnabled'] = config.auth_enabled
        if config.cpu_cores or config.memory_gb:
            if config.cpu_cores:
                json_payload['containerResourceRequirements']['cpu'] = config.cpu_cores
            else:
                del(json_payload['containerResourceRequirements']['cpu'])
            if config.memory_gb:
                json_payload['containerResourceRequirements']['memoryInGB'] = config.memory_gb
            else:
                del(json_payload['containerResourceRequirements']['memoryInGB'])
        else:
            del(json_payload['containerResourceRequirements'])
        json_payload['maxConcurrentRequestsPerContainer'] = config.replica_max_concurrent_requests
        if config.primary_key:
            json_payload['keys']['primaryKey'] = config.primary_key
            json_payload['keys']['secondaryKey'] = config.secondary_key
        else:
            del(json_payload['keys'])
        if config.scoring_timeout_ms:
            json_payload['scoringTimeoutMs'] = config.scoring_timeout_ms
        else:
            del(json_payload['scoringTimeoutMs'])

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
            print('AKS service creation operation finished, operation "{}"'.format(operation_state))
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
        service = AksWebservice(self.workspace, name=self.name)
        self.error = service.error
        self.state = service.state
        self.deployment_status = service.deployment_status
        self.updated_time = service.updated_time
        self.image = service.image
        self.image_id = service.image_id
        self.app_insights_enabled = service.app_insights_enabled
        self.autoscaler = service.autoscaler
        self.auth_enabled = service.auth_enabled
        self.container_resource_requirements = service.container_resource_requirements
        self.data_collection = service.data_collection
        self.max_concurrent_requests_per_container = service.max_concurrent_requests_per_container
        self.num_replicas = service.num_replicas
        self.scoring_timeout_ms = service.scoring_timeout_ms
        self.scoring_uri = service.scoring_uri
        self.tags = service.tags
        self.properties = service.properties
        self.description = service.description

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

    def update(self, image=None, autoscale_enabled=None, autoscale_min_replicas=None, autoscale_max_replicas=None,
               autoscale_refresh_seconds=None, autoscale_target_utilization=None, collect_model_data=None,
               auth_enabled=None, cpu_cores=None, memory_gb=None, enable_app_insights=None, scoring_timeout_ms=None,
               replica_max_concurrent_requests=None, num_replicas=None, tags=None, properties=None, description=None):
        """
        Update the Webservice with provided properties. Values left as None will remain unchanged in this Webservice

        :param image: A new Image to deploy to the Webservice
        :type image: Image
        :param autoscale_enabled: Enable or disable autoscaling of this Webservice
        :type autoscale_enabled: bool
        :param autoscale_min_replicas: The minimum number of containers to use when autoscaling this Webservice
        :type autoscale_min_replicas: int
        :param autoscale_max_replicas: The maximum number of containers to use when autoscaling this Webservice
        :type autoscale_max_replicas: int
        :param autoscale_refresh_seconds: How often the autoscaler should attempt to scale this Webservice
        :type autoscale_refresh_seconds: int
        :param autoscale_target_utilization: The target utilization (in percent out of 100) the autoscaler should
            attempt to maintain for this Webservice
        :type autoscale_target_utilization: int
        :param collect_model_data: Enable or disable model data collection for this Webservice
        :type collect_model_data: bool
        :param auth_enabled: Whether or not to enable auth for this Webservice
        :type auth_enabled: bool
        :param cpu_cores: The number of cpu cores to allocate for this Webservice. Can be a decimal
        :type cpu_cores: float
        :param memory_gb: The amount of memory (in GB) to allocate for this Webservice. Can be a decimal
        :type memory_gb: float
        :param enable_app_insights: Whether or not to enable Application Insights logging for this Webservice
        :type enable_app_insights: bool
        :param scoring_timeout_ms: A timeout to enforce for scoring calls to this Webservice
        :type scoring_timeout_ms: int
        :param replica_max_concurrent_requests: The number of maximum concurrent requests per node to allow for this
            Webservice
        :type replica_max_concurrent_requests: int
        :param num_replicas: The number of containers to allocate for this Webservice
        :type num_replicas: int
        :param tags: Dictionary of key value tags to give this Webservice. Will replace existing tags.
        :type tags: dict[str, str]
        :param properties: Dictionary of key value properties to add to existing properties dictionary
        :type properties: dict[str, str]
        :param description: A description to give this Webservice
        :type description: str
        :raises: WebserviceException
        """
        if not image and autoscale_enabled is None and not autoscale_min_replicas and not autoscale_max_replicas \
                and not autoscale_refresh_seconds and not autoscale_target_utilization and collect_model_data is None \
                and auth_enabled is None and not cpu_cores and not memory_gb and enable_app_insights is None \
                and not scoring_timeout_ms and not replica_max_concurrent_requests and not num_replicas \
                and tags is None and properties is None and not description:
            raise WebserviceException('No parameters provided to update.')

        headers = {'Content-Type': 'application/json-patch+json'}
        headers.update(self._auth.get_authentication_header())
        params = {'api-version': MMS_WORKSPACE_API_VERSION}

        self._validate_update(image, autoscale_enabled, autoscale_min_replicas, autoscale_max_replicas,
                              autoscale_refresh_seconds, autoscale_target_utilization, collect_model_data, cpu_cores,
                              memory_gb, enable_app_insights, scoring_timeout_ms, replica_max_concurrent_requests,
                              num_replicas, tags, properties, description)

        patch_list = []
        if image:
            patch_list.append({'op': 'replace', 'path': '/imageId', 'value': image.id})
        if autoscale_enabled is not None:
            patch_list.append({'op': 'replace', 'path': '/autoScaler/autoscaleEnabled', 'value': autoscale_enabled})
        if autoscale_min_replicas:
            patch_list.append({'op': 'replace', 'path': '/autoScaler/minReplicas', 'value': autoscale_min_replicas})
        if autoscale_max_replicas:
            patch_list.append({'op': 'replace', 'path': '/autoScaler/maxReplicas', 'value': autoscale_max_replicas})
        if autoscale_refresh_seconds:
            patch_list.append({'op': 'replace', 'path': '/autoScaler/refreshPeriodInSeconds',
                               'value': autoscale_refresh_seconds})
        if autoscale_target_utilization:
            patch_list.append({'op': 'replace', 'path': '/autoScaler/targetUtilization',
                               'value': autoscale_target_utilization})
        if collect_model_data is not None:
            patch_list.append({'op': 'replace', 'path': '/dataCollection/storageEnabled', 'value': collect_model_data})
        if auth_enabled is not None:
            patch_list.append({'op': 'replace', 'path': '/authEnabled', 'value': auth_enabled})
        if cpu_cores:
            patch_list.append({'op': 'replace', 'path': '/containerResourceRequirements/cpu', 'value': cpu_cores})
        if memory_gb:
            patch_list.append({'op': 'replace', 'path': '/containerResourceRequirements/memoryInGB',
                               'value': memory_gb})
        if enable_app_insights is not None:
            patch_list.append({'op': 'replace', 'path': '/appInsightsEnabled', 'value': enable_app_insights})
        if scoring_timeout_ms:
            patch_list.append({'op': 'replace', 'path': '/scoringTimeoutMs', 'value': scoring_timeout_ms})
        if replica_max_concurrent_requests:
            patch_list.append({'op': 'replace', 'path': '/maxConcurrentRequestsPerContainer',
                               'value': replica_max_concurrent_requests})
        if num_replicas:
            patch_list.append({'op': 'replace', 'path': '/numReplicas', 'value': num_replicas})
        if tags is not None:
            patch_list.append({'op': 'replace', 'path': '/kvTags', 'value': tags})
        if properties is not None:
            patch_list.append({'op': 'replace', 'path': '/properties', 'value': properties})
        if description:
            patch_list.append({'op': 'replace', 'path': '/description', 'value': description})

        try:
            resp = requests.patch(self._mms_endpoint, headers=headers, params=params, json=patch_list)
            resp.raise_for_status()
        except requests.ConnectionError:
            raise WebserviceException('Error connecting to {}.'.format(self._mms_endpoint))
        except requests.exceptions.HTTPError:
            raise WebserviceException('Received bad response from Model Management Service:\n'
                                      'Response Code: {}\n'
                                      'Headers: {}\n'
                                      'Content: {}'.format(resp.status_code, resp.headers, resp.content))

        if 'Operation-Location' in resp.headers:
            operation_location = resp.headers['Operation-Location']
        else:
            raise WebserviceException('Missing response header key: Operation-Location')
        create_operation_status_id = operation_location.split('/')[-1]
        base_url = '/'.join(self._mms_endpoint.split('/')[:-2])
        operation_url = base_url + '/operations/{}'.format(create_operation_status_id)
        self._operation_endpoint = operation_url
        self.update_deployment_state()

    def _validate_update(self, image, autoscale_enabled, autoscale_min_replicas, autoscale_max_replicas,
                         autoscale_refresh_seconds, autoscale_target_utilization, collect_model_data, cpu_cores,
                         memory_gb, enable_app_insights, scoring_timeout_ms, replica_max_concurrent_requests,
                         num_replicas, tags, properties, description):
        """

        :param image:
        :type image: Image
        :param autoscale_enabled:
        :type autoscale_enabled: bool
        :param autoscale_min_replicas:
        :type autoscale_min_replicas: int
        :param autoscale_max_replicas:
        :type autoscale_max_replicas: int
        :param autoscale_refresh_seconds:
        :type autoscale_refresh_seconds: int
        :param autoscale_target_utilization:
        :type autoscale_target_utilization: int
        :param collect_model_data:
        :type collect_model_data: bool
        :param cpu_cores:
        :type cpu_cores: float
        :param memory_gb:
        :type memory_gb: float
        :param enable_app_insights:
        :type enable_app_insights: bool
        :param scoring_timeout_ms:
        :type scoring_timeout_ms: int
        :param replica_max_concurrent_requests:
        :type replica_max_concurrent_requests: int
        :param num_replicas:
        :type num_replicas: int
        :param tags:
        :type tags: dict[str, str]
        :param properties:
        :type properties: dict[str, str]
        :param description:
        :type description: str
        """
        if cpu_cores and cpu_cores <= 0:
            raise WebserviceException('Error, cpu_cores must be greater than zero.')
        if memory_gb and memory_gb <= 0:
            raise WebserviceException('Error, memory_gb must be greater than zero.')
        if scoring_timeout_ms and scoring_timeout_ms <= 0:
            raise WebserviceException('Error, scoring_timeout_ms must be greater than zero.')
        if replica_max_concurrent_requests and replica_max_concurrent_requests <= 0:
            raise WebserviceException('Error, replica_max_concurrent_requests must be greater than '
                                      'zero.')
        if num_replicas and num_replicas <= 0:
            raise WebserviceException('Error, num_replicas must be greater than zero.')
        if autoscale_enabled:
            if num_replicas:
                raise WebserviceException('Error, autoscale enabled and num_replicas provided.')
            if autoscale_min_replicas and autoscale_min_replicas <= 0:
                raise WebserviceException('Error, autoscale_min_replicas must be greater than '
                                          'zero.')
            if autoscale_max_replicas and autoscale_max_replicas <= 0:
                raise WebserviceException('Error, autoscale_max_replicas must be greater than '
                                          'zero.')
            if autoscale_min_replicas and autoscale_max_replicas and \
                    autoscale_min_replicas > autoscale_max_replicas:
                raise WebserviceException('Error, autoscale_min_replicas cannot be greater than '
                                          'autoscale_max_replicas.')
            if autoscale_refresh_seconds and autoscale_refresh_seconds <= 0:
                raise WebserviceException('Error, autoscale_refresh_seconds must be greater than '
                                          'zero.')
            if autoscale_target_utilization and autoscale_target_utilization <= 0:
                raise WebserviceException('Error, autoscale_target_utilization must be greater '
                                          'than zero.')
        else:
            if autoscale_enabled is False and not num_replicas:
                raise WebserviceException('Error, autoscale disabled but num_replicas not provided.')
            if autoscale_min_replicas:
                raise WebserviceException('Error, autoscale_min_replicas provided without enabling '
                                          'autoscaling.')
            if autoscale_max_replicas:
                raise WebserviceException('Error, autoscale_max_replicas provided without enabling '
                                          'autoscaling.')
            if autoscale_refresh_seconds:
                raise WebserviceException('Error, autoscale_refresh_seconds provided without enabling '
                                          'autoscaling.')
            if autoscale_target_utilization:
                raise WebserviceException('Error, autoscale_target_utilization provided without '
                                          'enabling autoscaling.')

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
        self.update(tags=updated_properties)

        print('Image tag add operation complete.')

    def serialize(self):
        """
        Convert this Webservice into a json serialized dictionary.

        :return: The json representation of this Webservice
        :rtype: dict
        """
        properties = super(AksWebservice, self).serialize()
        autoscaler = self.autoscaler.serialize() if self.autoscaler else None
        container_resource_requirements = self.container_resource_requirements.serialize() \
            if self.container_resource_requirements else None
        data_collection = self.data_collection.serialize() if self.data_collection else None
        image = self.image.serialize() if self.image else None
        aks_properties = {'appInsightsEnabled': self.app_insights_enabled, 'authEnabled': self.auth_enabled,
                          'autoScaler': autoscaler, 'computeName': self.compute_name,
                          'containerResourceRequirements': container_resource_requirements,
                          'dataCollection': data_collection, 'imageId': self.image_id,
                          'imageDetails': image,
                          'maxConcurrentRequestsPerContainer': self.max_concurrent_requests_per_container,
                          'numReplicas': self.num_replicas, 'deploymentStatus': self.deployment_status,
                          'scoringTimeoutMs': self.scoring_timeout_ms, 'scoringUri': self.scoring_uri}
        properties.update(aks_properties)
        return properties

    @staticmethod
    def deserialize(workspace, webservice_payload):
        """
        Convert a json object into a AksWebservice object. Will fail if the provided workspace is not the workspace the
        Webservice is registered under.

        :param workspace: The workspace object the AksWebservice is registered under
        :type workspace: azureml.core.workspace.Workspace
        :param webservice_payload: A json object to convert to a Webservice object
        :type webservice_payload: dict
        :return: The AksWebservice representation of the provided json object
        :rtype: AksWebservice
        """
        AksWebservice._validate_get_payload(webservice_payload)
        webservice = AksWebservice(None, None)
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
            raise WebserviceException('Invalid payload for AKS webservice, missing computeType:\n'
                                      '{}'.format(payload))
        if payload['computeType'] != 'AKS':
            raise WebserviceException('Invalid payload for AKS webservice, computeType is not "AKS":\n'
                                      '{}'.format(payload))
        for payload_key in AksWebservice._expected_payload_keys:
            if payload_key not in payload:
                raise WebserviceException('Invalid webservice payload, missing {} for webservice:\n'
                                          '{}'.format(payload_key, payload))


class AutoScaler(object):
    """
    Class containing details for the autoscaler for AKS Webservices
    """
    _expected_payload_keys = ['autoscaleEnabled', 'maxReplicas', 'minReplicas', 'refreshPeriodInSeconds',
                              'targetUtilization']

    def __init__(self, autoscale_enabled, max_replicas, min_replicas, refresh_period_seconds, target_utilization):
        """
        Initialize the AKS AutoScaler

        :param autoscale_enabled: Whether the autoscaler is enabled or disabled
        :type autoscale_enabled: bool
        :param max_replicas: The maximum number of containers for the Autoscaler to use
        :type max_replicas: int
        :param min_replicas: The minimum number of containers for the Autoscaler to use
        :type min_replicas: int
        :param refresh_period_seconds: How often the autoscaler should attempt to scale the Webservice
        :type refresh_period_seconds: int
        :param target_utilization: The target utilization (in percent out of 100) the autoscaler should
            attempt to maintain for the Webservice
        :type target_utilization: int
        """
        self.autoscale_enabled = autoscale_enabled
        self.max_replicas = max_replicas
        self.min_replicas = min_replicas
        self.refresh_period_seconds = refresh_period_seconds
        self.target_utilization = target_utilization

    def serialize(self):
        """
        Convert this AutoScaler into a json serialized dictionary.

        :return: The json representation of this AutoScaler
        :rtype: dict
        """
        return {'autoscaleEnabled': self.autoscale_enabled, 'minReplicas': self.min_replicas,
                'maxReplicas': self.max_replicas, 'refreshPeriodInSeconds': self.refresh_period_seconds,
                'targetUtilization': self.target_utilization}

    @staticmethod
    def deserialize(payload_obj):
        """
        Convert a json object into a AutoScaler object.

        :param payload_obj: A json object to convert to a AutoScaler object
        :type payload_obj: dict
        :return: The AutoScaler representation of the provided json object
        :rtype: AutoScaler
        """
        for payload_key in AutoScaler._expected_payload_keys:
            if payload_key not in payload_obj:
                raise WebserviceException('Invalid webservice payload, missing {} for autoScaler:\n'
                                          '{}'.format(payload_key, payload_obj))

        return AutoScaler(payload_obj['autoscaleEnabled'], payload_obj['maxReplicas'], payload_obj['minReplicas'],
                          payload_obj['refreshPeriodInSeconds'], payload_obj['targetUtilization'])


class ContainerResourceRequirements(object):
    """
    Class containing details for the resource requirements for each container used by the Webservice
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
                raise WebserviceException('Invalid webservice payload, missing {} for ContainerResourceRequirements:\n'
                                          '{}'.format(payload_key, payload_obj))

        return ContainerResourceRequirements(payload_obj['cpu'], payload_obj['memoryInGB'])


class DataCollection(object):
    """
    Class for managing data collection for an AKS Webservice
    """
    _expected_payload_keys = ['eventHubEnabled', 'storageEnabled']

    def __init__(self, event_hub_enabled, storage_enabled):
        """
        Intialize the DataCollection object

        :param event_hub_enabled: Whether or not event hub is enabled for the Webservice
        :type event_hub_enabled: bool
        :param storage_enabled: Whether or not data collection storage is enabled for the Webservice
        :type storage_enabled: bool
        """
        self.event_hub_enabled = event_hub_enabled
        self.storage_enabled = storage_enabled

    def serialize(self):
        """
        Convert this DataCollection into a json serialized dictionary.

        :return: The json representation of this DataCollection
        :rtype: dict
        """
        return {'eventHubEnabled': self.event_hub_enabled, 'storageEnabled': self.storage_enabled}

    @staticmethod
    def deserialize(payload_obj):
        """
        Convert a json object into a DataCollection object.

        :param payload_obj: A json object to convert to a DataCollection object
        :type payload_obj: dict
        :return: The DataCollection representation of the provided json object
        :rtype: DataCollection
        """
        for payload_key in DataCollection._expected_payload_keys:
            if payload_key not in payload_obj:
                raise WebserviceException('Invalid webservice payload, missing {} for DataCollection:\n'
                                          '{}'.format(payload_key, payload_obj))

        return DataCollection(payload_obj['eventHubEnabled'], payload_obj['storageEnabled'])


class AksServiceDeploymentConfiguration(WebserviceDeploymentConfiguration):
    """
    Service deployment configuration object for services deployed on AKS compute.

    :param autoscale_enabled: Whether or not to enable autoscaling for this Webservice
    :type autoscale_enabled: bool
    :param autoscale_min_replicas: The minimum number of containers to use when autoscaling this Webservice
    :type autoscale_min_replicas: int
    :param autoscale_max_replicas: The maximum number of containers to use when autoscaling this Webservice
    :type autoscale_max_replicas: int
    :param autoscale_refresh_seconds: How often the autoscaler should attempt to scale this Webservice
    :type autoscale_refresh_seconds: int
    :param autoscale_target_utilization: The target utilization (in percent out of 100) the autoscaler should
        attempt to maintain for this Webservice
    :type autoscale_target_utilization: int
    :param collect_model_data: Whether or not to enable model data collection for this Webservice
    :type collect_model_data: bool
    :param auth_enabled: Whether or not to enable auth for this Webservice
    :type auth_enabled: bool
    :param cpu_cores: The number of cpu cores to allocate for this Webservice. Can be a decimal
    :type cpu_cores: float
    :param memory_gb: The amount of memory (in GB) to allocate for this Webservice. Can be a decimal
    :type memory_gb: float
    :param enable_app_insights: Whether or not to enable Application Insights logging for this Webservice
    :type enable_app_insights: bool
    :param scoring_timeout_ms: A timeout to enforce for scoring calls to this Webservice
    :type scoring_timeout_ms: int
    :param replica_max_concurrent_requests: The number of maximum concurrent requests per node to allow for this
        Webservice
    :type replica_max_concurrent_requests: int
    :param num_replicas: The number of containers to allocate for this Webservice
    :type num_replicas: int
    :param primary_key: A primary auth key to use for this Webservice
    :type primary_key: str
    :param secondary_key: A secondary auth key to use for this Webservice
    :type secondary_key: str
    :param tags: Dictionary of key value tags to give this Webservice
    :type tags: dict[str, str]
    :param properties: Dictionary of key value properties to give this Webservice. These properties cannot
        be changed after deployment, however new key value pairs can be added
    :type properties: dict[str, str]
    :param description: A description to give this Webservice
    :type description: str
    """

    def __init__(self, autoscale_enabled, autoscale_min_replicas, autoscale_max_replicas, autoscale_refresh_seconds,
                 autoscale_target_utilization, collect_model_data, auth_enabled, cpu_cores, memory_gb,
                 enable_app_insights, scoring_timeout_ms, replica_max_concurrent_requests, num_replicas, primary_key,
                 secondary_key, tags, properties, description):
        """
        Initialize a configuration object for deploying to an AKS compute target

        :param autoscale_enabled: Whether or not to enable autoscaling for this Webservice
        :type autoscale_enabled: bool
        :param autoscale_min_replicas: The minimum number of containers to use when autoscaling this Webservice
        :type autoscale_min_replicas: int
        :param autoscale_max_replicas: The maximum number of containers to use when autoscaling this Webservice
        :type autoscale_max_replicas: int
        :param autoscale_refresh_seconds: How often the autoscaler should attempt to scale this Webservice
        :type autoscale_refresh_seconds: int
        :param autoscale_target_utilization: The target utilization (in percent out of 100) the autoscaler should
            attempt to maintain for this Webservice
        :type autoscale_target_utilization: int
        :param collect_model_data: Whether or not to enable model data collection for this Webservice
        :type collect_model_data: bool
        :param auth_enabled: Whether or not to enable auth for this Webservice
        :type auth_enabled: bool
        :param cpu_cores: The number of cpu cores to allocate for this Webservice. Can be a decimal
        :type cpu_cores: float
        :param memory_gb: The amount of memory (in GB) to allocate for this Webservice. Can be a decimal
        :type memory_gb: float
        :param enable_app_insights: Whether or not to enable Application Insights logging for this Webservice
        :type enable_app_insights: bool
        :param scoring_timeout_ms: A timeout to enforce for scoring calls to this Webservice
        :type scoring_timeout_ms: int
        :param replica_max_concurrent_requests: The number of maximum concurrent requests per node to allow for this
            Webservice
        :type replica_max_concurrent_requests: int
        :param num_replicas: The number of containers to allocate for this Webservice
        :type num_replicas: int
        :param primary_key: A primary auth key to use for this Webservice
        :type primary_key: str
        :param secondary_key: A secondary auth key to use for this Webservice
        :type secondary_key: str
        :param tags: Dictionary of key value tags to give this Webservice
        :type tags: dict[str, str]
        :param properties: Dictionary of key value properties to give this Webservice. These properties cannot
            be changed after deployment, however new key value pairs can be added
        :type properties: dict[str, str]
        :param description: A description to give this Webservice
        :type description: str
        :raises: WebserviceException
        """
        super(AksServiceDeploymentConfiguration, self).__init__(AksWebservice)
        self.autoscale_enabled = autoscale_enabled
        self.autoscale_min_replicas = autoscale_min_replicas
        self.autoscale_max_replicas = autoscale_max_replicas
        self.autoscale_refresh_seconds = autoscale_refresh_seconds
        self.autoscale_target_utilization = autoscale_target_utilization
        self.collect_model_data = collect_model_data
        self.auth_enabled = auth_enabled
        self.cpu_cores = cpu_cores
        self.memory_gb = memory_gb
        self.enable_app_insights = enable_app_insights
        self.scoring_timeout_ms = scoring_timeout_ms
        self.replica_max_concurrent_requests = replica_max_concurrent_requests
        self.num_replicas = num_replicas
        self.primary_key = primary_key
        self.secondary_key = secondary_key
        self.tags = tags
        self.properties = properties
        self.description = description
        self.validate_configuration()

    def validate_configuration(self):
        """
        Checks that the specified configuration values are valid. Will raise a WebserviceException if validation
        fails.

        :raises: WebserviceException
        """
        if self.cpu_cores and self.cpu_cores <= 0:
            raise WebserviceException('Invalid configuration, cpu_cores must be greater than zero.')
        if self.memory_gb and self.memory_gb <= 0:
            raise WebserviceException('Invalid configuration, memory_gb must be greater than zero.')
        if self.scoring_timeout_ms and self.scoring_timeout_ms <= 0:
            raise WebserviceException('Invalid configuration, scoring_timeout_ms must be greater than zero.')
        if self.replica_max_concurrent_requests and self.replica_max_concurrent_requests <= 0:
            raise WebserviceException('Invalid configuration, replica_max_concurrent_requests must be greater than '
                                      'zero.')
        if self.num_replicas and self.num_replicas <= 0:
            raise WebserviceException('Invalid configuration, num_replicas must be greater than zero.')
        if self.autoscale_enabled:
            if self.num_replicas:
                raise WebserviceException('Invalid configuration, autoscale enabled and num_replicas provided.')
            if self.autoscale_min_replicas and self.autoscale_min_replicas <= 0:
                raise WebserviceException('Invalid configuration, autoscale_min_replicas must be greater than '
                                          'zero.')
            if self.autoscale_max_replicas and self.autoscale_max_replicas <= 0:
                raise WebserviceException('Invalid configuration, autoscale_max_replicas must be greater than '
                                          'zero.')
            if self.autoscale_min_replicas and self.autoscale_max_replicas and \
                    self.autoscale_min_replicas > self.autoscale_max_replicas:
                raise WebserviceException('Invalid configuration, autoscale_min_replicas cannot be greater than '
                                          'autoscale_max_replicas.')
            if self.autoscale_refresh_seconds and self.autoscale_refresh_seconds <= 0:
                raise WebserviceException('Invalid configuration, autoscale_refresh_seconds must be greater than '
                                          'zero.')
            if self.autoscale_target_utilization and self.autoscale_target_utilization <= 0:
                raise WebserviceException('Invalid configuration, autoscale_target_utilization must be greater '
                                          'than zero.')
        else:
            if self.autoscale_enabled is False and not self.num_replicas:
                raise WebserviceException('Invalid configuration, autoscale disabled but num_replicas not provided.')
            if self.autoscale_min_replicas:
                raise WebserviceException('Invalid configuration, autoscale_min_replicas provided without enabling '
                                          'autoscaling.')
            if self.autoscale_max_replicas:
                raise WebserviceException('Invalid configuration, autoscale_max_replicas provided without enabling '
                                          'autoscaling.')
            if self.autoscale_refresh_seconds:
                raise WebserviceException('Invalid configuration, autoscale_refresh_seconds provided without enabling '
                                          'autoscaling.')
            if self.autoscale_target_utilization:
                raise WebserviceException('Invalid configuration, autoscale_target_utilization provided without '
                                          'enabling autoscaling.')
