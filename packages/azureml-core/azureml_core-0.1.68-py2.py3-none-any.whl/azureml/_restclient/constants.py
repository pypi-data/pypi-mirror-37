# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Restclient constants"""
# origin for run related artifacts
RUN_ORIGIN = "ExperimentRun"
RUN_ID_EXPRESSION = 'RunId eq '
NAME_EXPRESSION = 'name eq '
ORDER_BY_STARTTIME_EXPRESSION = 'StartTimeUtc desc'
ORDER_BY_RUNID_EXPRESSION = 'RunId desc'
ATTRIBUTE_CONTINUATION_TOKEN_NAME = 'continuation_token'
ATTRIBUTE_VALUE_NAME = 'value'
ACCESS_TOKEN_NAME = 'access_token'
CONTINUATION_TOKEN = 'continuationtoken'

BASE_RUN_SOURCE = "azureml.runsource"

SDK_TARGET = "sdk"
