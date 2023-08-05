# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

""" cmd_computetarget_attach.py, A file for handling compute target attach commands."""

import getpass

from azureml._base_sdk_common.common import set_correlation_id
from azureml.core import attach_legacy_compute_target
from azureml.core.experiment import Experiment
from azureml.core.compute import AdlaCompute
from azureml.core.compute import AksCompute
from azureml.core.compute import DataFactoryCompute
from azureml.core.compute import DatabricksCompute
from azureml.core.compute import HDInsightCompute
from azureml.core.compute import RemoteCompute
from azureml.core.runconfig import RunConfiguration
from azureml._base_sdk_common.common import CLICommandOutput, RUNCONFIGURATION_EXTENSION, COMPUTECONTEXT_EXTENSION
from azureml.exceptions import UserErrorException
from azureml._project.project import Project
from ._common import get_workspace_or_default


from ._common import get_cli_specific_auth, get_cli_specific_output

# pylint: disable=line-too-long

""" Modules """


def attach_remote(name, address, ssh_port, username, password='', private_key_file='',
                  private_key_passphrase='', workspace_name=None, resource_group_name=None, ):
    workspace = get_workspace_or_default(workspace_name=workspace_name, resource_group=resource_group_name)

    print('Attaching compute resource...')
    RemoteCompute.attach(workspace, name, username, address, ssh_port, password, private_key_file,
                         private_key_passphrase)
    print('Resource attach submitted successfully.')
    print('To see if your compute target is ready to use, run:')
    print('  az ml computetarget show -n {}'.format(name))


def attach_hdi(name, address, ssh_port, username, password='', private_key_file='',
               private_key_passphrase='', workspace_name=None, resource_group_name=None):
    workspace = get_workspace_or_default(workspace_name=workspace_name, resource_group=resource_group_name)

    print('Attaching hdi compute cluster...')
    HDInsightCompute.attach(workspace, name, username, address, ssh_port, password, private_key_file,
                            private_key_passphrase)
    print('HDI cluster compute attach request submitted successfully.')
    print('To see if your compute target is ready to use, run:')
    print('  az ml computetarget show -n {}'.format(name))


def attach_batchai(name=None, base_docker_image=None, subscription_id=None, resource_group=None,
                   batchai_workspace_name=None, cluster_name=None, node_count=None, project=None):
    """
    Attach batch AI as a compute target.
    """

    from azureml.core.compute_target import BatchAITarget

    # Set correlation id
    set_correlation_id()

    if not project:
        project = "."

    auth = get_cli_specific_auth()
    project_object = Project(auth=auth, directory=project)

    compute_target_object = BatchAITarget(name, subscription_id, resource_group, cluster_name, batchai_workspace_name)
    experiment = Experiment(project_object.workspace_object, project_object.history.name)
    attach_legacy_compute_target(experiment, project_object.project_directory, compute_target_object)

    # Modifying fields directly in runconfig.
    run_config_object = RunConfiguration.load(project_object.project_directory, name)

    if base_docker_image:
        run_config_object.environment.docker.base_image = base_docker_image

    if node_count:
        run_config_object.batchai.node_count = int(node_count)

    run_config_object.save()
    cli_command_output = _get_attach_status(name)
    return get_cli_specific_output(cli_command_output)


def attach_aks(name, compute_resource_id, workspace_name=None, resource_group_name=None):
    _attach_compute_internal(name, compute_resource_id, AksCompute, workspace_name, resource_group_name)


def attach_datafactory(name, compute_resource_id, workspace_name=None, resource_group_name=None):
    _attach_compute_internal(name, compute_resource_id, DataFactoryCompute, workspace_name, resource_group_name)


def attach_databricks(name, access_token, compute_resource_id, workspace_name=None, resource_group_name=None):
    workspace = get_workspace_or_default(workspace_name, resource_group_name)

    print('Attaching compute resource...')
    DatabricksCompute.attach(workspace, name, compute_resource_id, access_token)
    print('Resource attach submitted successfully.')
    print('To see if your compute target is ready to use, run:')
    print('  az ml computetarget show -n {}'.format(name))


def attach_adla(name, compute_resource_id, workspace_name=None, resource_group_name=None):
    _attach_compute_internal(name, compute_resource_id, AdlaCompute, workspace_name, resource_group_name)


def _attach_compute_internal(name, compute_resource_id, compute_type, workspace_name=None, resource_group_name=None):
    workspace = get_workspace_or_default(workspace_name=workspace_name, resource_group=resource_group_name)

    print('Attaching compute resource...')
    compute_type.attach(workspace, name, compute_resource_id)
    print('Resource attach submitted successfully.')
    print('To see if your compute target is ready to use, run:')
    print('  az ml computetarget show -n {}'.format(name))


# The function takes an input from a user.
# prompt_message denotes a string, which is printed at the command prompt before
# a user enters the information.
# hide=False means the entered text will be echoed on the terminal.
# The function returns the entered text or raises an error in case of an incorrect input.
def _get_user_input(prompt_message, hide=False, allow_empty=False):
    if hide:
        return _password_input(prompt_message, allow_empty)
    else:
        return _text_input(prompt_message, allow_empty)


# The function takes a password as input from the current terminal.
# Takes as input a string that it displays to a user for entering a password.
# Prompts a user for password two times so that any password entering typos can be reduced.
def _password_input(prompt_message, allow_empty=False):
    password_1 = getpass.getpass(prompt_message)
    if len(password_1) <= 0 and not allow_empty:
        raise UserErrorException("Empty password not allowed. Please try again.")

    password_2 = getpass.getpass("Re-enter the password for confirmation:")
    if password_1 == password_2:
        return password_1
    else:
        raise UserErrorException("Entered passwords don't match. Please try again.")


# The function takes a text as input from the current terminal.
# Takes as input a string that it displays to a user for entering a text.
# Prompts a user for a text two times so that any text entering typos can be reduced.
# The text that user enters is displayed on the terminal.
def _text_input(prompt_message, allow_empty=False):
    text_1 = input(prompt_message)
    if len(text_1) <= 0 and not allow_empty:
        raise UserErrorException("Empty value not allowed. Please try again.")

    text_2 = input("Re-enter the value for confirmation:")
    if text_1 == text_2:
        return text_1
    else:
        raise UserErrorException("Entered values don't match. Please try again.")


# Prints the status messages on the terminal for the compute_target attach command before returning to user.
def _get_attach_status(compute_target_name, prepare_required=True):
    """
    Returns attach status as an object of CLICommandOutput.
    :param compute_target_name:
    :param prepare_required:
    :return: an object of CLICommandOutput, which contains the status.
    :rtype: CLICommandOutput
    """
    command_output = CLICommandOutput("")
    command_output.append_to_command_output("Successfully created the following files:")

    command_output.append_to_command_output("{name}{compute_extension}: contains connection and configuration "
                                            "information for a remote execution "
                                            "target".format(name=compute_target_name,
                                                            compute_extension=COMPUTECONTEXT_EXTENSION))

    command_output.append_to_command_output(
        "{name}{runconfiguration_extension}: set of run options used when executing within the Azure ML "
        "Workbench application".format(name=compute_target_name,
                                       runconfiguration_extension=RUNCONFIGURATION_EXTENSION))

    if prepare_required:
        command_output.append_to_command_output("")
        command_output.append_to_command_output("Before running against {name}, you need to prepare it with "
                                                "your project's environment by "
                                                "running:".format(name=compute_target_name))

        command_output.append_to_command_output("az ml experiment prepare -c {name}".format(name=compute_target_name))

    command_output.set_do_not_print_dict()
    return command_output
