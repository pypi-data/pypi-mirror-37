# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

""" compute_target.py includes different compute target classes"""
from abc import ABCMeta

from azureml.exceptions import ComputeTargetException


class AbstractComputeTarget(object):
    """
    An abstract class for a compute targets.
    """
    __metaclass__ = ABCMeta

    # Serialization keys.
    _TARGET_TYPE_KEY = "type"

    def __init__(self, compute_target_type, name):
        """
        :param compute_target_type: The compute target type.
        :type compute_target_type: str
        :param name: Name of the compute target.
        :type name: str
        """
        self._compute_target_type = compute_target_type
        self._name = name
        self._default_framework = "Python"

    @property
    def type(self):
        """
        :return: Returns the compute target type.
        :rtype: str
        """
        return self._compute_target_type

    @property
    def name(self):
        """
        :return: Returns name of the compute target.
        :rtype: str
        """
        return self._name

    @staticmethod
    def deserialize_from_dict(compute_target_name, compute_target_dict):
        """
        De-serializes compute_target_dict and returns the corresponding compute target object.
        :param compute_target_name: The compute target name, basically <compute_target_name>.compute file.
        :type compute_target_name: str
        :param compute_target_dict: The compute target dict, loaded from the on-disk .compute file.
        :type compute_target_dict: dict
        :return: The target specific compute target object.
        :rtype: AbstractComputeTarget
        """
        _type_to_class_dict = {
            BatchAITarget._BATCH_AI_TYPE: BatchAITarget
        }

        if AbstractComputeTarget._TARGET_TYPE_KEY in compute_target_dict:
            compute_type = compute_target_dict[AbstractComputeTarget._TARGET_TYPE_KEY]
            if compute_type in _type_to_class_dict:
                return _type_to_class_dict[compute_type]._deserialize_from_dict(compute_target_name,
                                                                                compute_target_dict)
            else:
                return None
        else:
            raise ComputeTargetException("{} required field is not present in {} dict for "
                                         "creating the require compute target "
                                         "object.".format(AbstractComputeTarget._TARGET_TYPE_KEY,
                                                          compute_target_dict))

    def _serialize_to_dict(self):
        """
        Serializes a compute target object to a dictionary.
        The dictionary is used to write the .compute file on disk in the yaml format.
        :return:
        :rtype: dict
        """
        compute_skeleton = dict()
        compute_skeleton[AbstractComputeTarget._TARGET_TYPE_KEY] = self._compute_target_type
        return compute_skeleton


class _SSHBasedComputeTarget(AbstractComputeTarget):
    """
    A class that defines a SSH based compute target.
    """

    # Serialization keys.
    _ADDRESS_KEY = "address"
    _USERNAME_KEY = "username"

    _PASSWORD_KEY = "password"
    _PRIVATE_KEY_KEY = "privateKey"

    def __init__(self, compute_target_type, name, address, username, password=None, private_key_file=None,
                 private_key_passphrase=None, use_ssh_keys=False):
        """

        :param compute_target_type: The compute target type.
        :type compute_target_type: str
        :param name: Name of the compute target.
        :type name: str
        :param address: Address of the compute target. Accepted addresses are
        DNS name, DNS name:port, IP address, IP address:port.
        If no port is specified then the default SSH port 22 is used.
        :type address: str
        :param username: Username name for SSH login.
        :type username: str
        :param password: Password for the SSH login.
        :type password: str
        :param private_key_file: Private key file for SSH login.
        :type private_key_file: str
        :param private_key_passphrase: Passphrase for the private key specified using private_key_file.
        :type private_key_passphrase: str
        :param use_ssh_keys: Use SSH keys for SSH into the compute target.
        :type use_ssh_keys: bool
        """
        # TODO: SSH key support.
        super(_SSHBasedComputeTarget, self).__init__(compute_target_type, name)
        self._address = address
        self._username = username
        self._password = password
        self._private_key_file = private_key_file
        self._private_key_passphrase = private_key_passphrase
        self._use_ssh_keys = use_ssh_keys

        # TODO: Validation checks, 1) address should not contains protocol prefix.
        # 2) Only password or private key should be specified.

    @property
    def address(self):
        """
        :return: Returns the address.
        :rtype: str
        """
        return self._address

    @property
    def username(self):
        """
        :return: Returns the username.
        :rtype: str
        """
        return self._username

    @property
    def password(self):
        """
        :return: Returns the password
        :rtype: str
        """
        return self._password

    @property
    def private_key_file(self):
        """
        :return: Returns the private key file path
        :rtype: str
        """
        return self._private_key_file

    @property
    def private_key_passphrase(self):
        """
        :return: Returns the private key passphrase
        :rtype: str
        """
        return self._private_key_passphrase

    @property
    def use_ssh_keys(self):
        """
        :return: Returns the setting for ssh keys
        :rtype: bool
        """
        return self._use_ssh_keys

    def _serialize_to_dict(self):
        """
        Serializes a compute target object to a dictionary excluding the properties that require storage
        in the credential service.
        The dictionary is used to write the .compute file on disk in the yaml format.
        :return:
        :rtype: dict
        """
        # Compute context
        compute_skeleton = super(_SSHBasedComputeTarget, self)._serialize_to_dict()

        compute_skeleton[_SSHBasedComputeTarget._ADDRESS_KEY] = self._address
        compute_skeleton[_SSHBasedComputeTarget._USERNAME_KEY] = self._username

        # Password or ssh key is stored while attaching, as at that time those are stored in
        # the credential service and the credential service key is stored in the .compute file.
        return compute_skeleton


class LocalTarget(AbstractComputeTarget):
    """
    A class to define the local machine as a compute target.
    """
    # Compute target type
    _LOCAL_TYPE = "local"

    def __init__(self):
        """
        Set up local target.
        """
        name = "local"
        super(LocalTarget, self).__init__(LocalTarget._LOCAL_TYPE, name)


class BatchAITarget(AbstractComputeTarget):
    """
    A class to define a batchAI cluster as a compute target.
    """
    # Compute target type
    _BATCH_AI_TYPE = "batchai"

    # Serialization keys
    _SUBSCRIPTION_ID_KEY = "subscriptionId"
    _RESOURCE_GROUP_NAME_KEY = "resourceGroup"
    _CLUSTER_NAME_KEY = "clusterName"
    _WORKSPACE_NAME_KEY = "workspaceName"

    def __init__(self, name, subscription_id, resource_group_name, cluster_name, batchai_workspace_name=None):
        """
        :param name: Name of the compute target.
        :type name: str
        :param subscription_id: The subscription id for the batchai cluster.
        :type subscription_id: str
        :param resource_group_name: The resource group name for the batchai cluster.
        :type resource_group_name: str
        :param cluster_name: The batchAI cluster name.
        :type cluster_name: str
        :param batchai_workspace_name: The batchAI workspace name.
        :type batchai_workspace_name: str
        """
        super(BatchAITarget, self).__init__(BatchAITarget._BATCH_AI_TYPE, name)
        self._subscription_id = subscription_id
        self._resource_group_name = resource_group_name
        self._cluster_name = cluster_name
        self._batchai_workspace_name = batchai_workspace_name

    @property
    def subscription_id(self):
        """
        :return: Returns the subscription id for the dynamic compute target.
        :rtype: str
        """
        return self._subscription_id

    @property
    def resource_group_name(self):
        """
        :return: Returns the resource group name for the dynamic compute target.
        :rtype: str
        """
        return self._resource_group_name

    @property
    def cluster_name(self):
        """
        :return: Returns cluster name.
        :rtype: str
        """
        return self._cluster_name

    def _serialize_to_dict(self):
        """
        Serializes a compute target object to a dictionary excluding the properties that require storage
        in the credential service.
        The dictionary is used to write the .compute file on disk in the yaml format.
        :return:
        :rtype: dict
        """
        # Compute context
        compute_skeleton = super(BatchAITarget, self)._serialize_to_dict()
        compute_skeleton[BatchAITarget._SUBSCRIPTION_ID_KEY] = self._subscription_id
        compute_skeleton[BatchAITarget._RESOURCE_GROUP_NAME_KEY] = self._resource_group_name
        compute_skeleton[BatchAITarget._CLUSTER_NAME_KEY] = self._cluster_name
        compute_skeleton[BatchAITarget._WORKSPACE_NAME_KEY] = self._batchai_workspace_name

        return compute_skeleton

    @staticmethod
    def _deserialize_from_dict(compute_target_name, compute_target_dict):
        """
        Creates a compute target object from a dictionary.
        :param compute_target_name: The compute target name, basically <compute_target_name>.compute file.
        :type compute_target_name: str
        :param compute_target_dict: The compute target dict, loaded from the on-disk .compute file.
        :type compute_target_dict: dict
        :return:
        :rtype: BatchAITarget
        """
        if (BatchAITarget._SUBSCRIPTION_ID_KEY in compute_target_dict and
                BatchAITarget._RESOURCE_GROUP_NAME_KEY in compute_target_dict and
                BatchAITarget._CLUSTER_NAME_KEY in compute_target_dict):
            batchai_object = BatchAITarget(compute_target_name,
                                           compute_target_dict[BatchAITarget._SUBSCRIPTION_ID_KEY],
                                           compute_target_dict[BatchAITarget._RESOURCE_GROUP_NAME_KEY],
                                           compute_target_dict[BatchAITarget._CLUSTER_NAME_KEY].
                                           compute_target_dict.get(BatchAITarget._WORKSPACE_NAME_KEY))

            return batchai_object
        else:
            raise ComputeTargetException("Failed to create a compute target object from a dictionary. "
                                         "Either {}, {} or {} is missing in "
                                         "{}".format(BatchAITarget._SUBSCRIPTION_ID_KEY,
                                                     BatchAITarget._RESOURCE_GROUP_NAME_KEY,
                                                     BatchAITarget._CLUSTER_NAME_KEY,
                                                     compute_target_dict))


# TODO: Free floating until MLC ready
def prepare_compute_target(experiment, source_directory, run_config):
    """
    Prepares the compute target, i.e., installs all the required
    packages for an experiment run based on run_config and custom_run_config.
    :param experiment:
    :type experiment: azureml.core.experiment.Experiment
    :param source_directory:
    :type source_directory: str
    :param run_config: The run configuration. This can be a run configuration name, as string, or a
    azureml.core.runconfig.RunConfiguration object.
    :type run_config: str or azureml.core.runconfig.RunConfiguration
    :return: A run object
    :rtype: azureml.core.experiment_run.ExperimentRun
    """
    from azureml._execution import _commands
    from azureml.core.runconfig import RunConfiguration
    from azureml._project.project import Project

    run_config_object = RunConfiguration._get_run_config_object(path=source_directory, run_config=run_config)
    project_object = Project(experiment=experiment, directory=source_directory)
    return _commands.prepare_compute_target(project_object, run_config_object)


# TODO: Free floating until MLC ready
def is_compute_target_prepared(experiment, source_directory, run_config):
    """
    Checks whether the compute target, specified in run_config, is already prepared or not for
    the specified run configuration.
    :param experiment:
    :type experiment: azureml.core.experiment.Experiment
    :param source_directory:
    :type source_directory: str
    :param run_config: The run configuration. This can be a run configuration name, as string, or a
    azureml.core.runconfig.RunConfiguration object.
    :type run_config: str or azureml.core.runconfig.RunConfiguration
    :return: True, if the compute target is prepared.
    :rtype: bool
    """
    from azureml._execution import _commands
    from azureml.core.runconfig import RunConfiguration
    from azureml._project.project import Project

    run_config_object = RunConfiguration._get_run_config_object(path=source_directory, run_config=run_config)
    project_object = Project(experiment=experiment, directory=source_directory)
    return _commands.prepare_compute_target(project_object, run_config_object, check=True)


# TODO: Free floating until MLC ready
def attach_legacy_compute_target(experiment, source_directory, compute_target):
    """
    Attaches a compute target to this project.
    :param experiment:
    :type experiment: azureml.core.experiment.Experiment
    :param source_directory:
    :type source_directory: str
    :param compute_target: A compute target object to attach. The object should be of one
    :type compute_target: str
    of the following classes:
      1) azureml.core.compute_target.BatchAITarget
    :return: None if the attach is successful, otherwise throws an exception.
    """
    from azureml._project import _compute_target_commands
    if isinstance(compute_target, _SSHBasedComputeTarget):
        _compute_target_commands.attach_ssh_based_compute_targets(experiment, source_directory, compute_target)
    elif isinstance(compute_target, BatchAITarget):
        _compute_target_commands.attach_batchai_compute_target(experiment, source_directory, compute_target)
    else:
        raise ComputeTargetException("Unsupported compute target type. Type={}".format(type(compute_target)))


# TODO: Free floating until MLC ready
def remove_legacy_compute_target(experiment, source_directory, compute_target_name):
    """
    Removes a compute target from the project.
    :param experiment:
    :type experiment: azureml.core.experiment.Experiment
    :param source_directory:
    :type source_directory: str
    :param compute_target_name:
    :type compute_target_name: str
    :return: None if the removal of the compute target is successful, otherwise throws an exception.
    :rtype: None
    """
    from azureml._project import _compute_target_commands
    _compute_target_commands.detach_compute_target(experiment, source_directory, compute_target_name)
