# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

import json
import sys
import os
import logging
from os.path import expanduser, join, dirname

from azureml._base_sdk_common.app_settings import AppSettings
from .workspace.version import VERSION

GALLERY_GLOBAL_ENDPOINT = 'https://gallery.cortanaintelligence.com/project'
CATALOG_GLOBAL_ENDPOINT = 'https://catalog.cortanaanalytics.com'
TRANSIENT_CLUSTER_ENDPOINT = 'AZUREML_EXPERIMENTATION_HOST'
HISTORY_SERVICE_ENDPOINT_KEY = "AZUREML_SERVICE_ENDPOINT"


if sys.version_info[0] < 3:
    from urlparse import urljoin
else:
    from urllib.parse import urljoin

module_logger = logging.getLogger(__name__)


def get_history_service_url(auth, account_scope):
    """
    Returns the history service url.
    :param auth: auth object.
    :type auth: azureml.core.authentication.AbstractAuthentication
    :param account_scope: full account scope.
    :type account_scope: str
    :return: History service URL.
    :rtype: str
    """
    #  Check environment variables for history_service_url overrides
    for key in [TRANSIENT_CLUSTER_ENDPOINT, HISTORY_SERVICE_ENDPOINT_KEY]:
        history_service_url = os.environ.get(key)
        if history_service_url:
            module_logger.debug("Found history service url in environment variable {}, "
                                "history service url: {}".format(key, history_service_url))
            return history_service_url

    return CachedServiceDiscovery(auth).get_service_url(account_scope, 'history', AppSettings().get_flight())


def get_gallery_service_url(account_scope, flight=None):
    # Gallery is a global service with only one endpoint. Simply return it
    return GALLERY_GLOBAL_ENDPOINT


def get_catalog_service_url(account_scope, flight=None):
    # Catalog is a global service with only one endpoint. Simply return it
    return CATALOG_GLOBAL_ENDPOINT

def get_pipelines_url(auth, account_scope):
    """
    Returns the service url for experiment graphs (Aeva).
    :param auth: auth object.
    :type auth: azureml.core.authentication.AbstractAuthentication
    :param account_scope: full account scope.
    :type account_scope: str
    :return: Experiment graph service URL.
    :rtype: str
    """
    return CachedServiceDiscovery(auth).get_service_url(account_scope, 'pipelines', AppSettings().get_flight())

class ServiceDiscovery(object):
    def __init__(self, auth):
        """

        :param auth: auth object.
        :type auth: azureml.core.authentication.AbstractAuthentication
        """
        self._auth_object = auth
        pass

    def get_service_url(self, account_scope, service_name, flight):
        return self.get_flight(account_scope, service_name, flight)[service_name]

    def get_flight(self, account_scope, service_name, flight):
        discovery_url = self.get_discovery_url(account_scope)
        params = {}
        if flight is not None and flight != "default":
            params = {'flight': flight}

        import requests
        status = requests.get(discovery_url, params=params)
        status.raise_for_status()
        return status.json()

    def discover_services_uris(self, discovery_url):
        import requests
        status = requests.get(discovery_url)
        status.raise_for_status()
        return status.json()

    def get_discovery_url(self, account_scope):
        resource = self._get_team_resource(account_scope)
        discovery_uri = resource['properties']['discoveryUrl']
        if discovery_uri is None:
            raise ValueError("cannot acquire discovery uri for resource {}".format(account_scope))
        return discovery_uri

    def _get_team_resource(self, account_scope):
        from azure.cli.core.cloud import get_active_cloud
        import requests
        arm_endpoint = get_active_cloud().endpoints.resource_manager
        headers = self._auth_object.get_authentication_header()
        query_parameters = {'api-version': VERSION}
        status = requests.get(urljoin(arm_endpoint, account_scope), headers=headers, params=query_parameters)

        status.raise_for_status()
        return status.json()


class CachedServiceDiscovery(ServiceDiscovery):
    def __init__(self, auth, file_path=join(expanduser("~"), ".azureml", ".discovery")):
        super(CachedServiceDiscovery, self).__init__(auth)
        dir_name = dirname(file_path)
        try:
            os.mkdir(os.path.abspath(dir_name))
        except OSError:
            # Ignoring error if the path already exists.
            pass
        self.file_path = file_path

    def get_flight(self, account_scope, service_name, flight):
        cache = {}
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as file:
                cache = json.load(file)
        try:
            if cache is not None and account_scope in cache:
                account_cache = cache.get(account_scope)
                if flight in account_cache:
                    flight_cache = account_cache.get(flight)
                    if service_name in flight_cache:
                        service_url = flight_cache[service_name]
                        if service_url is not None:
                            return flight_cache

        except TypeError as identifier:
            # This is a bad cache
            cache = {}

        if cache is None:
            cache = {}
        if cache.get(account_scope) is None:
            cache[account_scope] = {}

        cache[account_scope][flight] = super(CachedServiceDiscovery, self).get_flight(account_scope, service_name,
                                                                                      flight)
        with open(self.file_path, "w+") as file:
            json.dump(cache, file)
        return cache[account_scope][flight]
