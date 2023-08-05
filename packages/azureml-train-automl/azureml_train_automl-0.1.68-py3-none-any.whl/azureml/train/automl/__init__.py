# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Init for standard AutoML modules."""
import os
import sys

vendor_folder = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "_vendor"))
sys.path.append(vendor_folder)

from automl.client.core.common.utilities import extract_user_data, get_sdk_dependencies

from .automl import fit_pipeline
from .automlconfig import AutoMLConfig

__all__ = [
    'AutoMLConfig',
    'fit_pipeline',
    'extract_user_data',
    'get_sdk_dependencies']

try:
    from ._version import ver
    __version__ = ver
except ImportError:
    __version__ = '0.0.0+dev'
