# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

MMS_WORKSPACE_API_VERSION = '2018-03-01-preview'
MMS_SYNC_TIMEOUT_SECONDS = 80
SUPPORTED_RUNTIMES = {'spark-py': 'SparkPython', 'python': 'Python', 'python-slim': 'PythonSlim'}
UNDOCUMENTED_RUNTIMES = ['python-slim']
WORKSPACE_RP_API_VERSION = '2018-03-01-preview'
MAX_HEALTH_CHECK_TRIES = 30
HEALTH_CHECK_INTERVAL_SECONDS = 1
DOCKER_IMAGE_TYPE = "Docker"
FPGA_IMAGE_TYPE = "FPGA"
WEBAPI_IMAGE_FLAVOR = "WebApiContainer"
FPGA_IMAGE_FLAVOR = "BrainwavePackage"
IOT_IMAGE_FLAVOR = "IoTContainer"
CLOUD_DEPLOYABLE_IMAGE_FLAVORS = [WEBAPI_IMAGE_FLAVOR]
ARCHITECTURE_AMD64 = "amd64"
ARCHITECTURE_ARM32V7 = "arm32v7"
