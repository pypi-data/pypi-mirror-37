# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""This package contains classes used to manage Webservice objects within Azure ML"""

from azureml._base_sdk_common import __version__ as VERSION
from .webservice import Webservice
from .aci import AciWebservice
from .aks import AksWebservice


__version__ = VERSION

__all__ = [
    'Webservice',
    'AciWebservice',
    'AksWebservice'
]
