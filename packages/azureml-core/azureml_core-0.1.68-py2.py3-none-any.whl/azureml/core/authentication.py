# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

""" authentication.py for managing authentication for azureml"""
import base64
import json
import logging
import os
import time
import threading
import jwt


from abc import ABCMeta, abstractmethod

import collections
from azureml.core.util import NewLoggingLevel
from azureml.exceptions import AuthenticationException, UserErrorException
from azureml._base_sdk_common.common import fetch_tenantid_from_aad_token

SubscriptionInfo = collections.namedtuple("SubscriptionInfo", "subscription_name subscription_id")

module_logger = logging.getLogger(__name__)


class AbstractAuthentication(object):
    """
    An abstract class for all authentication classes. All derived classes provide different means
    to authenticate the user and acquire a valid access token.
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_authentication_header(self):
        """
        Returns the HTTP authorization header. The authorization header contains the user access token
        for access authorizaton against the service.

        :return: Returns the HTTP authorization header.
        :rtype: dict
        """
        pass

    @abstractmethod
    def _get_arm_token(self):
        pass

    @abstractmethod
    def _get_all_subscription_ids(self):
        """
        Returns a list of subscriptions that are accessible through this authentication.
        :return: Returns a list of SubscriptionInfo named tuples.
        :rtype: list
        """
        pass

    @abstractmethod
    def _perform_subscription_check(self, subscription_id):
        """
        Checks if the auth has access to the provided subscription id.
        If auth doesn't have access then azureml.exceptions.AuthenticationException is thrown.
        :param subscription_id:
        :type subscription_id: str
        :return: None if successful
        :rtype: None
        """
        pass

    @abstractmethod
    def _get_service_client(self, client_class, subscription_id, subscription_bound=True, base_url=None):
        """
        Creates and returns a service client object for client_class using subscription_id and auth token.
        :param client_class:
        :type client_class: object
        :param subscription_id:
        :type subscription_id: str
        :param subscription_bound: True if a subscription id is required to construct the client. Only False for
        1 RP clients.
        :type subscription_bound: bool
        :param base_url: The specified base URL client should use, usually differs by region
        :type base_url: str
        :return:
        :rtype: client_class
        """
        pass

    def signed_session(self, session=None):
        """
        Adds the authorization header as a persisted header on an HTTP session.
        Any new requests sent by the session will contain the authorization header.

        :param session: HTTP session that will have the authorization header as a default persisted header.
            When None a new session will be created.
        :type session: requests.session:
        :return: Returns the HTTP session after the update.
        :rtype: requests.session
        """
        from requests import Session
        session = session or Session()
        session.headers.update(self.get_authentication_header())
        return session


# We are using locks because in some cases like hyperdrive this
# function gets called in parallel, which initiates multiple
# "az login" at once.
# TODO: This needs to be made non-static.
# Currently we are not sure if it is a parallelism issue or multiple auth objects.
# So, going with static global lock.
_interactive_auth_lock = threading.Lock()


def _login_on_failure_decorator():
    """
    This decorator performs az login on failure of the actual function
    and retries the actual function one more time.

    Notebooks are long running processes, like people open them and then never close them.
    So, on InteractiveLoginAuthentication object, auth._get_arm_token etc functions can throw
    error if the arm token and refresh token both have expired, and this will prompt a
    user to run "az login" outside the notebook. So, we use this decorator on every function
    of InteractiveLoginAuthentication to catch the first failure, perform "az login" and retry the
    function.

    We also use Profile(async_persist=False), so that tokens are persisted and re-used on-disk.
    async_persist=True (default), az CLI only persists tokens on the process exit, which just never
    happens in a notebook case, in turn requiring users to perform "az login" outside notebooks.
    :return:
    :rtype: object
    """
    def actual_decorator(test_function):
        """
        :param test_function:
        :type test_function: object
        :return: Returns the wrapper.
        :rtype: object
        """
        def wrapper(self, *args, **kwargs):
            """
            :param args:
            :type args: list
            :param kwargs:
            :type kwargs: dict
            :return: Returns the test function.
            :rtype: object
            """
            try:
                _interactive_auth_lock.acquire()
                return test_function(self, *args, **kwargs)
            except Exception:
                # Perform InteractiveLoginAuthentication and try one more time.
                InteractiveLoginAuthentication(force=True)
                # Try one more time
                return test_function(self, *args, **kwargs)
            finally:
                _interactive_auth_lock.release()
        return wrapper

    return actual_decorator


class InteractiveLoginAuthentication(AbstractAuthentication):
    """
    This class authenticates the user to acquire the user's access token. The access token is used for authorization.

    .. remarks::

        The constructor of the class will prompt the user to login. The constructor then will save the credentials for any subsequent attempts.
        If the user is already logged in to azure CLI or have logged-in before, the constructor will load the existing credentials without prompt.

        When this python process is running in Azure Notebook service, the constructor will attempt to use the "connect to azure" feature in Azure Notebooks.
    """
    # TODO: This authentication mechanism should use the azureml application ID while
    # authenticating with ARM, rather than the az CLI application ID.

    # TODO: This should also persist state separately from .azure directory, so we need to
    # implement the state saving mechanism in a thread-safe manner using locking.

    def __init__(self, force=False, tenant_id=None):
        """
        This constructor will prompt the user to login, then it will save the credentials for any subsequent attempts.
        If the user is already logged in to azure CLI  or have logged in before, the constructor will load the existing credentials without prompt.
        When this python process is running in Azure Notebook service, the constructor will attempt to use the "connect to azure" feature in Azure Notebooks.

        :param force: If force=True, then "az login" will be run even if the old "az login" is still valid.
        :type force: bool
        :param tenant_id: Tenant id to login into, if a user has access to multiple tenants then the user can
        specify a tenant to login into. If unspecified, default tenant will be used.
        :type tenant_id: str
        """
        # TODO: This is just based on az login for now.
        # This all will need to change and made az CLI independent.

        self._auth = None
        if "MSI_ENDPOINT" in os.environ:
            # MSI_ENDPOINT is always set by Azure Notebooks, so if the MSI_ENDPOINT env var
            # is set, we will try to create an MsiAuthentication object.
            try:
                self._auth = MsiAuthentication()
                # make sure we can get an arm token through msi to validate the auth object.
                arm_token = self._auth._get_arm_token()
                # If a user has specified a tenant id then we need to check if this token is for that tenant.
                if tenant_id and fetch_tenantid_from_aad_token(arm_token) != tenant_id:
                    raise UserErrorException("The tenant in the MSI authentication is different "
                                             "than the user specified tenant.")
            except Exception as e:
                # let it fail silently and move on to AzureCliAuthentication as users on
                # Azure Notebooks may want to use the credentials from 'az login'.
                module_logger.debug(e)
                self._auth = None

        if self._auth is None:
            self._auth = AzureCliAuthentication()
            need_to_login = False
            # This prevents redundant az logins.
            try:
                # If we can get a valid ARM token, then we don't need to login.
                arm_token = self._auth._get_arm_token()
                # If a user has specified a tenant id then we need to check if this token is for that tenant.
                if tenant_id and fetch_tenantid_from_aad_token(arm_token) != tenant_id:
                    raise UserErrorException("The tenant in the az CLI authentication is different "
                                             "than the user specified tenant.")
            except Exception:
                need_to_login = True

            if need_to_login or force:
                print("Performing interactive authentication. Please follow the instructions "
                      "on the terminal.")
                # TODO: We should mimic the az CLI login mechanism with azureml application ID.
                # and the credentials should also be cached somewhere.
                from azure.cli.command_modules.profile import custom as az_cli_custom

                # A hack to make the az login function work.
                class DummyCommandLoader(object):
                    @property
                    def cli_ctx(self):
                        return None

                # TODO: This function should be removed from here, and the relevant code should be copied.
                # Otherwise, az CLI changes can easily break this code.
                az_cli_custom.login(DummyCommandLoader(), tenant=tenant_id)
                print("Interactive authentication successfully completed.")

    @_login_on_failure_decorator()
    def get_authentication_header(self):
        """
        Returns the HTTP authorization header. The authorization header contains the user access token
        for access authorizaton against the service.

        :return: Returns the HTTP authorization header.

        :rtype: dict
        """
        return self._auth.get_authentication_header()

    @_login_on_failure_decorator()
    def _get_arm_token(self):
        """
        :return: Returns the arm access token.
        :rtype: str
        """
        return self._auth._get_arm_token()

    @_login_on_failure_decorator()
    def _get_all_subscription_ids(self):
        """
        Returns a list of subscriptions that are accessible through this authentication.
        :return: Returns a list of SubscriptionInfo named tuples.
        :rtype: list
        """
        return self._auth._get_all_subscription_ids()

    @_login_on_failure_decorator()
    def _perform_subscription_check(self, subscription_id):
        """
        Checks if the auth has access to the provided subscription id.
        If auth doesn't have access then azureml.exceptions.AuthenticationException is thrown.
        :param subscription_id:
        :type subscription_id: str        
        :return: None if successful
        :rtype: None
        """
        # TODO: Don't call self._get_all_subscription_ids(), that will cause a deadlock because of locking that
        # we are doing.
        all_subscription_list = self._auth._get_all_subscription_ids()
        if not _check_if_subscription_exists(subscription_id, all_subscription_list):
            raise AuthenticationException("You don't have access to {} subscription. All the subscriptions "
                                          "that you have access to = {}. ".format(subscription_id,
                                                                                  all_subscription_list))

    @_login_on_failure_decorator()
    def _get_service_client(self, client_class, subscription_id, subscription_bound=True, base_url=None):
        """
        Creates and returns a service client object for client_class using subscription_id and auth token.
        :param client_class:
        :type client_class: object
        :param subscription_id:
        :type subscription_id: str
        :param subscription_bound: True if a subscription id is required to construct the client. Only False for
        1 RP clients.
        :type subscription_bound: bool
        :param base_url: The specified base URL client should use, usually differs by region
        :type base_url: str
        :return:
        :rtype: client_class
        """
        return self._auth._get_service_client(client_class, subscription_id,
                                              subscription_bound=subscription_bound, base_url=base_url)


class AzureCliAuthentication(AbstractAuthentication):
    """
        The class used internally to prompt the user for login.
        It's preferable to use :class:`azureml.core.authentication.InteractiveLoginAuthentication` for better Azure Notebooks experience.
    """

    def get_authentication_header(self):
        """
        Returns the HTTP authorization header. The authorization header contains the user access token
        for access authorizaton against the service.

        :return: Returns the HTTP authorization header.
        :rtype: dict
        """
        # We return a new dictionary each time, as some functions modify the headers returned
        # by this function.
        auth_header = {"Authorization": "Bearer " + self._get_arm_token()}
        return auth_header

    def _get_default_subscription_id(self):
        """
        :return: Returns the default subscription id.
        :rtype: str
        """
        self._load_azure_info()
        from azure.cli.core.commands.client_factory import get_subscription_id
        from azure.cli.core import get_default_cli
        return get_subscription_id(get_default_cli())

    def _get_arm_token(self):
        """
        Fetches a valid ARM token using azure API calls.
        :return: Arm access token.
        :rtype: str
        """

        # Update token if it expires in < TOKEN_REFRESH_THRESHOLD_SEC
        TOKEN_REFRESH_THRESHOLD_SEC = 5 * 60

        # TODO: not sure what this hard coded value is.
        AZ_CLI_AAP_ID = '04b07795-8ddb-461a-bbee-02f9e1bf7b46'

        from azure.cli.core._profile import Profile
        from azure.cli.core.cloud import get_active_cloud
        self._load_azure_info()

        # From notebook, we want to persist tokens synchronously to the on-disk file,
        # so that users don't have to run az login multiple times.
        # By default, a tokens are persisted on-disk on exit on a process, which
        # doesn't happen in notebook or happens in a way where token persistence logic
        # is not called.
        profile = Profile(async_persist=False)
        token_about_to_expire = False
        try:
            auth, _, _ = profile.get_login_credentials()
            access_token = auth._token_retriever()[1]
            if (self._get_exp_time(access_token) - time.time()) < TOKEN_REFRESH_THRESHOLD_SEC:
                # Token is about to expire, do not return, request a new one
                token_about_to_expire = True
            else:
                return access_token
        except Exception:
            if not token_about_to_expire:
                raise AuthenticationException("Could not retrieve user token. Please run 'az login'")

        try:
            # This call fails when AZ cli is run in parallel
            user_type = profile.get_subscription()['user']['type']
            if user_type == "user":
                _, refresh_token, access_token, tenant = profile.get_refresh_token()
                if (self._get_exp_time(access_token) - time.time()) < TOKEN_REFRESH_THRESHOLD_SEC:
                    authority = get_active_cloud().endpoints.active_directory
                    if authority[-1] == '/':
                        authority = authority[:-1]

                    # Note: Moved adal import from the beginning of the file to here.
                    # This import takes 0.25 s, so we move it close the the place where
                    # it is used, rather than slowing down other functions that don't use this.
                    import adal
                    context = adal.AuthenticationContext('{0}/{1}'.format(authority, tenant), api_version=None)
                    from adal import ADAL_LOGGER_NAME
                    with NewLoggingLevel(ADAL_LOGGER_NAME, level=logging.WARNING) as warn_logger:
                        adal_token = context.acquire_token_with_refresh_token(
                            refresh_token, AZ_CLI_AAP_ID, get_active_cloud().endpoints.management)
                        token = adal_token['accessToken']
                else:
                    token = access_token
                return token
            else:
                resource = get_active_cloud().endpoints.management
                creds, subscription, tenant = profile.get_raw_token(resource, None)
                token_dict = {
                    'tokenType': creds[0],
                    'accessToken': creds[1],
                    'expiresOn': creds[2]['expiresOn'],
                    'subscription': subscription,
                    'tenant': tenant
                }
                if (token_dict["expiresOn"] - time.time()) < TOKEN_REFRESH_THRESHOLD_SEC:
                    auth, _, _ = profile.get_login_credentials()
                    access_token = auth._token_retriever()[1]
                    return access_token
                return token_dict["accessToken"]

        except Exception:
            raise AuthenticationException("Could not retrieve user token. Please run 'az login'")

    def _get_exp_time(self, access_token):
        """
        Returns the expiry time of the supplied arm access token.
        :param access_token:
        :type access_token: str
        :return:
        :rtype: time
        """
        # We set verify=False, as we don't have keys to verify signature, and we also don't need to
        # verify signature, we just need the expiry time.
        decode_json = jwt.decode(access_token, verify=False)
        return decode_json['exp']

    def _load_azure_info(self):
        """
        Loads the azure account, config and session info. This is needed when we call az.cli.core modules/submodules
        without issuing an az CLI command.
        """
        # Hack to make this work outside the Azure CLI.
        from azure.cli.core._session import ACCOUNT, CONFIG, SESSION
        from azure.cli.core._environment import get_config_dir

        if not ACCOUNT.data:
            ACCOUNT.load(os.path.join(get_config_dir(), 'azureProfile.json'))
            CONFIG.load(os.path.join(get_config_dir(), 'az.json'))
            # TODO: Is 3600 s ARM specified limit or our limit.
            SESSION.load(os.path.join(get_config_dir(), 'az.sess'), max_age=3600)

    def _get_all_subscription_ids(self):
        """
        Returns a list of subscriptions that are accessible through this authentication.
        :return: Returns a list of SubscriptionInfo named tuples.
        :rtype: list
        """
        from azure.cli.core._profile import Profile
        from azureml._base_sdk_common.common import fetch_tenantid_from_aad_token
        profile = Profile(async_persist=False)
        # This is a CLI authentication, so we are just calling simple CLI methods
        # for getting subscriptions.

        all_subscriptions = profile.load_cached_subscriptions()
        result = []
        token_tenant_id = fetch_tenantid_from_aad_token(self._get_arm_token())

        for subscription_info in all_subscriptions:

            # Az CLI returns subscriptions for all tenants, but we want subscriptions
            # that a user has access to using the current arm token for the tenant. So we
            # filter based on tenant id.
            # There are some subscriptions from windows azure time that don't have
            # tenant id for them, so we ignore tenantId check for them.
            if "tenantId" not in subscription_info or \
                    subscription_info["tenantId"].lower() == token_tenant_id.lower():
                subscription_tuple = SubscriptionInfo(subscription_info['name'],
                                                      subscription_info['id'])
                result.append(subscription_tuple)
        return result

    def _perform_subscription_check(self, subscription_id):
        """
        Checks if the auth has access to the provided subscription id.
        If auth doesn't have access then azureml.exceptions.AuthenticationException is thrown.
        :param subscription_id:
        :type subscription_id: str        
        :return: None if successful
        :rtype: None
        """
        all_subscription_list = self._get_all_subscription_ids()
        if not _check_if_subscription_exists(subscription_id, all_subscription_list):
            raise AuthenticationException("You don't have access to {} subscription. All the subscriptions "
                                          "that you have access to = {}. Please run 'az login' or set {} as default "
                                          "subscription and retry.".format(subscription_id, all_subscription_list,
                                                                           subscription_id))

    def _get_service_client(self, client_class, subscription_id, subscription_bound=True, base_url=None):
        """
        Creates and returns a service client object for client_class using subscription_id and auth token.
        :param client_class:
        :type client_class: object
        :param subscription_id:
        :type subscription_id: str
        :param subscription_bound: True if a subscription id is required to construct the client. Only False for
        1 RP clients.
        :type subscription_bound: bool
        :param base_url: The specified base URL client should use, usually differs by region
        :type base_url: str
        :return:
        :rtype: client_class
        """
        # Checks if auth has access to the provided subscription.
        if subscription_id:
            self._perform_subscription_check(subscription_id)

        # We don't use az CLI methods to get a service client because in multi-tenant case, based on a subscription
        # az CLI code changes the arm token while getting a service client, which means that
        # the arm token that this auth object has differs from the arm token in the service client
        # in the multi-tenant case, which causes confusion.
        return _get_service_client_using_arm_token(self, client_class, subscription_id,
                                                   subscription_bound=subscription_bound,
                                                   base_url=base_url)


class ArmTokenAuthentication(AbstractAuthentication):
    """
    The class is used internally to acquire ARM access tokens using service principle or managed service identity.
    It's preferable to use :class:`azureml.core.authentication.ServicePrincipalAuthentication` instead.
    """
    def __init__(self, arm_access_token):
        """
        :param arm_access_token: ARM access token
        :type arm_access_token: str
        """
        # TODO: user_email will be removed or made optional.
        self._arm_access_token = arm_access_token

    def get_authentication_header(self):
        """
        Returns the HTTP authorization header. The authorization header contains the user access token
        for access authorizaton against the service.

        :return: Returns the HTTP authorization header.
        :rtype: dict
        """
        auth_header = {"Authorization": "Bearer " + self._arm_access_token}
        return auth_header

    def update_arm_access_token(self, new_arm_access_token):
        """
        Updates arm access token.
        :param new_arm_access_token: ARM access token
        :type new_arm_access_token: str
        """
        self._arm_access_token = new_arm_access_token

    def _get_arm_token(self):
        """
        :return: Returns arm access token
        :rtype: str
        """        
        return self._arm_access_token

    def _get_all_subscription_ids(self):
        """
        Returns a list of subscriptions that are accessible through this authentication.
        :return: Returns a list of SubscriptionInfo named tuples.
        :rtype: list
        """
        from azure.cli.core.adal_authentication import AdalAuthentication
        auth_object = AdalAuthentication(lambda: ("Bearer", self._get_arm_token(), None))
        return _get_subscription_ids_via_client(auth_object)

    def _perform_subscription_check(self, subscription_id):
        """
        Checks if the auth has access to the provided subscription id.
        If auth doesn't have access then azureml.exceptions.AuthenticationException is thrown.
        :param subscription_id:
        :type subscription_id: str        
        :return: None if successful
        :rtype: None
        """
        all_subscription_list = self._get_all_subscription_ids()
        if not _check_if_subscription_exists(subscription_id, all_subscription_list):
            raise AuthenticationException("You don't have access to {} subscription. All the subscriptions "
                                          "that you have access to = {}. "
                                          "Please provide an arm token with which you have access to "
                                          "the subscription.".format(subscription_id, all_subscription_list))

    def _get_service_client(self, client_class, subscription_id, subscription_bound=True, base_url=None):
        """
        Creates and returns a service client object for client_class using subscription_id and auth token.
        :param client_class:
        :type client_class: object
        :param subscription_id:
        :type subscription_id: str
        :param subscription_bound: True if a subscription id is required to construct the client. Only False for
        1 RP clients.
        :type subscription_bound: bool
        :param base_url: The specified base URL client should use, usually differs by region
        :type base_url: str
        :return:
        :rtype: client_class
        """
        # Checks if auth has access to the provided subscription.
        # In Azureml Token based auth, we don't do subscription check, as this requires querying ARM.
        if subscription_id:
            self._perform_subscription_check(subscription_id)

        return _get_service_client_using_arm_token(self, client_class, subscription_id,
                                                   subscription_bound=subscription_bound,
                                                   base_url=base_url)


class ServicePrincipalAuthentication(AbstractAuthentication):
    """
    The class allows for authentication using a service principle instead of users own identity.
    The class is ideal for automation and CI/CD scenarios.
    """

    def __init__(self, tenant_id, username, password):
        """
        The class allows for authentication using a service principle instead of users own identity.
        The class is ideal for automation and CI/CD scenarios.
        :param tenant_id: The active directory tenant that the service identity belongs to.
        :type tenant_id: str
        :param username: The service principal id.
        :type username: str
        :param password: The service principal key.
        :type password: str
        """
        self._tenant_id = tenant_id
        self._username = username
        self._password = password

    def get_authentication_header(self):
        """
        Returns the HTTP authorization header. The authorization header contains the user access token
        for access authorizaton against the service.

        :return: Returns the HTTP authorization header.
        :rtype: dict
        """
        auth_header \
            = {"Authorization": self._get_sp_credential_object().signed_session().headers['Authorization']}
        return auth_header

    def _get_arm_token(self):
        """
        :return: Returns arm token from sp credential object
        :rtype: str
        """        
        header = self._get_sp_credential_object().signed_session().headers['Authorization']
        return header.split(" ")[1]

    def _get_sp_credential_object(self):
        """
        :return: Returns sp credentials
        :rtype: AdalAuthentication
        """        
        import adal
        from msrestazure.azure_active_directory import AdalAuthentication
        from msrestazure.azure_cloud import AZURE_PUBLIC_CLOUD

        # TODO: We have some sad deepcopy in our code, and keeping
        # sp_credentials object as a class field prevents the deepcopy
        # off  auth object in workspace, project classes.
        # Because sp_credentials somehow contains RLock object that cannot be deepcopied.
        login_endpoint = AZURE_PUBLIC_CLOUD.endpoints.active_directory
        resource = AZURE_PUBLIC_CLOUD.endpoints.active_directory_resource_id

        context = adal.AuthenticationContext('{0}/{1}'.format(login_endpoint, self._tenant_id),
                                             api_version=None)
        sp_credentials = AdalAuthentication(
            context.acquire_token_with_client_credentials,
            resource, self._username, self._password)
        return sp_credentials

    def _perform_subscription_check(self, subscription_id):
        """
        Checks if the auth has access to the provided subscription id.
        If auth doesn't have access then azureml.exceptions.AuthenticationException is thrown.
        :param subscription_id:
        :type subscription_id: str        
        :return: None if successful
        :rtype: None
        """
        arm_auth = ArmTokenAuthentication(self._get_arm_token())
        return arm_auth._perform_subscription_check(subscription_id)

    def _get_all_subscription_ids(self):
        """
        Returns a list of subscriptions that are accessible through this authentication.
        :return: Returns a list of SubscriptionInfo named tuples.
        :rtype: list
        """
        arm_auth = ArmTokenAuthentication(self._get_arm_token())
        return arm_auth._get_all_subscription_ids()

    def _get_service_client(self, client_class, subscription_id, subscription_bound=True, base_url=None):
        """
        Creates and returns a service client object for client_class using subscription_id and auth token.
        :param client_class:
        :type client_class: object
        :param subscription_id:
        :type subscription_id: str
        :param subscription_bound: True if a subscription id is required to construct the client. Only False for
        1 RP clients.
        :type subscription_bound: bool
        :param base_url: The specified base URL client should use, usually differs by region
        :type base_url: str
        :return:
        :rtype: client_class
        """
        arm_auth = ArmTokenAuthentication(self._get_arm_token())
        return arm_auth._get_service_client(client_class, subscription_id,
                                            subscription_bound=subscription_bound, base_url=base_url)


class AzureMlTokenAuthentication(AbstractAuthentication):
    """
    Authorizes users by their Azure ML token. The Azure ML token is generated when a run is submitted and is only available to the code submitted.
    The class can only be used in the context of submitted run. The token cannot be used against any ARM operations like provisioning compute.
    The Azure ML token is useful when executing a program remotely where it might be unsafe to use the user's private credentials.
    """
    def __init__(self, azureml_access_token, user_email=None):
        """
        Authorizes users by their Azure ML token. The Azure ML token is generated when a run is submitted and is only available to the code submitted.
        The class can only be used in the context of submitted run. The token cannot be used against any ARM operations like provisioning compute.
        The Azure ML token is useful when executing a program remotely where it might be unsafe to use the user's private credentials.

        :param azureml_access_token: The Azure ML token is generated when a run is submitted and is only available to the code submitted.
        :type azureml_access_token: str
        :param user_email:
        :type user_email: str
        """
        self._azureml_access_token = azureml_access_token
        self._user_email = user_email

    def get_authentication_header(self):
        """
        Returns the HTTP authorization header. The authorization header contains the user access token
        for access authorizaton against the service.

        :return: Returns the HTTP authorization header.
        :rtype: dict
        """
        auth_header = {"Authorization": "Bearer " + self._azureml_access_token}
        return auth_header

    def update_azureml_access_token(self, new_arm_access_token):
        """
        Updates azureml access token.
        :param new_arm_access_token:
        :type new_arm_access_token: str        
        """
        raise AuthenticationException("AzureMlTokenAuthentication.update_azureml_access_token "
                                      "not yet supported.")

    def _get_arm_token(self):
        raise AuthenticationException("AzureMlTokenAuthentication._get_arm_token "
                                      "not yet supported.")


class MsiAuthentication(AbstractAuthentication):
    """
    Authorizes users using MSIAuthentication in msrestazure.azure_active_directory.
    """
    def get_authentication_header(self):
        """
        Returns the HTTP authorization header. The authorization header contains the user access token
        for access authorizaton against the service.
        :return: Returns the HTTP authorization header.
        :rtype: dict
        """
        auth_header = {"Authorization": "Bearer " + self._get_aad_token()}
        return auth_header

    def _get_aad_token(self):
        """
        :return: Returns the access token.
        :rtype: str
        """
        # retrieves the AAD token through MSI
        from msrestazure.azure_active_directory import MSIAuthentication
        msi_auth = MSIAuthentication()
        msi_auth.set_token()
        return msi_auth.token['access_token']

    def _get_arm_token(self):
        """
        :return: Returns the arm token.
        :rtype: str
        """
        return self._get_aad_token()

    def _get_all_subscription_ids(self):
        """
        Returns a list of subscriptions that are accessible through this authentication.
        :return: Returns a list of SubscriptionInfo named tuples.
        :rtype: list
        """
        from msrestazure.azure_active_directory import MSIAuthentication
        msi_auth = MSIAuthentication()
        return _get_subscription_ids_via_client(msi_auth)

    def _perform_subscription_check(self, subscription_id):
        """
        Checks if the auth has access to the provided subscription id.
        If auth doesn't have access then azureml.exceptions.AuthenticationException is thrown.
        :param subscription_id:
        :type subscription_id: str
        :return: None if successful
        :rtype: None
        """
        all_subscription_list = self._get_all_subscription_ids()
        if not _check_if_subscription_exists(subscription_id, all_subscription_list):
            raise AuthenticationException("You don't have access to {} subscription. All the subscriptions "
                                          "that you have access to = {}. "
                                          "Please provide an arm token with which you have access to "
                                          "the subscription.".format(subscription_id, all_subscription_list))

    def _get_service_client(self, client_class, subscription_id, subscription_bound=True, base_url=None):
        """
        Creates and returns a service client object for client_class using subscription_id and auth token.
        :param client_class:
        :type client_class: object
        :param subscription_id:
        :type subscription_id: str
        :param subscription_bound: True if a subscription id is required to construct the client. Only False for
        1 RP clients.
        :type subscription_bound: bool
        :param base_url: The specified base URL client should use, usually differs by region
        :type base_url: str
        :return:
        :rtype: client_class
        """
        arm_auth = ArmTokenAuthentication(self._get_arm_token())
        return arm_auth._get_service_client(client_class, subscription_id,
                                            subscription_bound=subscription_bound, base_url=base_url)


class AzureNotebooksAuthentication(AbstractAuthentication):
    """
    Only used when the program is running in Azure Notebooks.
    It uses the "Connect to Azure" feature in Azure Notebooks to authenticate users.
    """

    def get_authentication_header(self):
        """
        Returns the HTTP authorization header. The authorization header contains the user access token
        for access authorizaton against the service.

        :return: Returns the HTTP authorization header.
        :rtype: dict
        """
        module_logger.warning("azureml.core.authentication.AzureNotebooksAuthentication class will be deprecated. "
                              "Please use azureml.core.authentication.MsiAuthentication instead.")
        auth_header = {"Authorization": "Bearer " + self._get_aad_token()}
        return auth_header

    def _get_aad_token(self):
        """
        :return: Returns MSI auth token.
        :rtype: MSIAuthentication
        """        
        # retrieves the AAD token through MSI
        from msrestazure.azure_active_directory import MSIAuthentication
        msi_auth = MSIAuthentication()
        msi_auth.set_token()
        return msi_auth.token['access_token']

    def _get_arm_token(self):
        """
        :return: Returns access token
        :rtype: str
        """        
        return self._get_aad_token()

    def _get_all_subscription_ids(self):
        """
        Returns a list of subscriptions that are accessible through this authentication.
        :return: Returns a list of SubscriptionInfo named tuples.
        :rtype: list
        """
        from msrestazure.azure_active_directory import MSIAuthentication
        msi_auth = MSIAuthentication()
        return _get_subscription_ids_via_client(msi_auth)

    def _perform_subscription_check(self, subscription_id):
        """
        Checks if the auth has access to the provided subscription id.
        If auth doesn't have access then azureml.exceptions.AuthenticationException is thrown.
        :param subscription_id:
        :type subscription_id: str        
        :return: None if successful
        :rtype: None
        """
        all_subscription_list = self._get_all_subscription_ids()
        if not _check_if_subscription_exists(subscription_id, all_subscription_list):
            raise AuthenticationException("You don't have access to {} subscription. All the subscriptions "
                                          "that you have access to = {}. "
                                          "Please provide an arm token with which you have access to "
                                          "the subscription.".format(subscription_id, all_subscription_list))

    def _get_service_client(self, client_class, subscription_id, subscription_bound=True, base_url=None):
        """
        Creates and returns a service client object for client_class using subscription_id and auth token.
        :param client_class:
        :type client_class: object
        :param subscription_id:
        :type subscription_id: str
        :param subscription_bound: True if a subscription id is required to construct the client. Only False for
        1 RP clients.
        :type subscription_bound: bool
        :param base_url: The specified base URL client should use, usually differs by region
        :type base_url: str
        :return:
        :rtype: client_class
        """
        arm_auth = ArmTokenAuthentication(self._get_arm_token())
        return arm_auth._get_service_client(client_class, subscription_id,
                                            subscription_bound=subscription_bound, base_url=base_url)


def _get_subscription_ids_via_client(auth_obj):
    """
    A helper function to retrieve subscriptionIDs and names using the SubscriptionClient.
    Returns a list of subscriptions that are accessible through this authentication.
    :param auth_obj: The msrest auth object. This is not azureml.core.authentication object.
    :type auth_obj: azure.cli.core.adal_authentication.AdalAuthentication
    :return: Returns a list of SubscriptionInfo named tuples.
    :rtype: list
    """
    from azure.mgmt.resource import SubscriptionClient
    result = []
    subscription_client = SubscriptionClient(auth_obj)
    for subscription in subscription_client.subscriptions.list():
        subscription_info = SubscriptionInfo(subscription.display_name,
                                             subscription.subscription_id)
        result.append(subscription_info)
    return result


def _check_if_subscription_exists(subscription_id, subscription_id_list):
    """
    Checks if subscription_id exists in subscription_id_list.
    :param subscription_id: Subscription id to check.
    :type subscription_id: str
    :param subscription_id_list: Subscription id list.
    :type subscription_id_list: list[azureml.core.authentication.SubscriptionInfo]
    :return: True if subscription exists.
    :rtype: bool
    """
    for subscription_info in subscription_id_list:
        if subscription_info.subscription_id.strip() == subscription_id.strip():
            return True
    return False


def _get_service_client_using_arm_token(auth, client_class, subscription_id,
                                        subscription_bound=True, base_url=None):
    """
    :param auth:
    :type auth: AbstractAuthentication
    :param client_class: The service client class
    :type client_class: object    
    :param subscription_id:
    :type subscription_id: str
    :param subscription_bound: True if a subscription id is required to construct the client. Only False for
    1 RP clients.
    :type subscription_bound: bool
    :param base_url:
    :type base_url: str
    :return:
    :rtype: object
    """
    from azure.cli.core.adal_authentication import AdalAuthentication
    # TODO: Might replace it with the parsed values from the header.
    token = auth.get_authentication_header()["Authorization"].split(" ")[1]
    auth_object = AdalAuthentication(lambda: ("Bearer", token, None))

    # 1 RP clients are not subscription bound.
    if not subscription_bound:
        client = client_class(auth_object, base_url=base_url)
    else:
        # converting subscription_id, which is string, to string because of weird python 2.7 errors.
        client = client_class(auth_object, str(subscription_id))
    return client
