"""Unit test entry point for jurt"""
# jurt: Jeff's Unified Registration Tool
#
# Copyright (c) 2018, Jeffrey M. Engelmann
#
# jurt is released under the revised (3-clause) BSD license.
# For details, see LICENSE.txt
#

import sys
import os
import unittest

def main():
    """Discover and run jurt unit tests"""
    loader = unittest.TestLoader()
    suite = loader.discover(os.path.abspath(os.path.dirname(__file__)))
    runner = unittest.TextTestRunner()
    runner.run(suite)

if __name__ == '__main__':
    sys.exit(main())

