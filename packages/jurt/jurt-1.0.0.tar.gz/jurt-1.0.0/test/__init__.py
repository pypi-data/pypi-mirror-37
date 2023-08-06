"""Unit test module for jurt"""
# jurt: Jeff's Unified Registration Tool
#
# Copyright (c) 2018, Jeffrey M. Engelmann
#
# jurt is released under the revised (3-clause) BSD license.
# For details, see LICENSE.txt
#

import os
import unittest

def get_suite():
    """Return a unittest.TestSuite object for jurt"""
    loader = unittest.TestLoader()
    suite = loader.discover(os.path.abspath(os.path.dirname(__file__)))
    return suite

