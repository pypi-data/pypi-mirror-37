# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Module for managing Batch AI Compute Targets in Azure ML"""

import copy
import requests
import sys
import time
from azureml._compute._constants import MLC_COMPUTE_RESOURCE_ID_FMT
from azureml._compute._constants import MLC_ENDPOINT_FMT
from azureml._compute._constants import MLC_WORKSPACE_API_VERSION
from azureml._compute._util import batchai_payload_template
from azureml.core.compute import ComputeTarget
from azureml.core.compute.compute import ComputeTargetProvisioningConfiguration
from azureml.exceptions import ComputeTargetException
from dateutil.parser import parse


class BatchAiCompute(ComputeTarget):
    """
    Class for managing BatchAI compute target objects.
    """
    _compute_type = 'BatchAI'

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
            if 'computeLocation' in obj_dict['properties'] else None
        provisioning_state = obj_dict['properties']['provisioningState']
        provisioning_errors = obj_dict['properties']['provisioningErrors']
        vm_size = obj_dict['properties']['properties']['vmSize'] \
            if obj_dict['properties']['properties'] else None
        vm_priority = obj_dict['properties']['properties']['vmPriority'] \
            if obj_dict['properties']['properties'] else None
        scale_settings = obj_dict['properties']['properties']['scaleSettings'] \
            if obj_dict['properties']['properties'] else None
        scale_settings = RequestedScaleSettings.deserialize(scale_settings) if scale_settings else None
        status = BatchAiStatus.deserialize(obj_dict['properties']['status']['detailedStatus']) \
            if 'status' in obj_dict['properties'] and 'detailedStatus' in obj_dict['properties']['status'] else None
        super(BatchAiCompute, self)._initialize(compute_resource_id, name, location, compute_type, tags, description,
                                                created_on, modified_on, provisioning_state, provisioning_errors,
                                                cluster_resource_id, cluster_location, workspace, mlc_endpoint, None,
                                                workspace._auth)
        self.vm_size = vm_size
        self.vm_priority = vm_priority
        self.scale_settings = scale_settings
        self.status = status

    @staticmethod
    def _create(workspace, name, provisioning_configuration):
        """

        :param workspace:
        :type workspace: azureml.core.workspace.Workspace
        :param name:
        :type name: str
        :param provisioning_configuration:
        :type provisioning_configuration: BatchAiProvisioningConfiguration
        :return:
        :rtype: BatchAiCompute
        """
        compute_create_payload = BatchAiCompute._build_create_payload(provisioning_configuration, workspace.location)
        return ComputeTarget._create_compute_target(workspace, name, compute_create_payload, BatchAiCompute)

    @staticmethod
    def attach(workspace, name, resource_id):
        """
        Associates an already existing BatchAi compute resource with the provided workspace.

        :param workspace: The workspace object to associate the compute resource with
        :type workspace: azureml.core.workspace.Workspace
        :param name: The name to associate with the compute resource inside the provided workspace. Does not have to
            match with the already given name of the compute resource
        :type name: str
        :param resource_id: The Azure resource ID for the compute resource to attach
        :type resource_id: str
        :return: A BatchAiCompute object representation of the compute object
        :rtype: BatchAiCompute
        :raises: ComputeTargetException
        """
        resource_parts = resource_id.split('/')
        # Check for both lengths for now while we are in a transition period between BatchAI versions
        if len(resource_parts) != 9 and len(resource_parts) != 11:
            raise ComputeTargetException('Invalid resource ID provided: {}'.format(resource_id))
        resource_type = resource_parts[6]
        if resource_type != 'Microsoft.BatchAI':
            raise ComputeTargetException('Invalid resource ID provided, resource type {} does not match for BatchAi '
                                         'compute.'.format(resource_type))
        attach_payload = BatchAiCompute._build_attach_payload(resource_id)
        return ComputeTarget._attach(workspace, name, attach_payload, BatchAiCompute)

    @staticmethod
    def provisioning_configuration(vm_size='', vm_priority='', autoscale_enabled=None, cluster_min_nodes=None,
                                   cluster_max_nodes=None, location=None, tags=None, description=None):
        """
        Create a configuration object for provisioning an AKS compute target

        :param vm_size: Size of agent VMs. More details can be found here: https://aka.ms/azureml-batchai-details
            and here: https://aka.ms/azureml-vm-details. Note that not all sizes are available in all regions, as
            detailed in the previous link.
        :type vm_size: str
        :param vm_priority: dedicated or lowpriority VMs.
        :type vm_priority: str
        :param autoscale_enabled: Whether or not to enable autoscaling on the cluster. If enabled, must provide min
            and max nodes as well. If explicitly set to False, min and max nodes must be equal and are used to provide
            manual setting for number of nodes.
        :type autoscale_enabled: bool
        :param cluster_min_nodes: Minimum number of nodes to use on the cluster.
        :type cluster_min_nodes: int
        :param cluster_max_nodes: Maximum number of nodes to use on the cluster
        :type cluster_max_nodes: int
        :param location: Location to provision cluster in. If not specified, will default to workspace location.
            Available regions for this compute can be found here:
            https://azure.microsoft.com/en-us/global-infrastructure/services/?regions=all&products=batch-ai
        :type location: str
        :param tags: A dictionary of key value tags to provide to the compute object
        :type tags: dict[str, str]
        :param description: A description to provide to the compute object
        :type description: str
        :return: A configuration object to be used when creating a Compute object
        :rtype: BatchAiProvisioningConfiguration
        :raises: ComputeTargetException
        """
        config = BatchAiProvisioningConfiguration(vm_size, vm_priority, autoscale_enabled, cluster_min_nodes,
                                                  cluster_max_nodes, location, tags, description)
        return config

    @staticmethod
    def _build_create_payload(config, location):
        """
        Construct the payload needed to create an BatchAI cluster

        :param config:
        :type config: azureml.core.compute.BatchAiProvisioningConfiguration
        :param location:
        :type location: str
        :return:
        :rtype: dict
        """
        json_payload = copy.deepcopy(batchai_payload_template)
        del(json_payload['properties']['resourceId'])
        json_payload['location'] = location
        if not config.vm_size and not config.vm_priority and config.scale_settings.autoscale_enabled is None:
            del(json_payload['properties']['properties'])
        else:
            if not config.vm_size:
                del(json_payload['properties']['properties']['vmSize'])
            else:
                json_payload['properties']['properties']['vmSize'] = config.vm_size
            if not config.vm_priority:
                del(json_payload['properties']['properties']['vmPriority'])
            else:
                json_payload['properties']['properties']['vmPriority'] = config.vm_priority
            if config.scale_settings.autoscale_enabled is None:
                del(json_payload['properties']['properties']['scaleSettings'])
            else:
                json_payload['properties']['properties']['scaleSettings'] = config.scale_settings.serialize()
        if config.location:
            json_payload['properties']['computeLocation'] = config.location
        else:
            del(json_payload['properties']['computeLocation'])
        if config.tags:
            json_payload['tags'] = config.tags
        else:
            del(json_payload['tags'])
        if config.description:
            json_payload['properties']['description'] = config.description
        else:
            del(json_payload['properties']['description'])
        return json_payload

    @staticmethod
    def _build_attach_payload(resource_id):
        """

        :param resource_id:
        :type resource_id: str
        :return:
        :rtype:
        """
        json_payload = copy.deepcopy(batchai_payload_template)
        json_payload['properties']['resourceId'] = resource_id
        del (json_payload['properties']['computeLocation'])
        del(json_payload['properties']['properties'])
        return json_payload

    def wait_for_completion(self, show_output=False, min_node_count=None, timeout_in_minutes=20):
        """
        Wait for the BatchAI cluster to finish provisioning. This can be configured to wait for a minimum number of
        nodes, and to timeout after a set period of time.

        :param show_output: Boolean to provide more verbose output
        :type show_output: bool
        :param min_node_count: Minimum number of nodes to wait for before considering provisioning to be complete. This
            doesn't have to equal the minimum number of nodes that the compute was provisioned with, however it should
            not be greater than that.
        :type min_node_count: int
        :param timeout_in_minutes: The duration in minutes to wait before considering provisioning to have failed.
        :type timeout_in_minutes: int
        :raises: ComputeTargetException
        """
        min_nodes_reached, timeout_reached, terminal_state_reached, status_errors_present = \
            self._wait_for_nodes(min_node_count, timeout_in_minutes, show_output)
        print('BatchAI wait for completion finished')
        if min_nodes_reached:
            print('Minimum number of nodes requested have been provisioned')
        elif timeout_reached:
            print('Wait timeout has been reached')
        elif terminal_state_reached:
            if self.status:
                state = self.status.provisioning_state.capitalize()
            else:
                state = self.provisioning_state.capitalize()
            print('Terminal state of "{}" has been reached'.format(state))
            if state == 'Failed':
                print('Provisioning errors: {}'.format(self.provisioning_errors))
        elif status_errors_present:
            if self.status:
                errors = self.status.errors
            else:
                errors = self.provisioning_errors
            print('There were errors reported from BatchAI:\n{}'.format(errors))

    def _wait_for_nodes(self, min_node_count, timeout_in_minutes, show_output):
        """

        :param min_node_count:
        :type min_node_count: int
        :param timeout_in_minutes:
        :type timeout_in_minutes: int
        :param show_output:
        :type show_output: bool
        :return:
        :rtype:
        """
        self.refresh_state()
        start_time = time.time()

        if self.status:
            current_state = self.status.provisioning_state
        else:
            current_state = self.provisioning_state
        if show_output and current_state:
            sys.stdout.write('{}'.format(current_state))
            sys.stdout.flush()

        min_nodes_reached = self._min_node_count_reached(min_node_count)
        timeout_reached = self._polling_timeout_reached(start_time, timeout_in_minutes)
        terminal_state_reached = self._terminal_state_reached()
        status_errors_present = self._status_errors_present()

        while not min_nodes_reached and not timeout_reached and not terminal_state_reached \
                and not status_errors_present:
            time.sleep(5)
            self.refresh_state()

            if self.status:
                state = self.status.provisioning_state
            else:
                state = None

            if show_output and state:
                if state != current_state:
                    if current_state is None:
                        sys.stdout.write('{}'.format(state))
                    else:
                        sys.stdout.write('\n{}'.format(state))
                    current_state = state
                elif state:
                    sys.stdout.write('.')
                sys.stdout.flush()

            min_nodes_reached = self._min_node_count_reached(min_node_count)
            timeout_reached = self._polling_timeout_reached(start_time, timeout_in_minutes)
            terminal_state_reached = self._terminal_state_reached()
            status_errors_present = self._status_errors_present()

        if show_output:
            sys.stdout.write('\n')
            sys.stdout.flush()

        return min_nodes_reached, timeout_reached, terminal_state_reached, status_errors_present

    def _min_node_count_reached(self, min_node_count):
        """

        :param min_node_count:
        :type min_node_count: int
        :return:
        :rtype: bool
        """
        if not min_node_count:
            if self.status and self.status.scale_settings:
                if self.status.scale_settings.manual:
                    min_node_count = self.status.scale_settings.manual.target_node_count
                elif self.status.scale_settings.auto_scale:
                    min_node_count = self.status.scale_settings.auto_scale.min_node_count
        if min_node_count is not None and self.status and self.status.current_node_count >= min_node_count:
            return True
        return False

    def _polling_timeout_reached(self, start_time, timeout_in_minutes):
        """

        :param start_time:
        :type start_time: datetime.datetime
        :param timeout_in_minutes:
        :type timeout_in_minutes: int
        :return:
        :rtype: bool
        """
        cur_time = time.time()
        if cur_time - start_time > timeout_in_minutes * 60:
            return True
        return False

    def _terminal_state_reached(self):
        """

        :param state:
        :type state: str
        :return:
        :rtype: bool
        """
        if self.status:
            state = self.status.provisioning_state.capitalize()
        else:
            state = self.provisioning_state.capitalize()
        if state == 'Failed' or state == 'Canceled':
            return True
        return False

    def _status_errors_present(self):
        """

        :return:
        :rtype:
        """
        if (self.status and self.status.errors) or self.provisioning_errors:
            return True
        return False

    def refresh_state(self):
        """
        Perform an in-place update of the properties of the object based on the current state of the
        corresponding cloud object. Primarily useful for manual polling of compute state.
        """
        cluster = BatchAiCompute(self.workspace, self.name)
        self.modified_on = cluster.modified_on
        self.provisioning_state = cluster.provisioning_state
        self.provisioning_errors = cluster.provisioning_errors
        self.cluster_resource_id = cluster.cluster_resource_id
        self.cluster_location = cluster.cluster_location
        self.vm_size = cluster.vm_size
        self.vm_priority = cluster.vm_priority
        self.scale_settings = cluster.scale_settings
        self.status = cluster.status

    def get_status(self):
        """
        Retrieves the current detailed status for the BatchAI cluster.

        :return: A detailed status object for the cluster
        :rtype: BatchAiStatus
        """
        self.refresh_state()
        return self.status

    def delete(self):
        """
        Removes the BatchAiCompute object from its associated workspace. If this object was created through Azure ML,
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
        Convert this BatchAiCompute object into a json serialized dictionary.

        :return: The json representation of this BatchAiCompute object
        :rtype: dict
        """
        scale_settings = self.scale_settings.serialize() if self.scale_settings else None
        batchai_properties = {'vmSize': self.vm_size, 'vmPriority': self.vm_priority, 'scaleSettings': scale_settings}
        batchai_status = self.status.serialize() if self.status else None
        cluster_properties = {'computeType': 'BatchAI', 'computeLocation': self.cluster_location,
                              'description': self.description, 'resourceId': self.cluster_resource_id,
                              'provisioningErrors': self.provisioning_errors,
                              'provisioningState': self.provisioning_state, 'properties': batchai_properties,
                              'status': batchai_status}
        return {'id': self.id, 'name': self.name, 'tags': self.tags, 'location': self.location,
                'properties': cluster_properties}

    @staticmethod
    def deserialize(workspace, object_dict):
        """
        Convert a json object into a BatchAiCompute object. Will fail if the provided workspace is not the workspace
        the Compute is associated with.

        :param workspace: The workspace object the BatchAiCompute object is associated with
        :type workspace: azureml.core.workspace.Workspace
        :param object_dict: A json object to convert to a BatchAiCompute object
        :type object_dict: dict
        :return: The BatchAiCompute representation of the provided json object
        :rtype: BatchAiCompute
        :raises: ComputeTargetException
        """
        BatchAiCompute._validate_get_payload(object_dict)
        target = BatchAiCompute(None, None)
        target._initialize(workspace, object_dict)
        return target

    @staticmethod
    def _validate_get_payload(payload):
        if 'properties' not in payload or 'computeType' not in payload['properties']:
            raise ComputeTargetException('Invalid cluster payload:\n'
                                         '{}'.format(payload))
        if payload['properties']['computeType'] != BatchAiCompute._compute_type:
            raise ComputeTargetException('Invalid cluster payload, not "{}":\n'
                                         '{}'.format(BatchAiCompute._compute_type, payload))
        for arm_key in ['location', 'id', 'tags']:
            if arm_key not in payload:
                raise ComputeTargetException('Invalid cluster payload, missing ["{}"]:\n'
                                             '{}'.format(arm_key, payload))
        for key in ['properties', 'provisioningErrors', 'description', 'provisioningState', 'resourceId']:
            if key not in payload['properties']:
                raise ComputeTargetException('Invalid cluster payload, missing ["properties"]["{}"]:\n'
                                             '{}'.format(key, payload))
        if payload['properties']['properties']:
            for batchai_key in ['vmPriority', 'vmSize', 'scaleSettings']:
                if batchai_key not in payload['properties']['properties']:
                    raise ComputeTargetException('Invalid cluster payload, missing '
                                                 '["properties"]["properties"]["{}"]:\n'
                                                 '{}'.format(batchai_key, payload))


class BatchAiProvisioningConfiguration(ComputeTargetProvisioningConfiguration):
    """
    Provisioning configuration object for BatchAi compute targets. This objects is used to
    define the configuration parameters for provisioning BatchAiCompute objects.

    :param vm_size: Size of agent VMs. More details can be found here: https://aka.ms/azureml-batchai-details
        and here: https://aka.ms/azureml-vm-details. Note that not all sizes are available in all regions, as
        detailed in the previous link.
    :type vm_size: str
    :param vm_priority: dedicated or lowpriority VMs.
    :type vm_priority: str
    :param autoscale_enabled: Whether or not to enable autoscaling on the cluster. If enabled, must provide min
        and max nodes as well. If explicitly set to False, min and max nodes must be equal and are used to provide
        manual setting for number of nodes.
    :type autoscale_enabled: bool
    :param autoscale_min_nodes: Minimum number of nodes to use on the cluster.
    :type autoscale_min_nodes: int
    :param autoscale_max_nodes: Maximum number of nodes to use on the cluster
    :type autoscale_max_nodes: int
    :param location: Location to provision cluster in. If not specified, will default to workspace location.
        Available regions for this compute can be found here:
        https://azure.microsoft.com/en-us/global-infrastructure/services/?regions=all&products=batch-ai
    :type location: str
    :param tags: A dictionary of key value tags to provide to the compute object
    :type tags: dict[str, str]
    :param description: A description to provide to the compute object
    :type description: str
    """
    def __init__(self, vm_size='', vm_priority='', autoscale_enabled=None, autoscale_min_nodes=None,
                 autoscale_max_nodes=None, location=None, tags=None, description=None):
        """
        Create a configuration object for provisioning a BatchAi compute target

        :param vm_size: Size of agent VMs. More details can be found here: https://aka.ms/azureml-batchai-details
            and here: https://aka.ms/azureml-vm-details. Note that not all sizes are available in all regions, as
            detailed in the previous link.
        :type vm_size: str
        :param vm_priority: dedicated or lowpriority VMs.
        :type vm_priority: str
        :param autoscale_enabled: Whether or not to enable autoscaling on the cluster. If enabled, must provide min
            and max nodes as well. If explicitly set to False, min and max nodes must be equal and are used to provide
            manual setting for number of nodes.
        :type autoscale_enabled: bool
        :param autoscale_min_nodes: Minimum number of nodes to use on the cluster.
        :type autoscale_min_nodes: int
        :param autoscale_max_nodes: Maximum number of nodes to use on the cluster
        :type autoscale_max_nodes: int
        :param location: Location to provision cluster in. If not specified, will default to workspace location.
            Available regions for this compute can be found here:
            https://azure.microsoft.com/en-us/global-infrastructure/services/?regions=all&products=batch-ai
        :type location: str
        :param tags: A dictionary of key value tags to provide to the compute object
        :type tags: dict[str, str]
        :param description: A description to provide to the compute object
        :type description: str
        :return: A configuration object to be used when creating a Compute object
        :rtype: BatchAiProvisioningConfiguration
        :raises: ComputeTargetException
        """
        super(BatchAiProvisioningConfiguration, self).__init__(BatchAiCompute, location)
        self.vm_size = vm_size
        self.vm_priority = vm_priority
        self.scale_settings = RequestedScaleSettings(autoscale_enabled, autoscale_min_nodes, autoscale_max_nodes)
        self.validate_configuration()
        self.tags = tags
        self.description = description

    def validate_configuration(self):
        """
        Checks that the specified configuration values are valid. Will raise a ComputeTargetException if validation
        fails.

        :raises: ComputeTargetException
        """
        if self.scale_settings.autoscale_enabled is None:
            if self.scale_settings.minimum_node_count is not None:
                raise ComputeTargetException('Invalid provisioning configuration, value provided for min node count'
                                             'but autoscale flag not set.')
            if self.scale_settings.maximum_node_count is not None:
                raise ComputeTargetException('Invalid provisioning configuration, value provided for max node count'
                                             'but autoscale flag not set.')
        elif self.scale_settings.autoscale_enabled:
            if self.scale_settings.minimum_node_count is None or self.scale_settings.maximum_node_count is None:
                raise ComputeTargetException('Invalid provisioning configuration, min and max node counts must both '
                                             'be provided to enable autoscaling.')
        elif self.scale_settings.autoscale_enabled is False:
            if self.scale_settings.maximum_node_count is None or self.scale_settings.maximum_node_count is None or \
                    self.scale_settings.minimum_node_count != self.scale_settings.maximum_node_count:
                raise ComputeTargetException('Invalid provisioning configuration, min and max node counts must be '
                                             'provided and equal when autoscale is False.')


class RequestedScaleSettings(object):
    """
    Requested scale settings object for a BatchAi object
    """
    def __init__(self, autoscale_enabled, minimum_node_count, maximum_node_count):
        """
        Initialize the RequestedScaleSettings object

        :param autoscale_enabled: Whether or not to enable autoscaling on the cluster. If enabled, must provide min
            and max nodes as well. If explicitly set to False, min and max nodes must be equal and are used to provide
            manual setting for number of nodes.
        :type autoscale_enabled: bool
        :param minimum_node_count: Minimum number of nodes to use on the cluster.
        :type minimum_node_count: int
        :param maximum_node_count: Maximum number of nodes to use on the cluster
        :type maximum_node_count: int
        """
        self.autoscale_enabled = autoscale_enabled
        self.minimum_node_count = minimum_node_count
        self.maximum_node_count = maximum_node_count

    def serialize(self):
        """
        Convert this RequestedScaleSettings object into a json serialized dictionary.

        :return: The json representation of this RequestedScaleSettings object
        :rtype: dict
        """
        return {'autoScaleEnabled': self.autoscale_enabled, 'minNodeCount': self.minimum_node_count,
                'maxNodeCount': self.maximum_node_count}

    @staticmethod
    def deserialize(object_dict):
        """
        Convert a json object into a RequestedScaleSettings object.

        :param object_dict: A json object to convert to a RequestedScaleSettings object
        :type object_dict: dict
        :return: The RequestedScaleSettings representation of the provided json object
        :rtype: RequestedScaleSettings
        :raises: ComputeTargetException
        """
        if not object_dict:
            return None
        for key in ['autoScaleEnabled', 'minNodeCount', 'maxNodeCount']:
            if key not in object_dict:
                raise ComputeTargetException('Invalid scale settings payload, missing "{}":\n'
                                             '{}'.format(key, object_dict))
        return RequestedScaleSettings(object_dict['autoScaleEnabled'], object_dict['minNodeCount'],
                                      object_dict['maxNodeCount'])


class BatchAiStatus(object):
    """
    Detailed status for a BatchAI object
    """
    def __init__(self, allocation_state, allocation_state_transition_time, creation_time, current_node_count,
                 errors, node_state_counts, provisioning_state, provisioning_state_transition_time, scale_settings,
                 vm_priority, vm_size):
        """
        Initialize a BatchAiStatus object

        :param allocation_state: String description of the current allocation state
        :type allocation_state: str
        :param allocation_state_transition_time: Time of the most recent allocation state change
        :type allocation_state_transition_time: datetime.datetime
        :param creation_time: Cluster creation time
        :type creation_time: datetime.datetime
        :param current_node_count: The current number of nodes used by the cluster
        :type current_node_count: int
        :param errors: A list of error details, if any
        :type errors: list[dict]
        :param node_state_counts: An object containing counts of the various current node states in the cluster
        :type node_state_counts: BatchAiNodeStateCounts
        :param provisioning_state: Current provisioning state of the cluster
        :type provisioning_state: str
        :param provisioning_state_transition_time: Time of the most recent provisioning state change
        :type provisioning_state_transition_time: datetime.datetime
        :param scale_settings: An object containing the specified scale settings for the cluster
        :type scale_settings: ScaleSettings
        :param vm_priority: dedicated or lowpriority VMs.
        :type vm_priority: str
        :param vm_size: Size of agent VMs. More details can be found here: https://aka.ms/azureml-batchai-details
            and here: https://aka.ms/azureml-vm-details. Note that not all sizes are available in all regions, as
            detailed in the previous link.
        :type vm_size: str
        """
        self.allocation_state = allocation_state
        self.allocation_state_transition_time = allocation_state_transition_time
        self.creation_time = creation_time
        self.current_node_count = current_node_count
        self.errors = errors
        self.node_state_counts = node_state_counts
        self.provisioning_state = provisioning_state
        self.provisioning_state_transition_time = provisioning_state_transition_time
        self.scale_settings = scale_settings
        self.vm_priority = vm_priority
        self.vm_size = vm_size

    def serialize(self):
        """
        Convert this BatchAiStatus object into a json serialized dictionary.

        :return: The json representation of this BatchAiStatus object
        :rtype: dict
        """
        allocation_state_transition_time = self.allocation_state_transition_time.isoformat() \
            if self.allocation_state_transition_time else None
        creation_time = self.creation_time.isoformat() if self.creation_time else None
        node_state_counts = self.node_state_counts.serialize() if self.node_state_counts else None
        provisioning_state_transition_time = self.provisioning_state_transition_time.isoformat() \
            if self.provisioning_state_transition_time else None
        scale_settings = self.scale_settings.serialize() if self.scale_settings else None
        return {'allocationState': self.allocation_state,
                'allocationStateTransitionTime': allocation_state_transition_time, 'creationTime': creation_time,
                'currentNodeCount': self.current_node_count, 'errors': self.errors,
                'nodeStateCounts': node_state_counts, 'provisioningState': self.provisioning_state,
                'provisioningStateTransitionTime': provisioning_state_transition_time, 'scaleSettings': scale_settings,
                'vmPriority': self.vm_priority, 'vmSize': self.vm_size}

    @staticmethod
    def deserialize(object_dict):
        """
        Convert a json object into a BatchAiStatus object.

        :param object_dict: A json object to convert to a BatchAiStatus object
        :type object_dict: dict
        :return: The BatchAiStatus representation of the provided json object
        :rtype: BatchAiStatus
        :raises: ComputeTargetException
        """
        allocation_state = object_dict['properties.allocationState'] \
            if 'properties.allocationState' in object_dict else None
        allocation_state_transition_time = parse(object_dict['properties.allocationStateTransitionTime']) \
            if 'properties.allocationStateTransitionTime' in object_dict else None
        creation_time = parse(object_dict['properties.creationTime']) \
            if 'properties.creationTime' in object_dict else None
        current_node_count = object_dict['properties.currentNodeCount'] \
            if 'properties.currentNodeCount' in object_dict else None
        errors = object_dict['properties.errors'] \
            if 'properties.errors' in object_dict else None
        node_state_counts = BatchAiNodeStateCounts.deserialize(object_dict['properties.nodeStateCounts']) \
            if 'properties.nodeStateCounts' in object_dict else None
        provisioning_state = object_dict['properties.provisioningState'] \
            if 'properties.provisioningState' in object_dict else None
        provisioning_state_transition_time = parse(object_dict['properties.provisioningStateTransitionTime']) \
            if 'properties.provisioningStateTransitionTime' in object_dict else None
        scale_settings = ScaleSettings.deserialize(object_dict['properties.scaleSettings']) \
            if 'properties.scaleSettings' in object_dict else None
        vm_priority = object_dict['properties.vmPriority'] if 'properties.vmPriority' in object_dict else None
        vm_size = object_dict['properties.vmSize'] if 'properties.vmSize' in object_dict else None

        return BatchAiStatus(allocation_state, allocation_state_transition_time, creation_time, current_node_count,
                             errors, node_state_counts, provisioning_state, provisioning_state_transition_time,
                             scale_settings, vm_priority, vm_size)


class BatchAiNodeStateCounts(object):
    """
    Detailed node counts for a BatchAI object
    """
    def __init__(self, idle_node_count, leaving_node_count, preparing_node_count, running_node_count,
                 unusable_node_count):
        """
        Initialize a BatchAiNodeStateCounts object

        :param idle_node_count: Current number of idle nodes
        :type idle_node_count: int
        :param leaving_node_count: Current number of nodes that are being deprovisioned
        :type leaving_node_count: int
        :param preparing_node_count: Current number of nodes that are being provisioned
        :type preparing_node_count: int
        :param running_node_count: Current number of in use nodes
        :type running_node_count: int
        :param unusable_node_count: Current number of unusable nodes
        :type unusable_node_count: int
        """
        self.idle_node_count = idle_node_count
        self.leaving_node_count = leaving_node_count
        self.preparing_node_count = preparing_node_count
        self.running_node_count = running_node_count
        self.unusable_node_count = unusable_node_count

    def serialize(self):
        """
        Convert this BatchAiNodeStateCounts object into a json serialized dictionary.

        :return: The json representation of this BatchAiNodeStateCounts object
        :rtype: dict
        """
        return {'idleNodeCount': self.idle_node_count, 'leavingNodeCount': self.leaving_node_count,
                'preparingNodeCount': self.preparing_node_count, 'runningNodeCount': self.running_node_count,
                'unusableNodeCount': self.unusable_node_count}

    @staticmethod
    def deserialize(object_dict):
        """
        Convert a json object into a BatchAiNodeStateCounts object.

        :param object_dict: A json object to convert to a BatchAiNodeStateCounts object
        :type object_dict: dict
        :return: The BatchAiNodeStateCounts representation of the provided json object
        :rtype: BatchAiNodeStateCounts
        :raises: ComputeTargetException
        """
        idle_node_count = object_dict['idleNodeCount'] if 'idleNodeCount' in object_dict else None
        leaving_node_count = object_dict['leavingNodeCount'] if 'leavingNodeCount' in object_dict else None
        preparing_node_count = object_dict['preparingNodeCount'] if 'preparingNodeCount' in object_dict else None
        running_node_count = object_dict['runningNodeCount'] if 'runningNodeCount' in object_dict else None
        unusable_node_count = object_dict['unusableNodeCount'] if 'unusableNodeCount' in object_dict else None

        return BatchAiNodeStateCounts(idle_node_count, leaving_node_count, preparing_node_count, running_node_count,
                                      unusable_node_count)


class ScaleSettings(object):
    """
    Specific scale settings for a BatchAI object
    """
    def __init__(self, manual_scale_settings, auto_scale_settings):
        """
        Initialize a ScaleSettings object

        :param manual_scale_settings: An object defining the current manual scale settings for the cluster
        :type manual_scale_settings: ManualScaleSettings | None
        :param auto_scale_settings: An object defining the current automatic scale settings for the cluster
        :type auto_scale_settings: AutoScaleSettings | None
        """
        self.manual = manual_scale_settings
        self.auto_scale = auto_scale_settings

    def serialize(self):
        """
        Convert this ScaleSettings object into a json serialized dictionary.

        :return: The json representation of this ScaleSettings object
        :rtype: dict
        """
        manual = self.manual.serialize() if self.manual else None
        auto_scale = self.auto_scale.serialize() if self.auto_scale else None
        return {'manual': manual, 'autoScale': auto_scale}

    @staticmethod
    def deserialize(object_dict):
        """
        Convert a json object into a ScaleSettings object.

        :param object_dict: A json object to convert to a ScaleSettings object
        :type object_dict: dict
        :return: The ScaleSettings representation of the provided json object
        :rtype: ScaleSettings
        :raises: ComputeTargetException
        """
        manual = ManualScaleSettings.deserialize(object_dict['manual']) \
            if 'manual' in object_dict and object_dict['manual'] else None
        auto_scale = AutoScaleSettings.deserialize(object_dict['autoScale']) \
            if 'autoScale' in object_dict and object_dict['autoScale'] else None

        return ScaleSettings(manual, auto_scale)


class ManualScaleSettings(object):
    """
    Details for manual scale settings for a BatchAI object
    """
    def __init__(self, target_node_count, node_deallocation_option):
        """
        Initialize a ManualScaleSettings object

        :param target_node_count: The number of desired nodes for the cluster
        :type target_node_count: int
        :param node_deallocation_option: Option when nodes are deallocated
        :type node_deallocation_option: str
        """
        self.target_node_count = target_node_count
        self.node_deallocation_option = node_deallocation_option

    def serialize(self):
        """
        Convert this ManualScaleSettings object into a json serialized dictionary.

        :return: The json representation of this ManualScaleSettings object
        :rtype: dict
        """
        return {'targetNodeCount': self.target_node_count, 'nodeDeallocationOption': self.node_deallocation_option}

    @staticmethod
    def deserialize(object_dict):
        """
        Convert a json object into a ManualScaleSettings object.

        :param object_dict: A json object to convert to a ManualScaleSettings object
        :type object_dict: dict
        :return: The ManualScaleSettings representation of the provided json object
        :rtype: ManualScaleSettings
        :raises: ComputeTargetException
        """
        target_node_count = object_dict['targetNodeCount'] if 'targetNodeCount' in object_dict else None
        node_deallocation_option = object_dict['nodeDeallocationOption'] \
            if 'nodeDeallocationOption' in object_dict else None

        return ManualScaleSettings(target_node_count, node_deallocation_option)


class AutoScaleSettings(object):
    """
    Details for automatic scale settings for a BatchAI object
    """
    def __init__(self, max_node_count, min_node_count, initial_node_count):
        """
        Initialize an AutoScaleSettings object

        :param max_node_count: The maximum number of nodes for the cluster
        :type max_node_count: int
        :param min_node_count: The minimum number of nodes for the cluster
        :type min_node_count: int
        :param initial_node_count: The number of nodes for the cluster to start with
        :type initial_node_count: int
        """
        self.max_node_count = max_node_count
        self.min_node_count = min_node_count
        self.initial_node_count = initial_node_count

    def serialize(self):
        """
        Convert this AutoScaleSettings object into a json serialized dictionary.

        :return: The json representation of this AutoScaleSettings object
        :rtype: dict
        """
        return {'maximumNodeCount': self.max_node_count, 'minimumNodeCount': self.min_node_count,
                'initialNodeCount': self.initial_node_count}

    @staticmethod
    def deserialize(object_dict):
        """
        Convert a json object into a AutoScaleSettings object.

        :param object_dict: A json object to convert to a AutoScaleSettings object
        :type object_dict: dict
        :return: The AutoScaleSettings representation of the provided json object
        :rtype: AutoScaleSettings
        :raises: ComputeTargetException
        """
        max_node_count = object_dict['maximumNodeCount'] if 'maximumNodeCount' in object_dict else None
        min_node_count = object_dict['minimumNodeCount'] if 'minimumNodeCount' in object_dict else None
        initial_node_count = object_dict['initialNodeCount'] if 'initialNodeCount' in object_dict else None

        return AutoScaleSettings(max_node_count, min_node_count, initial_node_count)
