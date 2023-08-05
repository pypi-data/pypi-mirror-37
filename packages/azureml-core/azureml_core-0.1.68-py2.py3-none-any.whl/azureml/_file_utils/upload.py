# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

import re
import logging

module_logger = logging.getLogger(__name__)


def get_domain_parts(sas_url):
    pattern = r".*\/\/([^\/]+)"
    domain = re.match(pattern, sas_url).group(1)
    parts = domain.split(".")
    return parts


def get_block_blob_service_credentials(sas_url):
    uri_parts = sas_url.split("?", 2)
    sas_token = uri_parts[1]
    parts_dot = get_domain_parts(sas_url)
    account_name = parts_dot[0]
    paths_slash = re.split("/+", sas_url)
    container_name = paths_slash[2]
    return sas_token, account_name, container_name


def upload_blob_from_stream(stream, url, blob_name, content_type=None, session=None):
    # TODO add support for upload without azure.storage
    from azure.storage.blob import BlockBlobService
    from azure.storage.blob.models import ContentSettings

    sas_token, account_name, container_name = get_block_blob_service_credentials(url)
    content_settings = ContentSettings(content_type=content_type)
    blob_service = BlockBlobService(account_name=account_name, sas_token=sas_token, request_session=session)
    return blob_service.create_blob_from_stream(container_name, blob_name, stream, content_settings=content_settings)
