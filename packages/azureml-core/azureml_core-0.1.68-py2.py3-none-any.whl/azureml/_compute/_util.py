# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

import json
import requests
from pkg_resources import resource_string
from azureml.exceptions import ComputeTargetException

WORKSPACE_API_VERSION = '2018-03-01-preview'
batchai_payload_template = json.loads(resource_string(__name__, 'data/batchai_cluster_template.json').decode('ascii'))
aks_payload_template = json.loads(resource_string(__name__, 'data/aks_cluster_template.json').decode('ascii'))
dsvm_payload_template = json.loads(resource_string(__name__, 'data/dsvm_cluster_template.json').decode('ascii'))
hdinsight_payload_template = json.loads(resource_string(__name__, 'data/hdinsight_cluster_template.json')
                                        .decode('ascii'))
datafactory_payload_template = json.loads(resource_string(__name__, 'data/datafactory_payload_template.json')
                                          .decode('ascii'))
databricks_compute_template = json.loads(resource_string(__name__, 'data/databricks_compute_template.json')
                                         .decode('ascii'))
adla_payload_template = json.loads(resource_string(__name__, 'data/adla_payload_template.json').decode('ascii'))
remote_payload_template = json.loads(resource_string(__name__, 'data/remote_compute_template.json').decode('ascii'))


def get_paginated_compute_results(payload, headers):
    if 'value' not in payload:
        raise ComputeTargetException('Error, invalid paginated response payload, missing "value":\n'
                                     '{}'.format(payload))
    items = payload['value']
    while 'nextLink' in payload:
        next_link = payload['nextLink']

        try:
            resp = requests.get(next_link, headers=headers)
        except requests.Timeout:
            print('Error, request to Machine Learning Compute timed out. Returning with items found so far')
            return items
        if resp.status_code == 200:
            content = resp.content
            if isinstance(content, bytes):
                content = content.decode('utf-8')
            payload = json.loads(content)
        else:
            raise ComputeTargetException('Received bad response from Machine Learning Compute while retrieving '
                                         'paginated results:\n'
                                         'Response Code: {}\n'
                                         'Headers: {}\n'
                                         'Content: {}'.format(resp.status_code, resp.headers, resp.content))
        if 'value' not in payload:
            raise ComputeTargetException('Error, invalid paginated response payload, missing "value":\n'
                                         '{}'.format(payload))
        items += payload['value']

    return items
