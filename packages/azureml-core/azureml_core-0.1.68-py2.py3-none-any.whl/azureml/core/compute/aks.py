# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Module for managing AKS Compute Targets in Azure ML"""

import copy
import json
import requests
import traceback
from azureml._compute._constants import MLC_COMPUTE_RESOURCE_ID_FMT
from azureml._compute._constants import MLC_ENDPOINT_FMT
from azureml._compute._constants import MLC_WORKSPACE_API_VERSION
from azureml._compute._util import aks_payload_template
from azureml.core.compute import ComputeTarget
from azureml.core.compute.compute import ComputeTargetProvisioningConfiguration
from azureml.exceptions import ComputeTargetException


class AksCompute(ComputeTarget):
    """
    Class for managing AKS target objects.
    """
    _compute_type = 'AKS'

    def _initialize(self, workspace, obj_dict):
        """

        :param workspace:
        :type workspace: azureml.core.workspace.Workspace
        :param obj_dict:
        :type obj_dict: dict
        :return:
        :rtype: None
        """
        name = obj_dict['id']
        compute_resource_id = MLC_COMPUTE_RESOURCE_ID_FMT.format(workspace.subscription_id,
                                                                 workspace.resource_group, workspace.name,
                                                                 name)
        mlc_endpoint = MLC_ENDPOINT_FMT.format(workspace.subscription_id, workspace.resource_group,
                                               workspace.name, name)
        location = obj_dict['location']
        compute_type = obj_dict['properties']['computeType']
        tags = obj_dict['tags']
        description = obj_dict['properties']['description']
        created_on = None
        modified_on = None
        cluster_resource_id = obj_dict['properties']['resourceId']
        cluster_location = obj_dict['properties']['computeLocation'] \
            if 'computeLocation' in obj_dict['properties'] else None
        provisioning_state = obj_dict['properties']['provisioningState']
        provisioning_errors = obj_dict['properties']['provisioningErrors']
        aks_properties = obj_dict['properties']['properties']
        agent_vm_size = aks_properties['agentVmSize'] if aks_properties else None
        agent_count = aks_properties['agentCount'] if aks_properties else None
        cluster_fqdn = aks_properties['clusterFqdn'] if aks_properties else None
        system_services = aks_properties['systemServices'] if aks_properties else None
        if system_services:
            system_services = [SystemService.deserialize(service) for service in system_services]
        ssl_configuration = aks_properties['sslConfiguration'] \
            if aks_properties and 'sslConfiguration' in aks_properties else None
        if ssl_configuration:
            ssl_configuration = SslConfiguration.deserialize(ssl_configuration)
        super(AksCompute, self)._initialize(compute_resource_id, name, location, compute_type, tags, description,
                                            created_on, modified_on, provisioning_state, provisioning_errors,
                                            cluster_resource_id, cluster_location, workspace, mlc_endpoint, None,
                                            workspace._auth)
        self.agent_vm_size = agent_vm_size
        self.agent_count = agent_count
        self.cluster_fqdn = cluster_fqdn
        self.system_services = system_services
        self.ssl_configuration = ssl_configuration

    @staticmethod
    def _create(workspace, name, provisioning_configuration):
        """

        :param workspace:
        :type workspace: azureml.core.workspace.Workspace
        :param name:
        :type name: str
        :param provisioning_configuration:
        :type provisioning_configuration: AksProvisioningConfiguration
        :return:
        :rtype: AksCompute
        """
        compute_create_payload = AksCompute._build_create_payload(provisioning_configuration, workspace.location)
        return ComputeTarget._create_compute_target(workspace, name, compute_create_payload, AksCompute)

    @staticmethod
    def attach(workspace, name, resource_id):
        """
        Associates an already existing AKS compute resource with the provided workspace.

        :param workspace: The workspace object to associate the compute resource with
        :type workspace: azureml.core.workspace.Workspace
        :param name: The name to associate with the compute resource inside the provided workspace. Does not have to
            match with the already given name of the compute resource
        :type name: str
        :param resource_id: The Azure resource ID for the compute resource to attach
        :type resource_id: str
        :return: An AksCompute object representation of the compute object
        :rtype: AksCompute
        :raises: ComputeTargetException
        """
        resource_parts = resource_id.split('/')
        if len(resource_parts) != 9:
            raise ComputeTargetException('Invalid resource ID provided: {}'.format(resource_id))
        resource_type = resource_parts[6]
        if resource_type != 'Microsoft.ContainerService':
            raise ComputeTargetException('Invalid resource ID provided, resource type {} does not match for AKS '
                                         'compute.'.format(resource_type))
        attach_payload = AksCompute._build_attach_payload(resource_id)
        return ComputeTarget._attach(workspace, name, attach_payload, AksCompute)

    @staticmethod
    def provisioning_configuration(agent_count=None, vm_size=None, ssl_cname=None, ssl_cert_pem_file=None,
                                   ssl_key_pem_file=None, location=None):
        """
        Create a configuration object for provisioning an AKS compute target

        :param agent_count: Number of agents (VMs) to host containers
        :type agent_count: int
        :param vm_size: Size of agent VMs. A full list of options can be found here: https://aka.ms/azureml-aks-details
        :type vm_size: str
        :param ssl_cname: A CName to use if enabling SSL validation on the cluster. Must provide all three
            CName, cert file, and key file to enable SSL validation
        :type ssl_cname: str
        :param ssl_cert_pem_file: A file path to a file containing cert information for SSL validation. Must provide
            all three CName, cert file, and key file to enable SSL validation
        :type ssl_cert_pem_file: str
        :param ssl_key_pem_file: A file path to a file containing key information for SSL validation. Must provide
            all three CName, cert file, and key file to enable SSL validation
        :type ssl_key_pem_file: str
        :param location: Location to provision cluster in. If not specified, will default to workspace location.
            Available regions for this compute can be found here:
            https://azure.microsoft.com/en-us/global-infrastructure/services/?regions=all&products=kubernetes-service
        :type location: str
        :return: A configuration object to be used when creating a Compute object
        :rtype: AksProvisioningConfiguration
        :raises: ComputeTargetException
        """
        config = AksProvisioningConfiguration(agent_count, vm_size, ssl_cname, ssl_cert_pem_file, ssl_key_pem_file,
                                              location)
        return config

    @staticmethod
    def _build_create_payload(config, location):
        """
        Construct the payload needed to create an AKS cluster

        :param config:
        :type config: AksProvisioningConfiguration
        :param location:
        :type location:
        :return:
        :rtype: dict
        """
        json_payload = copy.deepcopy(aks_payload_template)
        del(json_payload['properties']['resourceId'])
        json_payload['location'] = location
        if not config.agent_count and not config.vm_size and not config.ssl_cname:
            del(json_payload['properties']['properties'])
        else:
            if config.agent_count:
                json_payload['properties']['properties']['agentCount'] = config.agent_count
            else:
                del(json_payload['properties']['properties']['agentCount'])
            if config.vm_size:
                json_payload['properties']['properties']['agentVmSize'] = config.vm_size
            else:
                del(json_payload['properties']['properties']['agentVmSize'])
            if config.ssl_cname:
                try:
                    with open(config.ssl_cert_pem_file, 'r') as cert_file:
                        cert_data = cert_file.read()
                    with open(config.ssl_key_pem_file, 'r') as key_file:
                        key_data = key_file.read()
                except (IOError, OSError) as exc:
                    raise ComputeTargetException("Error while reading ssl information:\n"
                                                 "{}".format(traceback.format_exc().splitlines()[-1]))
                json_payload['properties']['properties']['sslConfiguration']['cname'] = config.ssl_cname
                json_payload['properties']['properties']['sslConfiguration']['cert'] = cert_data
                json_payload['properties']['properties']['sslConfiguration']['key'] = key_data
            else:
                del(json_payload['properties']['properties']['sslConfiguration'])
        if config.location:
            json_payload['properties']['computeLocation'] = config.location
        else:
            del(json_payload['properties']['computeLocation'])
        return json_payload

    @staticmethod
    def _build_attach_payload(resource_id):
        """

        :param resource_id:
        :type resource_id: str
        :return:
        :rtype: dict
        """
        json_payload = copy.deepcopy(aks_payload_template)
        json_payload['properties']['resourceId'] = resource_id
        del (json_payload['properties']['computeLocation'])
        del(json_payload['properties']['properties'])
        return json_payload

    def refresh_state(self):
        """
        Perform an in-place update of the properties of the object based on the current state of the
        corresponding cloud object. Primarily useful for manual polling of compute state.
        """
        cluster = AksCompute(self.workspace, self.name)
        self.modified_on = cluster.modified_on
        self.provisioning_state = cluster.provisioning_state
        self.provisioning_errors = cluster.provisioning_errors
        self.cluster_resource_id = cluster.cluster_resource_id
        self.cluster_location = cluster.cluster_location
        self.agent_vm_size = cluster.agent_vm_size
        self.agent_count = cluster.agent_count
        self.cluster_fqdn = cluster.cluster_fqdn
        self.system_services = cluster.system_services
        self.ssl_configuration = cluster.ssl_configuration

    def delete(self):
        """
        Removes the AksCompute object from its associated workspace. If this object was created through Azure ML, the
        corresponding cloud based objects will also be deleted. If this object was created externally and only
        attached to the workspace, no underlying cloud object will be deleted, the association will just be removed.

        :raises: ComputeTargetException
        """
        headers = self._auth.get_authentication_header()
        params = {'api-version': MLC_WORKSPACE_API_VERSION}
        resp = requests.delete(self._mlc_endpoint, params=params, headers=headers)

        try:
            resp.raise_for_status()
        except requests.exceptions.HTTPError:
            raise ComputeTargetException('Received bad response from Resource Provider:\n'
                                         'Response Code: {}\n'
                                         'Headers: {}\n'
                                         'Content: {}'.format(resp.status_code, resp.headers, resp.content))

        self.provisioning_state = 'Deleting'

    def get_credentials(self):
        """
        Retrieve the credentials for the AKS target

        :return: Credentials for the AKS target
        :rtype: dict
        :raises: ComputeTargetException
        """
        endpoint = self._mlc_endpoint + '/listKeys'
        headers = self._auth.get_authentication_header()
        params = {'api-version': MLC_WORKSPACE_API_VERSION}
        resp = requests.post(endpoint, params=params, headers=headers)

        try:
            resp.raise_for_status()
        except requests.exceptions.HTTPError:
            raise ComputeTargetException('Received bad response from Resource Provider:\n'
                                         'Response Code: {}\n'
                                         'Headers: {}\n'
                                         'Content: {}'.format(resp.status_code, resp.headers, resp.content))
        content = resp.content
        if isinstance(content, bytes):
            content = content.decode('utf-8')
        creds_content = json.loads(content)
        return creds_content

    def serialize(self):
        """
        Convert this AksCompute object into a json serialized dictionary.

        :return: The json representation of this AksCompute object
        :rtype: dict
        """
        system_services = [system_service.serialize() for system_service in self.system_services] \
            if self.system_services else None

        ssl_configuration = self.ssl_configuration.serialize() if self.ssl_configuration else None

        aks_properties = {'agentVmSize': self.agent_vm_size, 'agentCount': self.agent_count,
                          'clusterFqdn': self.cluster_fqdn, 'systemServices': system_services,
                          'sslConfiguration': ssl_configuration}

        cluster_properties = {'computeType': 'AKS', 'computeLocation': self.cluster_location,
                              'description': self.description, 'resourceId': self.cluster_resource_id,
                              'provisioningState': self.provisioning_state,
                              'provisioningErrors': self.provisioning_errors, 'properties': aks_properties}

        return {'id': self.id, 'name': self.name, 'tags': self.tags, 'location': self.location,
                'properties': cluster_properties}

    @staticmethod
    def deserialize(workspace, object_dict):
        """
        Convert a json object into a AksCompute object. Will fail if the provided workspace is not the workspace the
        Compute is associated with.

        :param workspace: The workspace object the AksCompute object is associated with
        :type workspace: azureml.core.workspace.Workspace
        :param object_dict: A json object to convert to a AksCompute object
        :type object_dict: dict
        :return: The AksCompute representation of the provided json object
        :rtype: AksCompute
        :raises: ComputeTargetException
        """
        AksCompute._validate_get_payload(object_dict)
        target = AksCompute(None, None)
        target._initialize(workspace, object_dict)
        return target

    @staticmethod
    def _validate_get_payload(payload):
        """

        :param payload:
        :type payload: dict
        :return:
        :rtype: None
        """
        if 'properties' not in payload or 'computeType' not in payload['properties']:
            raise ComputeTargetException('Invalid cluster payload:\n'
                                         '{}'.format(payload))
        if payload['properties']['computeType'] != AksCompute._compute_type:
            raise ComputeTargetException('Invalid cluster payload, not "{}":\n'
                                         '{}'.format(AksCompute._compute_type, payload))
        for arm_key in ['location', 'id', 'tags']:
            if arm_key not in payload:
                raise ComputeTargetException('Invalid cluster payload, missing ["{}"]:\n'
                                             '{}'.format(arm_key, payload))
        for key in ['properties', 'provisioningErrors', 'description', 'provisioningState', 'resourceId']:
            if key not in payload['properties']:
                raise ComputeTargetException('Invalid cluster payload, missing ["properties"]["{}"]:\n'
                                             '{}'.format(key, payload))
        aks_properties = payload['properties']['properties']
        if aks_properties:
            for aks_key in ['agentVmSize', 'agentCount', 'clusterFqdn', 'systemServices']:
                if aks_key not in aks_properties:
                    raise ComputeTargetException('Invalid cluster payload, missing '
                                                 '["properties"]["properties"]["{}"]:\n'
                                                 '{}'.format(aks_key, payload))


class AksProvisioningConfiguration(ComputeTargetProvisioningConfiguration):
    """
    Provisioning configuration object for AKS compute targets. This objects is used to
    define the configuration parameters for provisioning AksCompute objects.

    :param agent_count: Number of agents (VMs) to host containers
    :type agent_count: int
    :param vm_size: Size of agent VMs. A full list of options can be found here: https://aka.ms/azureml-aks-details
    :type vm_size: str
    :param ssl_cname: A CName to use if enabling SSL validation on the cluster. Must provide all three
        CName, cert file, and key file to enable SSL validation
    :type ssl_cname: str
    :param ssl_cert_pem_file: A file path to a file containing cert information for SSL validation. Must provide
        all three CName, cert file, and key file to enable SSL validation
    :type ssl_cert_pem_file: str
    :param ssl_key_pem_file: A file path to a file containing key information for SSL validation. Must provide
        all three CName, cert file, and key file to enable SSL validation
    :type ssl_key_pem_file: str
    :param location: Location to provision cluster in. If not specified, will default to workspace location.
        Available regions for this compute can be found here:
        https://azure.microsoft.com/en-us/global-infrastructure/services/?regions=all&products=kubernetes-service
    :type location: str
    """
    def __init__(self, agent_count, vm_size, ssl_cname, ssl_cert_pem_file, ssl_key_pem_file, location):
        """
        Initialize a configuration object for provisioning an AKS compute target

        :param agent_count: Number of agents (VMs) to host containers
        :type agent_count: int
        :param vm_size: Size of agent VMs. A full list of options can be found here: https://aka.ms/azureml-aks-details
        :type vm_size: str
        :param ssl_cname: A CName to use if enabling SSL validation on the cluster. Must provide all three
            CName, cert file, and key file to enable SSL validation
        :type ssl_cname: str
        :param ssl_cert_pem_file: A file path to a file containing cert information for SSL validation. Must provide
            all three CName, cert file, and key file to enable SSL validation
        :type ssl_cert_pem_file: str
        :param ssl_key_pem_file: A file path to a file containing key information for SSL validation. Must provide
            all three CName, cert file, and key file to enable SSL validation
        :type ssl_key_pem_file: str
        :param location: Location to provision cluster in. If not specified, will default to workspace location.
            Available regions for this compute can be found here:
            https://azure.microsoft.com/en-us/global-infrastructure/services/?regions=all&products=kubernetes-service
        :type location: str
        :return: A configuration object to be used when creating a Compute object
        :rtype: AksProvisioningConfiguration
        :raises: ComputeTargetException
        """
        super(AksProvisioningConfiguration, self).__init__(AksCompute, location)
        self.agent_count = agent_count
        self.vm_size = vm_size
        self.ssl_cname = ssl_cname
        self.ssl_cert_pem_file = ssl_cert_pem_file
        self.ssl_key_pem_file = ssl_key_pem_file
        self.validate_configuration()

    def validate_configuration(self):
        """
        Checks that the specified configuration values are valid. Will raise a ComputeTargetException if validation
        fails.

        :raises: ComputeTargetException
        """
        if self.agent_count and self.agent_count <= 0:
            raise ComputeTargetException('Invalid configuration, agent count must be a positive integer.')
        if self.ssl_cname or self.ssl_cert_pem_file or self.ssl_key_pem_file:
            if not self.ssl_cname or not self.ssl_cert_pem_file or not self.ssl_key_pem_file:
                raise ComputeTargetException('Invalid configuration, not all ssl information provided. To enable SSL '
                                             'validation please provide the cname, cert pem file, and key pem file.')


class SystemService(object):
    """
    AKS System Service object
    """
    def __init__(self, service_type, version, public_ip_address):
        """
        Initialize the System Service object

        :param service_type: The underlying type associated with this service
        :type service_type: str
        :param version: Service version
        :type version: str
        :param public_ip_address: Accessible IP address for this service
        :type public_ip_address: str
        """
        self.service_type = service_type
        self.version = version
        self.public_ip_address = public_ip_address

    def serialize(self):
        """
        Convert this SystemService object into a json serialized dictionary.

        :return: The json representation of this SystemService object
        :rtype: dict
        """
        return {'serviceType': self.service_type, 'version': self.version, 'publicIpAddress': self.public_ip_address}

    @staticmethod
    def deserialize(object_dict):
        """
        Convert a json object into a SystemService object

        :param object_dict: A json object to convert to a SystemService object
        :type object_dict: dict
        :return: The SystemService representation of the provided json object
        :rtype: SystemService
        :raises: ComputeTargetException
        """
        for service_key in ['systemServiceType', 'version', 'publicIpAddress']:
            if service_key not in object_dict:
                raise ComputeTargetException('Invalid system service payload, missing "{}":\n'
                                             '{}'.format(service_key, object_dict))
        return SystemService(object_dict['systemServiceType'], object_dict['version'], object_dict['publicIpAddress'])


class SslConfiguration(object):
    """
    AKS SSL Configuration object
    """
    def __init__(self, status, cert, key, cname):
        """
        Initialize the SslConfiguration object

        :param status: Whether SSL validation is enabled or disabled
        :type status: str
        :param cert: Cert string used for SSL validation
        :type cert: str
        :param key: Key string used for SSL validation
        :type key: str
        :param cname: CName used for SSL validation
        :type cname: str
        """
        self.status = status
        self.cert = cert
        self.key = key
        self.cname = cname

    def serialize(self):
        """
        Convert this SslConfiguration object into a json serialized dictionary.

        :return: The json representation of this SslConfiguration object
        :rtype: dict
        """
        return {'status': self.status, 'cert': self.cert, 'key': self.key, 'cname': self.cname}

    @staticmethod
    def deserialize(object_dict):
        """
        Convert a json object into a SslConfiguration object

        :param object_dict: A json object to convert to a SslConfiguration object
        :type object_dict: dict
        :return: The SslConfiguration representation of the provided json object
        :rtype: SslConfiguration
        :raises: ComputeTargetException
        """
        status = object_dict.get('status', None)
        cert = object_dict.get('cert', None)
        key = object_dict.get('key', None)
        cname = object_dict.get('cname', None)
        return SslConfiguration(status, cert, key, cname)
