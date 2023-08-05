# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Module for managing Remote Compute Targets in Azure ML"""

import copy
import json
import requests
import traceback
from azureml._compute._constants import MLC_COMPUTE_RESOURCE_ID_FMT
from azureml._compute._constants import MLC_ENDPOINT_FMT
from azureml._compute._constants import MLC_WORKSPACE_API_VERSION
from azureml._compute._util import remote_payload_template
from azureml.core.compute import ComputeTarget
from azureml.exceptions import ComputeTargetException


class RemoteCompute(ComputeTarget):
    """
    Class for managing RemoteCompute target objects.
    """
    _compute_type = 'VirtualMachine'

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
        vm_size = obj_dict['properties']['properties']['virtualMachineSize'] \
            if 'virtualMachineSize' in obj_dict['properties']['properties'] else None
        address = obj_dict['properties']['properties']['address'] \
            if 'address' in obj_dict['properties']['properties'] else None
        ssh_port = obj_dict['properties']['properties']['sshPort'] \
            if 'sshPort' in obj_dict['properties']['properties'] else None
        super(RemoteCompute, self)._initialize(compute_resource_id, name, location, compute_type, tags, description,
                                               created_on, modified_on, provisioning_state, provisioning_errors,
                                               cluster_resource_id, cluster_location, workspace, mlc_endpoint, None,
                                               workspace._auth)
        self.vm_size = vm_size
        self.address = address
        self.ssh_port = ssh_port

    @staticmethod
    def attach(workspace, name, username, address, ssh_port='22', password='',
               private_key_file='', private_key_passphrase=''):
        """
        Associates an already existing Remote compute resource with the provided workspace.

        :param workspace: The workspace object to associate the compute resource with
        :type workspace: azureml.core.workspace.Workspace
        :param name: The name to associate with the compute resource inside the provided workspace. Does not have to
            match with the already given name of the compute resource
        :type name: str
        :param username: The username needed to access the resource
        :type username: str
        :param address: The address for the already existing resource
        :type address: str
        :param ssh_port: The exposed port for the resource
        :type ssh_port: int
        :param password: The password needed to access the resource
        :type password: str
        :param private_key_file: Path to a file containing the private key for the resource
        :type private_key_file: str
        :param private_key_passphrase: Private key phrase needed to access the resource
        :type private_key_passphrase: str
        :return: A RemoteCompute object representation of the compute object
        :rtype: RemoteCompute
        :raises: ComputeTargetException
        """
        attach_payload = RemoteCompute._build_attach_payload(address, ssh_port, username, password,
                                                             private_key_file, private_key_passphrase)
        return ComputeTarget._attach(workspace, name, attach_payload, RemoteCompute)

    @staticmethod
    def _build_attach_payload(address, ssh_port, username, password=None, private_key_file=None,
                              private_key_passphrase=None):
        """

        :param address:
        :type address: str
        :param ssh_port:
        :type ssh_port: int
        :param username:
        :type username: str
        :param password:
        :type password: str
        :param private_key_file:
        :type private_key_file: str
        :param private_key_passphrase:
        :type private_key_passphrase: str
        :return:
        :rtype: dict
        """
        json_payload = copy.deepcopy(remote_payload_template)
        if not address:
            raise ComputeTargetException('Error, missing address.')
        if not ssh_port:
            raise ComputeTargetException('Error, missing ssh-port.')

        if not username:
            raise ComputeTargetException('Error, no username provided. Please provide a username and either a'
                                         'password or key information.')
        json_payload['properties']['properties']['administratorAccount']['username'] = username
        if not password and not private_key_file:
            raise ComputeTargetException('Error, no password or key information provided. Please provide either a '
                                         'password or key information.')
        if password and private_key_file:
            raise ComputeTargetException('Invalid attach information, both password and key information provided. '
                                         'Please provide either a password or key information')
        if password:
            json_payload['properties']['properties']['administratorAccount']['password'] = password
            del(json_payload['properties']['properties']['administratorAccount']['publicKeyData'])
            del(json_payload['properties']['properties']['administratorAccount']['privateKeyData'])
        else:
            try:
                with open(private_key_file, 'r') as private_key_file_obj:
                    private_key = private_key_file_obj.read()
            except (IOError, OSError) as exc:
                raise ComputeTargetException("Error while reading key information:\n"
                                             "{}".format(traceback.format_exc().splitlines()[-1]))
            json_payload['properties']['properties']['administratorAccount']['privateKeyData'] = private_key
            if private_key_passphrase:
                json_payload['properties']['properties']['administratorAccount']['passphrase'] = private_key_passphrase

        del (json_payload['properties']['properties']['virtualMachineSize'])
        del (json_payload['properties']['computeLocation'])
        json_payload['properties']['properties']['address'] = address
        json_payload['properties']['properties']['sshPort'] = ssh_port
        return json_payload

    def refresh_state(self):
        """
        Perform an in-place update of the properties of the object based on the current state of the
        corresponding cloud object. Primarily useful for manual polling of compute state.
        """
        cluster = RemoteCompute(self.workspace, self.name)
        self.modified_on = cluster.modified_on
        self.provisioning_state = cluster.provisioning_state
        self.provisioning_errors = cluster.provisioning_errors
        self.cluster_resource_id = cluster.cluster_resource_id
        self.cluster_location = cluster.cluster_location
        self.vm_size = cluster.vm_size
        self.address = cluster.address
        self.ssh_port = cluster.ssh_port

    def delete(self):
        """
        Removes the RemoteCompute object from its associated workspace. If this object was created through Azure ML,
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

    def get_credentials(self):
        """
        Retrieve the credentials for the RemoteCompute target

        :return: Credentials for the RemoteCompute target
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
            raise ComputeTargetException('Received bad response from MLC:\n'
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
        Convert this RemoteCompute object into a json serialized dictionary.

        :return: The json representation of this RemoteCompute object
        :rtype: dict
        """
        remote_properties = {'vmSize': self.vm_size, 'address': self.address, 'ssh-port': self.ssh_port}
        cluster_properties = {'computeType': 'VirtualMachine', 'computeLocation': self.cluster_location,
                              'description': self.description, 'resourceId': self.cluster_resource_id,
                              'provisioningErrors': self.provisioning_errors,
                              'provisioningState': self.provisioning_state, 'properties': remote_properties}
        return {'id': self.id, 'name': self.name, 'tags': self.tags, 'location': self.location,
                'properties': cluster_properties}

    @staticmethod
    def deserialize(workspace, object_dict):
        """
        Convert a json object into a RemoteCompute object. Will fail if the provided workspace is not the
        workspace the Compute is associated with.

        :param workspace: The workspace object the RemoteCompute object is associated with
        :type workspace: azureml.core.workspace.Workspace
        :param object_dict: A json object to convert to a RemoteCompute object
        :type object_dict: dict
        :return: The RemoteCompute representation of the provided json object
        :rtype: RemoteCompute
        :raises: ComputeTargetException
        """
        RemoteCompute._validate_get_payload(object_dict)
        target = RemoteCompute(None, None)
        target._initialize(workspace, object_dict)
        return target

    @staticmethod
    def _validate_get_payload(payload):
        if 'properties' not in payload or 'computeType' not in payload['properties']:
            raise ComputeTargetException('Invalid cluster payload:\n'
                                         '{}'.format(payload))
        if payload['properties']['computeType'] != RemoteCompute._compute_type:
            raise ComputeTargetException('Invalid cluster payload, not "{}":\n'
                                         '{}'.format(RemoteCompute._compute_type, payload))
        for arm_key in ['location', 'id', 'tags']:
            if arm_key not in payload:
                raise ComputeTargetException('Invalid cluster payload, missing ["{}"]:\n'
                                             '{}'.format(arm_key, payload))
        for key in ['properties', 'provisioningErrors', 'description', 'provisioningState', 'resourceId']:
            if key not in payload['properties']:
                raise ComputeTargetException('Invalid cluster payload, missing ["properties"]["{}"]:\n'
                                             '{}'.format(key, payload))
