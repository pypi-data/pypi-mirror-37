# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

MLC_WORKSPACE_API_VERSION = '2018-03-01-preview'
MLC_COMPUTE_RESOURCE_ID_FMT = '/subscriptions/{}/resourceGroups/{}/providers/Microsoft.MachineLearningServices/' \
                              'workspaces/{}/computes/{}'
MLC_ENDPOINT_FMT = 'https://management.azure.com{}'.format(MLC_COMPUTE_RESOURCE_ID_FMT)
