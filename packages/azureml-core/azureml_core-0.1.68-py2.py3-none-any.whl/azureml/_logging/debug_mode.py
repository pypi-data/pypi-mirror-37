# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

import logging
import os

LOG_FILE = os.path.abspath("azureml.log")
LOG_FORMAT = '%(asctime)s|%(name)s|%(levelname)s|%(message)s'
INTERESTING_NAMESPACES = [
    "azureml",
    "msrest",
    "urllib2",
    "azure"
]

module_logger = logging.getLogger(__name__)

_debugging_enabled = False


def debug_sdk():
    global _debugging_enabled
    if _debugging_enabled:
        module_logger.warning("Debug logs are already enabled at %s", LOG_FILE)
        return

    formatter = logging.Formatter(LOG_FORMAT)

    file_handler = logging.FileHandler(filename=LOG_FILE, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    module_logger.info("Debug logs are being sent to %s", LOG_FILE)

    for namespace in INTERESTING_NAMESPACES:
        module_logger.debug("Adding [%s] debug logs to this file", namespace)
        n_logger = logging.getLogger(namespace)
        n_logger.setLevel(logging.DEBUG)
        n_logger.addHandler(file_handler)
        # We do the below for strange environments like Revo + Jupyter
        # where root handlers appear to already be set.
        # We don't want to spew to those consoles with DEBUG emissions
        n_logger.propagate = 0

    _debugging_enabled = True
