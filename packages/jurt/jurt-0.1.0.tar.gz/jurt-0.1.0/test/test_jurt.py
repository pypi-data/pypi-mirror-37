"""Unit tests for jurt"""
# jurt: Jeff's Unified Registration Tool
#
# Copyright (c) 2018, Jeffrey M. Engelmann
#
# jurt is released under the revised (3-clause) BSD license.
# For details, see LICENSE.txt
#

import unittest
import sys
import os
import tempfile
import logging
import jurt

###############################################################################

class TestPrefix(unittest.TestCase):
    """Test the jurt.Prefix class"""

    def test_prefix_noarg(self):
        with self.assertRaisesRegex(TypeError,
            "__new__\(\) missing 1 required positional argument: 'prefix'"):
            obj = jurt.Prefix()

    def test_prefix_none(self):
        with self.assertRaisesRegex(TypeError, 'prefix must be a string'):
            obj = jurt.Prefix(None)

    def test_prefix_empty(self):
        with self.assertRaisesRegex(ValueError, 'prefix cannot be empty'):
            obj = jurt.Prefix('')

    def test_prefix_bad_dir(self):
        td = tempfile.TemporaryDirectory()
        td_name = td.name
        td.cleanup()
        self.assertFalse(os.path.isdir(td_name))
        with self.assertRaisesRegex(IOError,
            f'Could not find directory: {td_name}'):
            obj = jurt.Prefix(os.path.join(td_name, 'TEST'))

    def test_prefix_good_without_path(self):
        test_prefix = 'TEST'
        obj = jurt.Prefix(test_prefix)
        self.assertEqual(obj, os.path.join(os.getcwd(), test_prefix))

    def test_prefix_good_with_path(self):
        with tempfile.TemporaryDirectory() as td:
            test_prefix = os.path.join(td, 'TEST')
            obj = jurt.Prefix(test_prefix)
            self.assertEqual(obj, test_prefix)

    def test_prefix_reassign(self):
        test_prefix = 'TEST01'
        obj = jurt.Prefix(test_prefix)
        self.assertEqual(obj, os.path.join(os.getcwd(), test_prefix))
        with self.assertRaisesRegex(TypeError, 'prefix must be a string'):
            obj = jurt.Prefix(None)
        self.assertEqual(obj, os.path.join(os.getcwd(), test_prefix))
        with self.assertRaisesRegex(ValueError, 'prefix cannot be empty'):
            obj = jurt.Prefix('')
        self.assertEqual(obj, os.path.join(os.getcwd(), test_prefix))
        test_prefix = 'TEST02'
        obj = jurt.Prefix(test_prefix)
        self.assertEqual(obj, os.path.join(os.getcwd(), test_prefix))

###############################################################################

class TestDataset(unittest.TestCase):
    """Test the jurt.Dataset class"""

    def test_dataset_noarg(self):
        with self.assertRaisesRegex(TypeError,
            "__new__\(\) missing 1 required positional argument: 'dataset'"):
            obj = jurt.Dataset()

    def test_dataset_none(self):
        with self.assertRaisesRegex(TypeError, 'dataset name must be a string'):
            obj = jurt.Dataset(None)

    def test_dataset_empty(self):
        with self.assertRaisesRegex(ValueError, 'dataset name cannot be empty'):
            obj = jurt.Dataset('')

    def test_dataset_bad(self):
        with tempfile.TemporaryDirectory() as td:
            tf = os.path.join(td, 'test.nii')
            with self.assertRaisesRegex(IOError, f'Could not find dataset: {tf}'):
                obj = jurt.Dataset(tf)

    def test_dataset_good(self):
        with tempfile.NamedTemporaryFile() as tf:
            obj = jurt.Dataset(tf.name)
            self.assertEqual(obj, tf.name)

    def test_dataset_reassign(self):
        with tempfile.NamedTemporaryFile() as tf1:
            obj = jurt.Dataset(tf1.name)
            self.assertEqual(obj, tf1.name)
            with self.assertRaisesRegex(TypeError, 'dataset name must be a string'):
                obj = jurt.Dataset(None)
            self.assertEqual(obj, tf1.name)
            with self.assertRaisesRegex(ValueError, 'dataset name cannot be empty'):
                obj = jurt.Dataset('')
            self.assertEqual(obj, tf1.name)
            with tempfile.NamedTemporaryFile() as tf2:
                obj = jurt.Dataset(tf2.name)
                self.assertEqual(obj, tf2.name)

###############################################################################

class TestPipeline(unittest.TestCase):
    """Test the jurt.Pipeline class"""

    def setUp(self):
        # Use a NullHandler for logging for this round of tests to prevent
        # extra console output when expected exceptions are raised
        logging.getLogger('jurt').addHandler(logging.NullHandler())

        # Set up the jurt.Pipeline() object
        self.obj = jurt.Pipeline()
        self.assertIsNotNone(self.obj)
        self.assertIsNone(self.obj.prefix)
        self.assertFalse(self.obj.overwrite)
        self.assertIsNone(self.obj.scratch)
        self.assertEqual(self.obj.threads, jurt.Pipeline._default_threads)
        self.assertEqual(self.obj.umask, jurt.Pipeline._default_umask)

    def test_overwrite_none(self):
        with self.assertRaisesRegex(TypeError, 'overwrite must be boolean'):
            self.obj.overwrite = None

    def test_overwrite_false(self):
        self.obj.overwrite = False
        self.assertFalse(self.obj.overwrite)

    def test_overwrite_true(self):
        self.obj.overwrite = True
        self.assertTrue(self.obj.overwrite)

    def test_scratch_none(self):
            self.obj.scratch = None
            self.assertIsNone(self.obj.scratch)

    def test_scratch_bad_type(self):
        with self.assertRaisesRegex(TypeError,'scratch must be a string or None'):
            self.obj.scratch = 0

    def test_scratch_empty(self):
        with self.assertRaisesRegex(ValueError,'scratch cannot be empty'):
            self.obj.scratch = ''

    def test_scratch_bad_dir(self):
        with tempfile.TemporaryDirectory() as td:
            d = os.path.join(td, 'TEST')
            with self.assertRaisesRegex(IOError, f'Could not find directory: {d}'):
                self.obj.scratch = d

    def test_scratch_good_dir(self):
        with tempfile.TemporaryDirectory() as td:
            self.obj.scratch = td
            self.assertEqual(self.obj.scratch, td)

    def test_threads_none(self):
        with self.assertRaisesRegex(TypeError, 'threads must be an integer'):
            self.obj.threads = None

    def test_threads_string(self):
        with self.assertRaisesRegex(TypeError, 'threads must be an integer'):
            self.obj.threads = '8'

    def test_threads_negative(self):
        with self.assertRaisesRegex(ValueError, 'threads must be greater than zero'):
            self.obj.threads = -8

    def test_threads_zero(self):
        with self.assertRaisesRegex(ValueError, 'threads must be greater than zero'):
            self.obj.threads = 0

    def test_threads_positive(self):
        self.obj.threads = 8
        self.assertEqual(self.obj.threads, 8)

    def test_umask_none(self):
        with self.assertRaisesRegex(TypeError, 'umask must be an integer'):
            self.obj.umask = None

    def test_umask_string(self):
        with self.assertRaisesRegex(TypeError, 'umask must be an integer'):
            self.obj.umask = '007'

    def test_umask_invalid(self):
        with self.assertRaisesRegex(ValueError,
            'umask must be in the range \[%#05o,%#05o\]' % (0, 0o777)):
            self.obj.umask = 0o7771

    def test_umask_valid(self):
        umask = 0o007
        self.obj.umask = umask
        self.assertEqual(self.obj.umask, umask)

    def test_run_no_prefix(self):
        with self.assertRaisesRegex(RuntimeError,
            f'prefix must be set prior to {type(self.obj).__name__}.run\(\)'):
            self.obj.run()

    def test_run(self):
        self.obj.prefix = 'TEST'
        with self.assertRaisesRegex(NotImplementedError,
            f'{type(self.obj).__name__}.pipeline\(\) must be overridden'):
            self.obj.run()

    def test_cmd_redirect(self):
        teststr = 'Hello, world!'
        with tempfile.TemporaryDirectory() as td:
            fn = os.path.join(td, 'test.log')
            with open(fn, 'w', buffering=1) as f:
                self.obj._cmd('echo', teststr, redirect=f)
            with open(fn, 'r') as f:
                self.assertEqual(f.readline().strip(), teststr)

###############################################################################

class TestFsPipeline(unittest.TestCase):
    """Test the jurt.FsPipeline class"""

    def setUp(self):
        self.obj = jurt.FsPipeline()
        self.assertIsNotNone(self.obj)

    def test_run(self):
        logging.getLogger('jurt').addHandler(logging.NullHandler())
        self.obj.prefix = 'TEST'
        with self.assertRaisesRegex(NotImplementedError,
            f'{type(self.obj).__name__}.pipeline\(\) must be overridden'):
            self.obj.run()

###############################################################################

class TestPrepT1(unittest.TestCase):
    """Test the jurt.PrepT1 class"""

    def setUp(self):
        self.obj = jurt.PrepT1()
        self.assertIsNotNone(self.obj)
        self.assertIsNone(self.obj.raw)

    def test_run_no_raw(self):
        self.obj.prefix = 'TEST'
        with self.assertRaisesRegex(RuntimeError,
            f'raw must be set prior to {type(self.obj).__name__}.run\(\)'):
            self.obj.run()

###############################################################################

class TestHwaT1(unittest.TestCase):
    """Test the jurt.HwaT1 class"""

    def setUp(self):
        self.obj = jurt.HwaT1()
        self.assertIsNotNone(self.obj)
        self.assertEqual(self.obj.preflood, jurt.HwaT1._preflood_default)

    def test_preflood_none(self):
        with self.assertRaisesRegex(TypeError,
            'preflood must be an integer'):
            self.obj.preflood = None

    def test_preflood_bool(self):
        with self.assertRaisesRegex(TypeError,
            'preflood must be an integer'):
            self.obj.preflood = True

    def test_preflood_string(self):
        with self.assertRaisesRegex(TypeError,
            'preflood must be an integer'):
            self.obj.preflood = '25'

    def test_preflood_too_low(self):
        with self.assertRaisesRegex(ValueError,
            'preflood must be in the range \[0,100\]'):
            self.obj.preflood = -1

    def test_preflood_too_high(self):
        with self.assertRaisesRegex(ValueError,
            'preflood must be in the range \[0,100\]'):
            self.obj.preflood = 101

    def test_preflood_good(self):
        self.obj.preflood = 35
        self.assertEqual(self.obj.preflood, 35)

###############################################################################

class TestGcutT1(unittest.TestCase):
    """Test the jurt.GcutT1 class"""

    def setUp(self):
        self.obj = jurt.GcutT1()
        self.assertIsNotNone(self.obj)
        self.assertEqual(self.obj.thresh, jurt.GcutT1._thresh_default)

    def test_thresh_none(self):
        with self.assertRaisesRegex(TypeError,
            'thresh must be numeric'):
            self.obj.thresh = None

    def test_thresh_bool(self):
        with self.assertRaisesRegex(TypeError,
            'thresh must be numeric'):
            self.obj.thresh = True

    def test_thresh_string(self):
        with self.assertRaisesRegex(TypeError,
            'thresh must be numeric'):
            self.obj.thresh = '.4'

    def test_thresh_too_low(self):
        with self.assertRaisesRegex(ValueError,
            'thresh must be in the range \(0\.0,1\.0\)'):
            self.obj.thresh = 0.0

    def test_thresh_too_high(self):
        with self.assertRaisesRegex(ValueError,
            'thresh must be in the range \(0\.0,1\.0\)'):
            self.obj.thresh = 1.0

    def test_thresh_good(self):
        self.obj.thresh = 0.36
        self.assertEqual(self.obj.thresh, 0.36)

###############################################################################

if __name__ == '__main__':
    unittest.main()

###############################################################################

