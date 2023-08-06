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
__version__ = '0.1.1.dev0'

# Import classes from submodules into the jurt namespace
from jurt.core import Prefix
from jurt.core import Dataset
from jurt.core import Pipeline
from jurt.core import FsPipeline
from jurt.core import FslPipeline
from jurt.t1 import PrepT1
from jurt.t1 import SST1
from jurt.t1 import SegT1
from jurt.reg import PrepFunc
from jurt.reg import FuncToT1
from jurt.reg import T1ToStd
from jurt.reg import FuncToStd

###############################################################################

if __name__ == '__main__':
    raise RuntimeError('jurt/__init__.py cannot be directly executed')

###############################################################################

