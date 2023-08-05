# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""This package is used for managing Azure ML Images"""

from azureml._base_sdk_common import __version__ as VERSION
from .image import Image
from .container import ContainerImage


__version__ = VERSION

__all__ = [
    'Image',
    'ContainerImage',
]
