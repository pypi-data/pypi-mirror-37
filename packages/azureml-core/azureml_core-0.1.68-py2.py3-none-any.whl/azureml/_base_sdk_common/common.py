# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

""" base_sdk_common.py, A file for storing commonly-used functions."""
from __future__ import print_function

import json
import os
import re
import sys
import uuid
import warnings
import jwt

from azureml.exceptions import ProjectSystemException
from azureml.exceptions import UserErrorException

TOKEN_EXPIRE_TIME = 5 * 60
AZ_CLI_AAP_ID = '04b07795-8ddb-461a-bbee-02f9e1bf7b46'
AML_WORKBENCH_CLI_CALLER = "AML_WORKBENCH_CLI_CALLER"

# EXTENSIONS AND FILE NAMES
RUNCONFIGURATION_EXTENSION = '.runconfig'
COMPUTECONTEXT_EXTENSION = '.compute'
YAML_EXTENSION = '.yml'
AML_CONFIG_DIR = "aml_config"
TEAM_FILENAME = '.team'
ACCOUNT_FILENAME = 'runhistory'

# ARM RELATED CONSTANTS
ARM_ACCOUNT_DATA = "ARM_TEAM"
TEAM_LIST_OF_KEYS = {"subscriptions", "resourceGroups", "accounts", "workspaces"}
TEAM_DEFAULT_KEY = "id"
ACCOUNT_DEFAULT_KEY = "default"
CORRELATION_ID = None

# Environment variable names related to arm account token and user's email address.
# UX or any other service can set these environment variables in the python
# environment then the code uses values of these variables
AZUREML_ARM_ACCESS_TOKEN = "AZUREML_ARM_ACCESS_TOKEN"

# The subscription id environment variable. Mainly used for project commands.
AZUREML_SUBSCRIPTION_ID = "AZUREML_SUBSCRIPTION_ID"

# Environment variable for tenant id, mainly required for flighting.
AZUREML_TENANT_ID = "AZUREML_TENANT_ID"


# Default resource group location.
# Currently, supported locations are: australiaeast, eastus2, westcentralus, southeastasia, westeurope, eastus2euap
# TODO: Should be changed to eastus

# If we are running this code from source then we use default region as eastus2euap
if os.path.abspath(__file__).endswith(
        os.path.join("src", "azureml-core", "azureml", "_base_sdk_common", "common.py")):
    DEFAULT_RESOURCE_LOCATION = "eastus2euap"
else:
    DEFAULT_RESOURCE_LOCATION = "eastus2"


# FILE LOCATIONS
if 'win32' in sys.platform:
    USER_PATH = os.path.expanduser('~')
    # TODO Rename CREDENTIALS_PATH since there aren't credentials there anymore.
    CREDENTIALS_PATH = os.path.join(USER_PATH, ".azureml")
else:
    USER_PATH = os.path.join(os.getenv('HOME'), '.config')
    CREDENTIALS_PATH = os.path.join(os.getenv('HOME'), '.azureml')


def normalize_windows_paths(path):
    if not path:
        return path
    if os.name == "nt":
        return path.replace("\\", "/")

    return path


# PROJECT RELATED METHODS


def _valid_workspace_name(workspace_name):
    """Check validity of workspace name"""
    if not workspace_name:
        return False
    return re.match("^[a-zA-Z0-9][\w\-]{2,32}$", workspace_name)


def fetch_tenantid_from_aad_token(token):
    # We set verify=False, as we don't have keys to verify signature, and we also don't need to
    # verify signature, we just need the tenant id.
    decode_json = jwt.decode(token, verify=False)
    return decode_json['tid']


def check_valid_resource_name(resource_name, resource_type):
    """
    Checks if the resource name is valid.
    If it is non valid then we throw UserErrorException.
    :param resource_name: The resource name.
    :type resource_name: str
    :param resource_type: The resource type like Workspace or History.
    :type resource_type: str
    :return:
    :rtype: None
    """
    message = "{} name must be between 3 and 33 characters long. " \
              "Its first character has to be alphanumeric, and " \
              "the rest may contain hyphens and underscores.".format(resource_type)
    if not _valid_workspace_name(resource_name):
        raise UserErrorException(message)


def graph_client_factory(**_):
    from azure.cli.core._profile import Profile
    from azure.cli.core.cloud import get_active_cloud

    # TODO: May not work with all auths.
    from azure.graphrbac import GraphRbacManagementClient
    profile = Profile()
    cred, _, tenant_id = profile.get_login_credentials(
        resource=get_active_cloud().endpoints.active_directory_graph_resource_id)
    client = GraphRbacManagementClient(cred,
                                       tenant_id,
                                       base_url=get_active_cloud().endpoints.active_directory_graph_resource_id)

    return client


def auth_client_factory(auth, scope=None):
    """
    :param auth: auth object
    :type auth: azureml.core.authentication.AbstractAuthentication
    :param scope:
    :return:
    """
    import re
    from azure.mgmt.authorization import AuthorizationManagementClient
    subscription_id = None
    if scope:
        matched = re.match('/subscriptions/(?P<subscription>[^/]*)/', scope)
        if matched:
            subscription_id = matched.groupdict()['subscription']
    return auth._get_service_client(AuthorizationManagementClient, subscription_id=subscription_id)


# pylint:disable=too-many-arguments
def _resolve_role_id(role, scope, definitions_client):
    """
    # TODO: Types of input parameters.
    :param role:
    :param scope:
    :param definitions_client:
    :return:
    """
    role_id = None
    if re.match(r'/subscriptions/.+/providers/Microsoft.Authorization/roleDefinitions/',
                role, re.I):
        role_id = role
    else:
        try:
            # try to parse role as a guid, if fails then try to retrieve it
            uuid.UUID(role)
            role_id = '/subscriptions/{}/providers/Microsoft.Authorization/roleDefinitions/{}'.format(
                definitions_client.config.subscription_id, role)
        except ValueError:
            pass
        if not role_id:  # retrieve role id
            role_defs = list(definitions_client.list(scope, "roleName eq '{}'".format(role)))
            if not role_defs:
                raise ProjectSystemException("Role '{}' doesn't exist.".format(role))
            elif len(role_defs) > 1:
                ids = [r.id for r in role_defs]
                err = "More than one role matches the given name '{}'. Please pick a value from '{}'"
                raise ProjectSystemException(err.format(role, ids))
            role_id = role_defs[0].id
    return role_id


def _build_role_scope(resource_group_name, scope, subscription_id):
    subscription_scope = '/subscriptions/' + subscription_id
    if scope:
        if resource_group_name:
            err = 'Resource group "{}" is redundant because scope is supplied'
            raise ProjectSystemException(err.format(resource_group_name))
    elif resource_group_name:
        scope = subscription_scope + '/resourceGroups/' + resource_group_name
    else:
        scope = subscription_scope
    return scope


def _get_object_stubs(graph_client, assignees):
    from azure.graphrbac.models import GetObjectsParameters
    params = GetObjectsParameters(include_directory_object_references=True,
                                  object_ids=assignees)
    return list(graph_client.objects.get_objects_by_object_ids(params))


def _resolve_object_id(assignee):
    """
    TODO: assignee type
    :param assignee:
    :return:
    """
    client = graph_client_factory()
    result = None
    if assignee.find('@') >= 0:  # looks like a user principal name
        result = list(client.users.list(filter="userPrincipalName eq '{}'".format(assignee)))
    if not result:
        result = list(client.service_principals.list(
            filter="servicePrincipalNames/any(c:c eq '{}')".format(assignee)))
    if not result:  # assume an object id, let us verify it
        result = _get_object_stubs(client, [assignee])

    # 2+ matches should never happen, so we only check 'no match' here
    if not result:
        raise ProjectSystemException("No matches in graph database for '{}'".format(assignee))

    return result[0].object_id


def create_role_assignment(auth, role, assignee, resource_group_name=None, scope=None,
                           resolve_assignee=True):
    """
    :param auth: auth object
    :type auth: azureml.core.authentication.AbstractAuthentication
    :param role:
    :param assignee:
    :param resource_group_name:
    :param scope:
    :param resolve_assignee:
    :return:
    """
    factory = auth_client_factory(auth, scope)
    assignments_client = factory.role_assignments
    definitions_client = factory.role_definitions

    scope = _build_role_scope(resource_group_name, scope,
                              assignments_client.config.subscription_id)

    role_id = _resolve_role_id(role, scope, definitions_client)
    object_id = _resolve_object_id(assignee) if resolve_assignee else assignee
    from azure.mgmt.authorization.models import RoleAssignmentCreateParameters
    properties = RoleAssignmentCreateParameters(role_definition_id=role_id, principal_id=object_id)
    assignment_name = uuid.uuid4()
    custom_headers = None
    return assignments_client.create(scope, assignment_name, properties,
                                     custom_headers=custom_headers)


def resource_error_handling(response_exception, resource_type):
    """General error handling for projects"""
    if response_exception.response.status_code == 404:
        raise ProjectSystemException("{resource_type} not found.".format(resource_type=resource_type))
    else:
        response_message = get_http_exception_response_string(response_exception.response)
        raise ProjectSystemException(response_message)


def resource_client_factory(auth, subscription_id):
    """
    Returns the azure SDK resource management client.
    :param auth: auth object
    :type auth: azureml.core.authentication.AbstractAuthentication
    :param subscription_id:
    :type subscription_id: str
    :return:
    :rtype: azure.mgmt.resource.resources.ResourceManagementClient
    """
    from azure.mgmt.resource.resources import ResourceManagementClient
    return auth._get_service_client(ResourceManagementClient, subscription_id)


def storage_client_factory(auth, subscription_id):
    """
    Returns the azure SDK storage management client.
    :param auth: auth object
    :type auth: azureml.core.authentication.AbstractAuthentication
    :param subscription_id:
    :type subscription_id: str
    :return:
    :rtype: azure.mgmt.resource.resources.StorageManagementClient
    """
    from azure.mgmt.storage import StorageManagementClient
    return auth._get_service_client(StorageManagementClient, subscription_id)


def get_project_id(project):
    """Gets project id from metadata"""
    project = os.path.join(os.path.dirname(os.getcwd()), '.ci')

    with open(os.path.join(project, 'metadata'), 'r') as file:
        metadata = json.load(file)

    if 'Id' in metadata:
        return metadata['Id']
    else:
        raise ValueError('No project id found.')

# COMMAND RELATED METHODS


def create_common_argument(command_list, argument_name, argument_longcut,
                           argument_shortcut, argument_help):
    "Register base_sdk_common arguments for multiple commands"
    from azure.cli.core.commands import register_cli_argument
    for names in command_list:
        register_cli_argument(
            names,
            argument_name,
            options_list=(
                argument_longcut,
                argument_shortcut),
            help=argument_help)


def set_config_dir():
    """Get home directory"""
    if not os.path.exists(CREDENTIALS_PATH):
        os.makedirs(CREDENTIALS_PATH)

# ARM RELATED METHODS


def check_for_keys(key_list, dictionary):
    """Checks if all keys are present in dictionary"""
    return True if all(k in dictionary for k in key_list) else False


def update_engine_account(account_id):
    """Tries to call Engine to update account information"""
    try:
        # Make Engine call, pass if cannot make it (means not calling from within Azure ML Workbench app)
        from vienna.Account import Account
        Account.create_account(account_id, ACCOUNT_DEFAULT_KEY)
    except ImportError:
        print("Command must be ran from within the application's shell for account information to be updated")
    except RuntimeError as e:
        print(e)
        os._exit(0)


# CLI FUNCTIONALITY RELATED METHODS


def set_correlation_id():
    """Set telemetry correlation data with application information and newly-created correlation id"""
    global CORRELATION_ID
    CORRELATION_ID = uuid.uuid4()
    user = "user"
    if AML_WORKBENCH_CLI_CALLER in os.environ:
        user = os.environ[AML_WORKBENCH_CLI_CALLER]

    from azure.cli.core.telemetry import set_module_correlation_data
    set_module_correlation_data(str(CORRELATION_ID) + ' ' + user)


def to_snake_case(input_string):
    """
    Converts a string into a snake case.
    :param input_string: Input string
    :return: Snake case string
    :rtype: str
    """
    final = ''
    for item in input_string:
        if item.isupper():
            final += "_"+item.lower()
        else:
            final += item
    if final[0] == "_":
        final = final[1:]
    return final


def to_title_case(input_string):
    camel_case = to_camel_case(input_string)
    title_case = camel_case[0].upper() + camel_case[1:]
    return title_case


def to_camel_case(snake_str):
    """
    Converts snake case and title case to camelCase.
    :param snake_str:
    :return:
    """
    components = snake_str.split('_')
    # We capitalize the first letter of each component except the first one
    # with the 'title' method and join them together.
    # We also just explicitly change the first character to lowercase, in case it is not, especially
    # in title case.
    return components[0][0].lower() + components[0][1:] + "".join(x.title() for x in components[1:])


def convert_dict_keys_to_camel_case(input_dict):
    return {to_camel_case(k): v for k, v in input_dict.items()}


def get_project_files(path, suffix):
    """
    Returns all project config files with the specified suffix.
    :param path:
    :type path: str
    :param suffix:
    :type suffix: str
    :return: TODO
    :rtype: dict
    """
    targets = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(suffix):
                targets.append(os.path.relpath(os.path.join(root, file), path))
    return {os.path.splitext(os.path.basename(x))[0]: x for x in targets}


def give_warning(warning_message):
    # A custom formatter, so that we don't print the ugly full file path
    # in the userfacing warning.

    def custom_formatwarning(message, category, filename, lineno, line=None):
        # Ignore everything except the message
        return str(message) + '\n'

    original_formatter = warnings.formatwarning
    warnings.formatwarning = custom_formatwarning
    warnings.warn(warning_message, UserWarning)
    warnings.formatwarning = original_formatter


def get_http_exception_response_string(http_response):
    """
    Takes a http_response and returns a json formatted string with
    appropriate fields.
    :param http_response:
    :type http_response: requests.Response
    :return:
    :rtype: str
    """
    error_dict = dict()
    error_dict["url"] = http_response.url
    error_dict["status_code"] = http_response.status_code
    if http_response.text:
        try:
            # In case response is a json, which is the usual case with service responses.
            error_dict["error_details"] = remove_empty_values_json(http_response.json())
        except BaseException:
            # Response is not a json, so we just add that as text.
            error_dict["error_details"] = http_response.text
    return json.dumps(error_dict, indent=4, sort_keys=True)


def remove_empty_values_json(data):
    try:
        if not isinstance(data, (dict, list)):
            return data
        if isinstance(data, list):
            return [v for v in (remove_empty_values_json(v) for v in data) if v]
        return {k: v for k, v in ((k, remove_empty_values_json(v)) for k, v in data.items()) if v}
    except BaseException:
        return data


class CLICommandError(object):
    # TODO: This class needs to be removed or merged with our new excepion classes
    """
    A class for returning a error for a CLI command. This class is mainly used
    when an error is not because of a service request. In the case of service errors, we
    directly return the error json returned by a service.
    """
    def __init__(self, error_type, error_message, stack_trace=None, **kwargs):
        """
        CLICommandError constructor.
        :param error_type: Type of error like UserError, FormattingError etc.
        :param error_message: Error message.
        :param stack_trace: Stack trace if available.
        :param kwargs: A dictionary of any other key-value pairs to include in the error message.
        :type error_type: str
        :type error_message: str
        :type stack_trace: str
        :type kwargs: dict
        """
        self._error_type = error_type
        self._error_message = error_message
        self._stack_trace = stack_trace
        self._kwargs = kwargs

    def get_json_dict(self):
        """
        Serializes the object into a dictionary, which can be printed as a JSON object.
        :return: A dictionary representation of this object.
        :rtype: dict
        """
        error_dict = {"errorType": self._error_type, "errorMessage": self._error_message}

        if self._stack_trace:
            error_dict["stackTrace"] = self._stack_trace

        if self._kwargs:
            for key, value in self._kwargs.items():
                error_dict[key] = value

        return error_dict


class CLICommandOutput(object):
    # TODO: This class also needs to be removed, and sdk methods should return specific
    # return types.
    """
    A class for returning a command output for a CLI command.
    """

    def __init__(self, command_output):
        """
        CLICommandOutput constructor.
        :param command_output: Output of a command. command_output can contain
        multiple lines separated by \n
        :type command_output: str
        """
        self._command_output = command_output
        self._dict_to_merge = None
        self._do_not_print_dict = False

    def get_json_dict(self, exclude_command_output=False):
        """
        Serializes the object into a dictionary, which can be printed as a JSON object.
        :param exclude_command_output: exclude_command_output=True, excludes the commandOutput key from
        the returned dictionary.
        :return: A dictionary representation of this object.
        :rtype: dict
        """
        if self._dict_to_merge:
            if not exclude_command_output:
                self._dict_to_merge["commandOutput"] = self._command_output

            return self._dict_to_merge
        else:
            if exclude_command_output:
                return {}
            else:
                output_dict = {"commandOutput": self._command_output}
                return output_dict

    def append_to_command_output(self, lines_to_append):
        """
        Appends lines to the command output.
        Basically, this function does _command_output=_command_output+"\n"+lines_to_append
        :param lines_to_append:
        :return: None
        """
        if len(self._command_output) > 0:
            self._command_output = self._command_output + "\n" + lines_to_append
        else:
            self._command_output = lines_to_append

    def merge_dict(self, dict_to_merge):
        """
        Merges dict_to_merge with the overall dict returned by get_json_dict.
        Basically, we merge the dict returned by a service with the CLI command output.
        The actual merge happens when get_json_dict is called.
        :param dict_to_merge:
        :return:
        """
        import copy
        self._dict_to_merge = copy.deepcopy(dict_to_merge)

    def get_command_output(self):
        """
        :return: Returns the command output.
        :rtype: str
        """
        return self._command_output

    def set_do_not_print_dict(self):
        """
        Set the flag to not print dict. Sometimes, in az CLI commands, we set the output in
        self._command_output in pretty format, and don't want to print the whole dict.
        :return:
        """
        self._do_not_print_dict = True

    def get_do_not_print_dict(self):
        """
        Returns True if az CLI should not print the output in dict/JSONObject format.
        :return:
        :rtype bool:
        """
        return self._do_not_print_dict
