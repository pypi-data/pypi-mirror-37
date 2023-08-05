"""Jeff's Unified Registration Tool

Facilitate coregistration and spatial normalization of fMRI datasets.
"""
#
# Copyright (c) 2018, Jeffrey M. Engelmann
#
# jurt is released under the revised (3-clause) BSD license.
# For details, see LICENSE.txt
#

# Set the version string
# This is automatically updated by bumpversion (see .bumpversion.cfg)
__version__ = '0.1.0.dev2'

# Import classes from submodules into the jurt namespace
from jurt.core import Prefix, Dataset, Pipeline
from jurt.t1 import FsPipeline, PrepT1, HwaT1, GcutT1

###############################################################################

if __name__ == '__main__':
    raise RuntimeError('jurt/__init__.py cannot be directly executed')

###############################################################################

