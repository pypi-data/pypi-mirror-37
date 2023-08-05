# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

import os


# Az CLI converts the keys to camelCase and our tests assume that behavior,
# so converting for the SDK too.
from azureml.core.authentication import InteractiveLoginAuthentication
from azureml.exceptions import UserErrorException
from azureml.core.runconfig import RunConfiguration
from azureml._base_sdk_common.project_context import create_project_context
from azureml._base_sdk_common.create_snapshot import create_snapshot
from azureml._base_sdk_common.restore_snapshot import RestoreSnapshot

from azureml._base_sdk_common.common import give_warning
from azureml._base_sdk_common.common import check_valid_resource_name


from azureml._project import _commands
from azureml._project import _compute_target_commands


class Project(object):
    """
    The project class for local on-disk projects.
    """
    def __init__(self, directory=".", experiment=None, auth=None, _disable_service_check=False):
        """
        Creates the project object using the local project path.
        :param directory: Project path.
        :type directory: str
        :param experiment:
        :type experiment: azureml.core.Experiment
        :param auth: An authentication object of a subclass of azureml.core.authentication.AbstractAuthentication
        :type auth: azureml.core.authentication.AbstractAuthentication
        :return:
        """
        from azureml.core.experiment import Experiment
        if not directory:
            directory = "."
        if experiment:
            self._workspace_object = experiment.workspace
            self.directory = directory
            self._project_path = os.path.abspath(directory)
            self._experiment = experiment

        else:
            if not auth:
                auth = InteractiveLoginAuthentication()

            self._project_path = os.path.abspath(directory)

            info_dict = _commands.get_project_info(auth, self._project_path)

            from azureml.core.workspace import Workspace
            self._workspace_object = Workspace(info_dict[_commands.SUBSCRIPTION_KEY],
                                               info_dict[_commands.RESOURCE_GROUP_KEY],
                                               info_dict[_commands.WORKSPACE_KEY],
                                               auth, _disable_service_check=_disable_service_check)
            self._experiment = Experiment(self._workspace_object, info_dict[_commands.PROJECT_KEY])

    @property
    def workspace_object(self):
        """
        :return: Returns the workspace object corresponding to this project.
        :rtype: azureml.core.workspace.Workspace
        """
        return self._workspace_object

    @property
    def history(self):
        """
        :return: Returns the run history corresponding to this project.
        :rtype: azureml.core.experiment.Experiment
        """
        return self._experiment

    @staticmethod
    def attach(workspace_object, experiment_name, directory=".", auth=None, _location=None):
        """
        Attaches the project, specified by directory, as an azureml project to
        the specified workspace and run history.
        If the path specified by directory doesn't exist then we create those directories.
        :param workspace_object: The workspace object.
        :type workspace_object: azureml.core.workspace.Workspace
        :param experiment_name: The experiment name.
        :type experiment_name: str
        :param directory: The directory path.
        :type directory: str
        :param auth: The auth object.
        :type auth: azureml.core.authentication.AbstractAuthentication
        :return: The project object.
        :rtype: azureml.core.project.Project
        """
        if not auth:
            auth = InteractiveLoginAuthentication()

        if not directory:
            directory = "."

        # Runhistory location.
        if not _location:
            _location = workspace_object.location

        check_valid_resource_name(experiment_name, "Experiment")

        _commands.attach_project(auth, workspace_object.resource_group, workspace_object.name, experiment_name,
                                 workspace_object.subscription_id, project_path=directory, location=_location)

        # The project is created inside directory with name project_name.
        # So the project directory is os.path.join(directory, project_name)
        project = Project(auth=auth, directory=directory)

        return project

    @property
    def project_directory(self):
        """
        Returns the local on-disk project path.
        :return:
        """
        return self._project_path

    @property
    def run_configurations(self):
        """
        Returns all run configurations for the project.
        :return: Returns a dictionary of all RunConfiguration objects.
        A key is a run config name, the value is the azureml.core.runconfig.RunConfiguration object.
        :rtype: dict
        """
        return RunConfiguration._get_all_run_configurations(self.project_directory)

    def detach(self):
        """
        Detaches the current project from being an azureml project.
        Throws an exception if detach fails.
        :return: None
        """
        # TODO: Nice errors for the detached projects object reuse.
        _commands.detach_project(self.project_directory)

    def clean_target(self, run_config):
        """
        Removes files corresponding to all azureml runs on the target specified by run_config.
        :param run_config: The run configuration. This can be a run configuration name, as string, or a
        azureml.core.runconfig.RunConfiguration object.
        :type run_config: str or azureml.core.runconfig.RunConfiguration
        :return: List of files deleted.
        :rtype: list
        """
        give_warning("DeprecationWarning: This method will be deprecated in a week. Please use "
                     "Run.clean_all method.")
        from azureml.core.run import Run
        return Run.clean_all(self, run_config)

    def get_details(self):
        """
        Returns the details of the current project.
        :return:
        :rtype: dict
        """
        return self._serialize_to_dict()

    @property
    def legacy_compute_targets(self):
        """
        Returns legacy compute targets as a dictionary.
        Key is the compute target name, value is the compute target type
        :return:
        :rtype: dict
        """
        return _compute_target_commands.get_all_compute_target_objects(self)

    # To be made public in future.
    def _take_snapshot(self):
        """
        Take a snapshot of the project.
        :return: SnapshotId
        """
        project_context = create_project_context(self.workspace_object._auth_object,
                                                 subscription_id=self.workspace_object.subscription_id,
                                                 resource_group=self.workspace_object.resource_group,
                                                 workspace=self.workspace_object.name,
                                                 project_name=self.history.name)
        return create_snapshot(self.project_directory, project_context)

    # To be made public in future.
    def _snapshot_restore(self, snapshot_id, path=None):
        """
        Restores a project to a snapshot, specified by the snapshot_id.
        :param snapshot_id: The snapshot id to restore to.
        :type snapshot_id: str
        :param path: The path where the project should be restored.
        :type path: str
        :return: The path.
        :rtype: str
        """
        project_context = create_project_context(self._workspace_object._auth_object,
                                                 subscription_id=self._workspace_object.subscription_id,
                                                 resource_group=self._workspace_object.resource_group,
                                                 workspace=self._workspace_object.name,
                                                 project_name=self.history.name)
        restore = RestoreSnapshot(project_context)
        path = restore.restore_snapshot(snapshot_id, path)
        return path

    def _get_run_config_object(self, run_config):
        if isinstance(run_config, str):
            # If it is a string then we don't need to create a copy.
            return RunConfiguration.load(self.project_directory, run_config)
        elif isinstance(run_config, RunConfiguration):
            # TODO: Deep copy of project and auth object too.
            import copy
            return copy.deepcopy(run_config)
        else:
            raise UserErrorException("Unsupported runconfig type {}. run_config can be of str or "
                                     "azureml.core.runconfig.RunConfiguration type.".format(type(run_config)))

    def _serialize_to_dict(self):
        """
        Serializes the Project object details into a dictionary.
        :return:
        :rtype: dict
        """
        output_dict = self.history._serialize_to_dict()
        output_dict["Project path"] = self.project_directory
        return output_dict
