# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Module for managing Datafactory Compute Targets in Azure ML"""

import copy
import requests
from azureml._compute._constants import MLC_COMPUTE_RESOURCE_ID_FMT
from azureml._compute._constants import MLC_ENDPOINT_FMT
from azureml._compute._constants import MLC_WORKSPACE_API_VERSION
from azureml._compute._util import datafactory_payload_template
from azureml.core.compute import ComputeTarget
from azureml.core.compute.compute import ComputeTargetProvisioningConfiguration
from azureml.exceptions import ComputeTargetException


class DataFactoryCompute(ComputeTarget):
    """
    Class for managing DataFactory target objects.
    """
    _compute_type = 'DataFactory'

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
        compute_resource_id = MLC_COMPUTE_RESOURCE_ID_FMT.format(workspace.subscription_id, workspace.resource_group,
                                                                 workspace.name, name)
        mlc_endpoint = MLC_ENDPOINT_FMT.format(workspace.subscription_id, workspace.resource_group, workspace.name,
                                               name)
        location = obj_dict['location']
        compute_type = obj_dict['properties']['computeType']
        tags = obj_dict['tags']
        description = obj_dict['properties']['description']
        created_on = None
        modified_on = None
        cluster_resource_id = obj_dict['properties']['resourceId']
        cluster_location = obj_dict['properties']['computeLocation'] \
            if 'computeLocation' in obj_dict['properties'] else location
        provisioning_state = obj_dict['properties']['provisioningState']
        provisioning_errors = obj_dict['properties']['provisioningErrors']
        super(DataFactoryCompute, self)._initialize(compute_resource_id, name, location, compute_type, tags,
                                                    description, created_on, modified_on, provisioning_state,
                                                    provisioning_errors, cluster_resource_id, cluster_location,
                                                    workspace, mlc_endpoint, None, workspace._auth)

    @staticmethod
    def _create(workspace, name, provisioning_configuration):
        """

        :param workspace:
        :type workspace: azureml.core.workspace.Workspace
        :param name:
        :type name: str
        :param provisioning_configuration:
        :type provisioning_configuration: DataFactoryProvisioningConfiguration
        :return:
        :rtype: DataFactoryCompute
        """
        create_payload = DataFactoryCompute._build_create_payload(provisioning_configuration, workspace.location)
        return ComputeTarget._create_compute_target(workspace, name, create_payload, DataFactoryCompute)

    @staticmethod
    def attach(workspace, name, resource_id):
        """
        Associates an already existing Databricks compute resource with the provided workspace.

        :param workspace: The workspace object to associate the compute resource with
        :type workspace: azureml.core.workspace.Workspace
        :param name: The name to associate with the compute resource inside the provided workspace. Does not have to
            match with the already given name of the compute resource
        :type name: str
        :param resource_id: The Azure resource ID for the compute resource to attach
        :type resource_id: str
        :return: A DataFactoryCompute object representation of the compute object
        :rtype: DataFactoryCompute
        :raises: ComputeTargetException
        """
        resource_parts = resource_id.split('/')
        if len(resource_parts) != 9:
            raise ComputeTargetException('Invalid resource ID provided: {}'.format(resource_id))
        resource_type = resource_parts[6]
        if resource_type != 'Microsoft.DataFactory':
            raise ComputeTargetException('Invalid resource ID provided, resource type {} does not match for '
                                         'DataFactory'.format(resource_type))
        attach_payload = DataFactoryCompute._build_attach_payload(resource_id)
        return ComputeTarget._attach(workspace, name, attach_payload, DataFactoryCompute)

    @staticmethod
    def provisioning_configuration(location=None):
        """
        Create a configuration object for provisioning a DataFactory compute target

        :param location: Location to provision cluster in. If not specified, will default to workspace location.
            Available regions for this compute can be found here:
            https://azure.microsoft.com/en-us/global-infrastructure/services/?regions=all&products=data-factory
        :type location: str
        :return: A configuration object to be used when creating a Compute object
        :rtype: DataFactoryProvisioningConfiguration
        :raises: ComputeTargetException
        """
        config = DataFactoryProvisioningConfiguration(location)
        return config

    @staticmethod
    def _build_create_payload(config, location):
        """
        Construct the payload needed to create a DataFactory

        :param config:
        :type config: azureml.core.compute.DataFactoryProvisioningConfiguration
        :param location:
        :type location: str
        :return:
        :rtype: dict
        """
        json_payload = copy.deepcopy(datafactory_payload_template)
        json_payload['location'] = location
        del(json_payload['properties']['resourceId'])
        if config.location:
            json_payload['properties']['computeLocation'] = config.location
        else:
            del (json_payload['properties']['computeLocation'])
        return json_payload

    @staticmethod
    def _build_attach_payload(resource_id):
        """

        :param resource_id:
        :type resource_id: str
        :return:
        :rtype: dict
        """
        json_payload = copy.deepcopy(datafactory_payload_template)
        json_payload['properties']['resourceId'] = resource_id
        del (json_payload['properties']['computeLocation'])
        return json_payload

    def refresh_state(self):
        """
        Perform an in-place update of the properties of the object based on the current state of the
        corresponding cloud object. Primarily useful for manual polling of compute state.
        """
        cluster = DataFactoryCompute(self.workspace, self.name)
        self.modified_on = cluster.modified_on
        self.provisioning_state = cluster.provisioning_state
        self.provisioning_errors = cluster.provisioning_errors
        self.cluster_resource_id = cluster.cluster_resource_id
        self.cluster_location = cluster.cluster_location

    def delete(self):
        """
        Removes the Datafactory object from its associated workspace. If this object was created through Azure ML,
        the corresponding cloud based objects will also be deleted. If this object was created externally and only
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

    def serialize(self):
        """
        Convert this DataFactoryCompute object into a json serialized dictionary.

        :return: The json representation of this DataFactoryCompute object
        :rtype: dict
        """
        return {'id': self.id, 'name': self.name, 'tags': self.tags, 'location': self.location,
                'properties': {'computeType': 'DataFactory', 'computeLocation': self.cluster_location,
                               'description': self.description,
                               'resourceId': self.cluster_resource_id,
                               'provisioningErrors': self.provisioning_errors,
                               'provisioningState': self.provisioning_state}}

    @staticmethod
    def deserialize(workspace, object_dict):
        """
        Convert a json object into a DataFactoryCompute object. Will fail if the provided workspace is not the
        workspace the Compute is associated with.

        :param workspace: The workspace object the DataFactoryCompute object is associated with
        :type workspace: azureml.core.workspace.Workspace
        :param object_dict: A json object to convert to a DataFactoryCompute object
        :type object_dict: dict
        :return: The DataFactoryCompute representation of the provided json object
        :rtype: DataFactoryCompute
        :raises: ComputeTargetException
        """
        DataFactoryCompute._validate_get_payload(object_dict)
        target = DataFactoryCompute(None, None)
        target._initialize(workspace, object_dict)
        return target

    @staticmethod
    def _validate_get_payload(payload):
        if 'properties' not in payload or 'computeType' not in payload['properties']:
            raise ComputeTargetException('Invalid cluster payload:\n'
                                         '{}'.format(payload))
        if payload['properties']['computeType'] != DataFactoryCompute._compute_type:
            raise ComputeTargetException('Invalid cluster payload, not "{}":\n'
                                         '{}'.format(DataFactoryCompute._compute_type, payload))
        for arm_key in ['location', 'id', 'tags']:
            if arm_key not in payload:
                raise ComputeTargetException('Invalid cluster payload, missing ["{}"]:\n'
                                             '{}'.format(arm_key, payload))
        for key in ['properties', 'provisioningErrors', 'description', 'provisioningState', 'resourceId']:
            if key not in payload['properties']:
                raise ComputeTargetException('Invalid cluster payload, missing ["properties"]["{}"]:\n'
                                             '{}'.format(key, payload))


class DataFactoryProvisioningConfiguration(ComputeTargetProvisioningConfiguration):
    """
    Provisioning configuration object for DataFactory compute targets.

    :param location: Location to provision cluster in. If not specified, will default to workspace location.
        Available regions for this compute can be found here:
        https://azure.microsoft.com/en-us/global-infrastructure/services/?regions=all&products=data-factory
    :type location: str
    """
    def __init__(self, location):
        """
        Create a configuration object for provisioning a DataFactory compute target

        :param location: Location to provision cluster in. If not specified, will default to workspace location.
            Available regions for this compute can be found here:
            https://azure.microsoft.com/en-us/global-infrastructure/services/?regions=all&products=data-factory
        :type location: str
        """
        super(DataFactoryProvisioningConfiguration, self).__init__(DataFactoryCompute, location)
        self.validate_configuration()

    def validate_configuration(self):
        """
        Checks that the specified configuration values are valid. Will raise a ComputeTargetException if validation
        fails.

        :raises: ComputeTargetException
        """
        pass
