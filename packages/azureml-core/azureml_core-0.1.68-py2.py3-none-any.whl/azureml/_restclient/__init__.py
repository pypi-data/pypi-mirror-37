# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Initialize _restclient."""

from .rest_client import RestClient
from .run_history_client import RunHistoryClient
from .jasmine_client import JasmineClient
from azureml._base_sdk_common import __version__ as VERSION
__version__ = VERSION

__all__ = ['RestClient', 'RunHistoryClient', 'JasmineClient']
