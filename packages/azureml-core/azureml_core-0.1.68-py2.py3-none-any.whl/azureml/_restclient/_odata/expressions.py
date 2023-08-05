# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

from .constants import AND_OP


def and_join(expression_string_list):
    separator = " {0} ".format(AND_OP)
    return separator.join(expression_string_list)
