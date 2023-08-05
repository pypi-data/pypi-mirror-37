"""jurt's T1 module

Facilitate preprocessing and brain-extraction of T1-weighted datasets.
"""
# jurt: Jeff's Unified Registration Tool
#
# Copyright (c) 2018, Jeffrey M. Engelmann
#
# jurt is released under the revised (3-clause) BSD license.
# For details, see LICENSE.txt
#

import os
import re
import shutil
import subprocess
import argparse
import tempfile
import logging

import jurt
import jurt.core

###############################################################################

class FsPipeline(jurt.core.Pipeline):
    """FreeSurfer processing pipeline"""

    @classmethod
    def parser(cls):
        """Return an argument parser for scripts that use FsPipeline objects"""
        p = argparse.ArgumentParser(add_help=False, allow_abbrev=False,
            parents=[cls.__base__.parser()])
        return p

    def __init__(self):
        super().__init__()

        # Check FreeSurfer version
        FS_MIN = (6, 0, 0)
        cmd = subprocess.Popen(['recon-all', '-version'], stdout=subprocess.PIPE)
        o, e = cmd.communicate()
        if cmd.returncode != 0:
            raise RuntimeError('Could not determine FreeSurfer version')
        fs_verstr = o.decode().splitlines()[0]
        pattern = '^freesurfer.+\-v(\d+)\.(\d+)\.(\d+)\-\w+$'
        match = re.search(pattern, fs_verstr)
        if match is None:
            raise RuntimeError('Could not determine FreeSurfer version')
        self._fs_ver = tuple(map(int, match.groups()))
        self._log.debug('FreeSufer version %d.%d.%d' % (self._fs_ver))
        if self._fs_ver < FS_MIN:
            raise RuntimeError(
                    'FreeSurfer %d.%d.%d or newer is required\n' % (FS_MIN) +
                    'Found version %d.%d.%d' % (self._fs_ver))

        # Set default gca
        self._gca = os.path.join(os.environ['FREESURFER_HOME'], 'average',
            'RB_all_withskull_2016-05-10.vc700.gca')
        if not os.path.isfile(self._gca):
            raise IOError(f'Could not find gca template: {self._gca}')

    def __str__(self):
        return super().__str__() + '\n' + (
            '  %-20s : ' % 'FreeSurfer version' + '%d.%d.%d' % self._fs_ver)

###############################################################################

class PrepT1(FsPipeline):
    """Preprocess T1-weighted datasets using FreeSurfer.

    Preprocessing is run via FreeSurfer's recon-all and consists of conforming
    the data to FreeSurfer orientation, non-uniformity correction, and
    intensity normalization.
    """

    @classmethod
    def parser(cls):
        """Return an argument parser for scripts that use PrepT1 objects"""
        p = argparse.ArgumentParser(add_help=False, allow_abbrev=False,
            parents=[cls.__base__.parser()])
        g1 = p.add_argument_group('Required parameters')
        g1.add_argument('-raw', required=True, metavar='DSET',
            help=PrepT1.raw.__doc__)
        g2 = p.add_argument_group('Options')
        g2.add_argument('-help', action='help',
            help='Show this help message and exit')
        return p

    @classmethod
    def main(cls, ns):
        """Run the PrepT1 pipeline using an argparse namespace"""
        jurt.core._pipeline_main(cls, ns)

    def __init__(self):
        super().__init__()

        # Set defaults
        self._raw    = None     # Raw T1-weighted dataset

    def __str__(self):
        return super().__str__() + '\n  %-20s : %s' % ('Raw dataset', self._raw)

    @property
    def prefix(self):
        """Output dataset prefix (including path)"""
        return self._prefix

    @prefix.setter
    def prefix(self, prefix):
        self._prefix = jurt.core.Prefix(prefix)

    @property
    def raw(self):
        """Raw T1-weighted dataset"""
        return self._raw

    @raw.setter
    def raw(self, raw):
        self._raw = jurt.core.Dataset(raw)

    def pipeline(self):


        if self.raw is None:
            raise RuntimeError(
                f'raw must be set prior to {type(self).__name__}.run()')

        # Create a temporary directory for SUBJECTS_DIR
        wd = os.getcwd()
        try:
            with tempfile.TemporaryDirectory(dir=self._scratch) as sd:
                os.chdir(sd)
                self._log.debug(f'Temporary SUBJECTS_DIR: {sd}')

                # Get the subject ID from the prefix
                sid = os.path.basename(self._prefix)
                self._log.info(f'Subject ID: {sid}')

                # Map of FreeSurfer output to PrepT1 output
                orig = f'{sd}/{sid}/mri/orig.mgz'
                nu   = f'{sd}/{sid}/mri/nu.mgz'
                t1   = f'{sd}/{sid}/mri/T1.mgz'
                xfm  = f'{sd}/{sid}/mri/transforms/talairach.xfm'
                lta  = f'{sd}/{sid}/mri/transforms/talairach-with-skull.lta'
                log  = f'{sd}/{sid}/scripts/recon-all.log'

                outfiles = {
                    orig: f'{self._prefix}-anat.mgz',
                    nu:   f'{self._prefix}-anat-nu.mgz',
                    t1:   f'{self._prefix}-anat-inorm.mgz',
                    xfm:  f'{self._prefix}-anat-talairach.xfm',
                    lta:  f'{self._prefix}-anat-talairach-with-skull.lta',
                    log:  f'{self._prefix}-PrepT1.log'}


                # Check if output already exists (delete if overwriting)
                for k, v in outfiles.items():
                    self._log.debug(f'{k} --> {v}')
                    if os.path.isfile(v):
                        if self._overwrite:
                            os.remove(v)
                        else:
                            raise IOError(f'{v} already exists')

                # Run recon-all through intensity normalization
                self._cmd('recon-all',
                    '-motioncor',
                    '-nuintensitycor',
                    '-talairach',
                    '-normalization',
                    '-umask', '{0:03o}'.format(self._umask),
                    '-openmp', str(self._threads),
                    '-sd', sd,
                    '-s', sid,
                    '-i', self._raw)

                # Run mri_em_register, appending to the log file
                env = os.environ
                env['OMP_NUM_THREADS'] = str(self._threads)
                with open(log, 'a', buffering=1) as lf:
                    self._cmd('mri_em_register',
                        '-skull',
                        nu,
                        self._gca,
                        lta,
                        env=env,
                        redirect=lf)

                try:
                    # Copy output to destination
                    for k, v in outfiles.items():
                        shutil.copy2(k, v)

                    # Re-link XFM to MGZ
                    for f in (orig, nu, t1):
                        self._cmd('mri_add_xform_to_header',
                            '-c', outfiles[xfm], outfiles[f])

                except:
                    for k, v in outfiles.items():
                        if os.path.isfile(v):
                            os.remove(v)
                    raise
        except:
            raise
        finally:
            os.chdir(wd)

###############################################################################

class HwaT1(FsPipeline):
    """Remove non-brain tissue using FreeSurfer's hybrid watershed algorithm."""

    _preflood_default = 25

    @classmethod
    def parser(cls):
        """Return an argument parser for scripts taht use HwaT1 objects"""
        p = argparse.ArgumentParser(add_help=False, allow_abbrev=False,
            parents=[cls.__base__.parser()])
        g1 = p.add_argument_group('Options')
        g1.add_argument('-preflood', metavar='h',
            type=int, default=HwaT1._preflood_default,
            help=HwaT1.preflood.__doc__)
        g1.add_argument('-help', action='help',
            help='Show this help message and exit')
        return p

    @classmethod
    def main(cls, ns):
        """Run the HwaT1 pipeline using an argparse namespace"""
        jurt.core._pipeline_main(cls, ns)

    def __init__(self):
        super().__init__()

        # Preflood height (-h) for mri_watershed
        self._preflood = HwaT1._preflood_default

    def __str__(self):
        return super().__str__() + '\n  %-20s : %s' % ('preflood', self._preflood)

    @property
    def preflood(self):
        """Preflooding height for the hybrid watershed algorithm"""
        return self._preflood

    @preflood.setter
    def preflood(self, preflood):
        # Default is 25
        # Range: 0-100
        # Lower values shrink the skull surface
        # Higher values expand the skull surfice

        if type(preflood) is not int:
            raise TypeError('preflood must be an integer')
        if preflood < 0 or preflood > 100:
            raise ValueError('preflood must be in the range [0,100]')
        self._preflood = preflood

    def pipeline(self):

        # Check input files
        anat  = jurt.core.Dataset(self._prefix + '-anat.mgz')
        nu    = jurt.core.Dataset(self._prefix + '-anat-nu.mgz')
        inorm = jurt.core.Dataset(self._prefix + '-anat-inorm.mgz')
        lta   = jurt.core.Dataset(self._prefix + '-anat-talairach-with-skull.lta')

        # Check if output already exists (delete if overwriting)
        brainmask_inorm = self._prefix + '-anat-inorm-hwa.mgz'
        brainmask_nu    = self._prefix + '-anat-nu-hwa.mgz'
        brainmask_anat  = self._prefix + '-anat-hwa.mgz'
        log             = self._prefix + '-HwaT1.log'
        outfiles = (brainmask_inorm, brainmask_nu, brainmask_anat, log)

        for f in outfiles:
            if os.path.isfile(f):
                if self._overwrite:
                    os.remove(f)
                else:
                    raise IOError(f'{f} already exists')

        try:
            env = os.environ
            env['OMP_NUM_THREADS'] = str(self._threads)
            with open(log, 'w', buffering=1) as lf:

                # Run mri_watershed
                self._cmd('mri_watershed',
                    '-T1',
                    '-h', str(self._preflood),
                    '-brain_atlas', self._gca, lta,
                    inorm,
                    brainmask_inorm,
                    env=env,
                    redirect=lf)

                # Apply the brainmask to nu and anat datasets

                self._cmd('mri_mask',
                    anat,
                    brainmask_inorm,
                    brainmask_anat,
                    env=env,
                    redirect=lf)

                self._cmd('mri_mask',
                    nu,
                    brainmask_inorm,
                    brainmask_nu,
                    env=env,
                    redirect=lf)

        except:
            for f in outfiles:
                if os.path.isfile(f):
                    os.remove(f)
            raise

###############################################################################

class GcutT1(FsPipeline):
    """Remove additional non-brain tissue using Freesurfer's mri_gcut."""

    _thresh_default = 0.4

    @classmethod
    def parser(cls):
        """Return an argument parser for scripts that use GcutT1 objects"""
        p = argparse.ArgumentParser(add_help=False, allow_abbrev=False,
            parents=[cls.__base__.parser()])
        g1 = p.add_argument_group('Options')
        g1.add_argument('-thresh', metavar='t',
            type=float, default=GcutT1._thresh_default,
            help=GcutT1.thresh.__doc__)
        g1.add_argument('-help', action='help',
            help='Show this help message and exit')
        return p

    @classmethod
    def main(cls, ns):
        """Run the GcutT1 pipeline using an argparse namespace"""
        jurt.core._pipeline_main(cls, ns)

    def __init__(self):
        super().__init__()

        # Threshold (-T) for mri_gcut
        self._thresh = GcutT1._thresh_default

    def __str__(self):
        return super().__str__() + '\n  %-20s : %s' % ('thresh', self._thresh)

    @property
    def thresh(self):
        """gcut threshold(s) (percent of white matter intensity)"""
        return self._thresh

    @thresh.setter
    def thresh(self, thresh):
        # Default is 0.4
        # Range: (0-1)
        if type(thresh) is int:
            thresh = float(thresh)
        if type(thresh) is not float:
            raise TypeError('thresh must be numeric')
        if thresh <= 0.0 or thresh >= 1.0:
            raise ValueError('thresh must be in the range (0.0,1.0)')
        self._thresh = thresh

    def pipeline(self):

        # Check the input files
        anat  = jurt.core.Dataset(self._prefix + '-anat.mgz')
        nu    = jurt.core.Dataset(self._prefix + '-anat-nu.mgz')
        inorm = jurt.core.Dataset(self._prefix + '-anat-inorm.mgz')
        hwa   = jurt.core.Dataset(self._prefix + '-anat-inorm-hwa.mgz')

        # Check if output already exists (delete if overwriting)
        gcut_inorm = self._prefix + '-anat-inorm-gcut.mgz'
        gcut_nu    = self._prefix + '-anat-nu-gcut.mgz'
        gcut_anat  = self._prefix + '-anat-gcut.mgz'
        log  = self._prefix + '-GcutT1.log'
        outfiles = (gcut_inorm, gcut_nu, gcut_anat, log)

        for f in outfiles:
            if os.path.isfile(f):
                if self._overwrite:
                    os.remove(f)
                else:
                    raise IOError(f'{f} already exists')

        try:
            env = os.environ
            env['OMP_NUM_THREADS'] = str(self._threads)
            with open(log, 'w', buffering=1) as lf:

                # Run mri_gcut
                self._cmd('mri_gcut',
                    '-110',
                    '-T', str(self._thresh),
                    '-mult', hwa,
                    inorm,
                    gcut_inorm,
                    env=env,
                    redirect=lf)

                # Apply the brainmask to nu and anat datasets

                self._cmd('mri_mask',
                    anat,
                    gcut_inorm,
                    gcut_anat,
                    env=env,
                    redirect=lf)

                self._cmd('mri_mask',
                    nu,
                    gcut_inorm,
                    gcut_nu,
                    env=env,
                    redirect=lf)

        except:
            for f in outfiles:
                if os.path.isfile(f):
                    os.remove(f)
            raise

###############################################################################

if __name__ == '__main__':
    raise RuntimeError('jurt/t1.py cannot be directly executed')

###############################################################################

