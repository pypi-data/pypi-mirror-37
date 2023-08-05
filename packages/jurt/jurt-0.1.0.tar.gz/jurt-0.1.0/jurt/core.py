"""Core jurt functionality

Support basic processing pipelines.
"""
# jurt: Jeff's Unified Registration Tool
#
# Copyright (c) 2018, Jeffrey M. Engelmann
#
# jurt is released under the revised (3-clause) BSD license.
# For details, see LICENSE.txt
#

import sys
import os
import subprocess
import argparse
import logging

from jurt import __version__

###############################################################################

def _pipeline_main(cls, ns):

    # Run pipeline from class cls using argparse namespace ns

    delattr(ns, 'func')
    d = vars(ns)
    obj = cls()
    for arg in d:
        setattr(obj, arg, d[arg])
    obj.run()

###############################################################################

class Prefix(str):
    """Dataset prefix (including path)"""

    def __new__(cls, prefix):
        if not isinstance(prefix, str):
            raise TypeError('prefix must be a string')
        if len(prefix) == 0:
            raise ValueError('prefix cannot be empty')
        ap = os.path.abspath(prefix)
        wd = os.path.dirname(ap)
        if not os.path.isdir(wd):
            raise IOError(f'Could not find directory: {wd}')
        return str.__new__(cls, ap)

###############################################################################

class Dataset(str):
    """Full dataset name (including path)"""

    def __new__(cls, dataset):
        if not isinstance(dataset, str):
            raise TypeError('dataset name must be a string')
        if len(dataset) == 0:
            raise ValueError('dataset name cannot be empty')
        ap = os.path.abspath(dataset)
        if not os.path.isfile(ap):
            raise IOError(f'Could not find dataset: {ap}')
        return str.__new__(cls, ap)

###############################################################################

class Pipeline(object):
    """Processing pipeline"""

    _default_threads = 1
    _default_umask = 0o077

    @classmethod
    def parser(cls):
        """Return an argument parser for scripts that use Pipeline objects"""
        p = argparse.ArgumentParser(add_help=False, allow_abbrev=False)
        g1 = p.add_argument_group('Required parameters')
        g1.add_argument('-prefix', required=True,
            help=Pipeline.prefix.__doc__)
        g2 = p.add_argument_group('Options')
        g2.add_argument('-overwrite', action='store_true',
            help=Pipeline.overwrite.__doc__)
        g2.add_argument('-scratch', metavar='DIR',
            help=Pipeline.scratch.__doc__)
        g2.add_argument('-threads', metavar='n', type=int,
            default=Pipeline._default_threads,
            help=Pipeline.threads.__doc__)
        g2.add_argument('-umask', metavar='m',
            type=lambda m: int(m,8),
            default=Pipeline._default_umask,
            help=Pipeline.umask.__doc__)
        return p

    def __init__(self):

        # Set defaults
        self._prefix    = None
        self._overwrite = False
        self._scratch   = None
        self._threads   = Pipeline._default_threads
        self._umask     = Pipeline._default_umask

        # jurt logger
        self._log = logging.getLogger(__name__)
        self._log.debug('Python version: %d.%d.%d.%s%d' % sys.version_info)
        self._log.debug(f'jurt version: {__version__}')

    def __str__(self):
        return (
            f'jurt.{type(self).__name__} object at {id(self):#x}\n' +
            '  %-20s : %s\n'  % ('Prefix', self._prefix) +
            '  %-20s : %s\n'  % ('Overwrite', self._overwrite) +
            '  %-20s : %s\n'  % ('Scratch space', self._scratch) +
            '  %-20s : %d\n'  % ('Threads requested', self._threads) +
            '  %-20s : %#05o' % ('Umask', self._umask))

    @property
    def prefix(self):
        """Output prefix (including path)"""
        return self._prefix

    @prefix.setter
    def prefix(self, prefix):
        self._prefix = Prefix(prefix)

    @property
    def overwrite(self):
        """Overwrite existing output"""
        return self._overwrite

    @overwrite.setter
    def overwrite(self, overwrite):
        if not isinstance(overwrite, bool):
            raise TypeError('overwrite must be boolean')
        self._overwrite = overwrite

    @property
    def scratch(self):
        """Scratch directory"""
        return self._scratch

    @scratch.setter
    def scratch(self, scratch):
        if scratch is None:
            self._scratch = None
            return
        if not isinstance(scratch, str):
            raise TypeError('scratch must be a string or None')
        if len(scratch) == 0:
            raise ValueError('scratch cannot be empty')
        ap = os.path.abspath(scratch)
        if not os.path.isdir(ap):
            raise IOError(f'Could not find directory: {ap}')
        self._scratch = ap

    @property
    def threads(self):
        """Number of threads requested"""
        return self._threads

    @threads.setter
    def threads(self, threads):
        if type(threads) is not int:
            raise TypeError('threads must be an integer')
        if threads <= 0:
            raise ValueError('threads must be greater than zero')
        self._threads = threads

    @property
    def umask(self):
        """Permissions mask (umask) requested"""
        return self._umask

    @umask.setter
    def umask(self, umask):
        if type(umask) is not int:
            raise TypeError('umask must be an integer')
        if umask < 0 or umask > 0o777:
            raise ValueError(
                'umask must be in the range [{0:#05o},{1:#05o}]'.format(0, 0o777))
        self._umask = umask

    def _cmd(self, *cmd, env=None, redirect=subprocess.DEVNULL):
        self._log.info(' '.join(cmd))
        sp = subprocess.Popen(cmd, env=env,
            stdout=redirect, stderr=subprocess.STDOUT)
        sp.communicate()
        rc = sp.returncode
        if rc != 0:
            raise RuntimeError(f'{cmd[0]} failed with code {rc}')

    def run(self):
        """Run the processing pipeline"""

        self._log.info(f'{type(self).__name__} begins')
        old_umask = None

        try:

            # All pipelines require a prefix
            if self.prefix is None:
                raise RuntimeError(
                    f'prefix must be set prior to {type(self).__name__}.run()')

            # Set the umask
            old_umask = os.umask(self._umask)

            # Run the pipeline
            self.pipeline()

        except Exception as e:
            self._log.exception(e)
            raise

        finally:
            if old_umask is not None:
                os.umask(old_umask)
            self._log.info(f'{type(self).__name__} ends')

    def pipeline(self):
        """Processing pipeline"""
        raise NotImplementedError(
            f'{type(self).__name__}.pipeline() must be overridden')

###############################################################################

if __name__ == '__main__':
    raise RuntimeError('jurt/core.py cannot be directly executed')

###############################################################################

