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
import shutil
import argparse
import tempfile
import logging

import jurt
import jurt.core

###############################################################################

class PrepT1(jurt.core.FsPipeline):
    """Preprocess T1-weighted datasets using FreeSurfer

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
                    orig: f'{self._prefix}-t1.mgz',
                    nu:   f'{self._prefix}-t1-nu.mgz',
                    t1:   f'{self._prefix}-t1-inorm.mgz',
                    xfm:  f'{self._prefix}-t1-talairach.xfm',
                    lta:  f'{self._prefix}-t1-talairach-with-skull.lta',
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

class SST1(jurt.core.FsPipeline):
    """Skull strip T1-weighted datasets

    Removes non-brain tissue from T1-weighted datasets using FreeSurfer's
    Hybrid Watershed Algorithm (HWA) and by optionally applying graph cuts.
    """

    _preflood_default = 25
    _gcut_default     = 0.0
    _gcut_const       = 0.4

    @classmethod
    def parser(cls):
        """Return an argument parser for scripts taht use SST1 objects"""
        p = argparse.ArgumentParser(add_help=False, allow_abbrev=False,
            parents=[cls.__base__.parser()])
        g1 = p.add_argument_group('Options')
        g1.add_argument('-preflood', metavar='h',
            type=int, default=SST1._preflood_default,
            help=SST1.preflood.__doc__)
        g1.add_argument('-gcut', metavar='gthresh', type=float, nargs='?',
            default=SST1._gcut_default,
            const=SST1._gcut_const,
            help=SST1.gcut.__doc__)
        g1.add_argument('-help', action='help',
            help='Show this help message and exit')
        return p

    @classmethod
    def main(cls, ns):
        """Run the SST1 pipeline using an argparse namespace"""
        jurt.core._pipeline_main(cls, ns)

    def __init__(self):
        super().__init__()

        # Preflood height (-h) for mri_watershed
        self._preflood = SST1._preflood_default
        self._gcut     = SST1._gcut_default

    def __str__(self):
        return super().__str__() + (
            '\n  %-20s : %s\n  %-20s : %s' % (
                'preflood', self._preflood,
                'gcut'    , self._gcut))

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

    @property
    def gcut(self):
        """gcut threshold (percent of white matter intensity; 0 = no gcut)"""
        return self._gcut

    @gcut.setter
    def gcut(self, gcut):
        # Default is 0.4
        # Range: (0-1) non-inclusive, 0.0 means don't use gcut
        if type(gcut) is int:
            gcut = float(gcut)
        if type(gcut) is not float:
            raise TypeError('gcut must be numeric')
        if gcut < 0.0 or gcut >= 1.0:
            raise ValueError('gcut must be in the range [0.0,1.0)')
        self._gcut = gcut


    def pipeline(self):

        # Check input files
        inorm = jurt.core.Dataset(self._prefix + '-t1-inorm.mgz')
        lta   = jurt.core.Dataset(self._prefix + '-t1-talairach-with-skull.lta')

        # Check if output already exists (delete if overwriting)
        inorm_brain = self._prefix + '-t1-inorm-brain.mgz'
        log         = self._prefix + '-SST1.log'
        outfiles    = (inorm_brain, log)

        for f in outfiles:
            self._log.debug(f'output {f}')
            if os.path.isfile(f):
                if self._overwrite:
                    os.remove(f)
                else:
                    raise IOError(f'{f} already exists')

        try:
            env = os.environ
            env['OMP_NUM_THREADS'] = str(self._threads)
            with open(log, 'w', buffering=1) as lf:
                with tempfile.TemporaryDirectory(dir=self._scratch) as td:

                    inorm_hwa = inorm_brain
                    if self._gcut > 0.0:
                        inorm_hwa = os.path.join(td, 'hwa.nii')

                    # Run mri_watershed
                    self._cmd('mri_watershed',
                        '-T1',
                        '-h', str(self._preflood),
                        '-brain_atlas', self._gca, lta,
                        inorm,
                        inorm_hwa,
                        env=env,
                        redirect=lf)

                    if self._gcut > 0.0:
                        # Run gcut
                        if not os.path.isfile(inorm_hwa):
                            raise IOError(f'Could not find dataset: {inorm_hwa}')

                        self._cmd('mri_gcut',
                            '-110',
                            '-T', str(self._gcut),
                            '-mult', inorm_hwa,
                            inorm,
                            inorm_brain,
                            env=env,
                            redirect=lf)

        except:
            for f in outfiles:
                if os.path.isfile(f):
                    os.remove(f)
            raise

###############################################################################

class SegT1(jurt.core.FsPipeline, jurt.core.FslPipeline):
    """Segment T1-weighted dataset using FSL's FAST

    This pipeline uses FSL's FAST to segment the brain-extracted T1-weighted
    dataset, keeping the white-matter map for use in coregistration.

    FreeSurfer's mri_mask is used to apply the -t1-inorm-brain.mgz mask to the
    -t1-nu.mgz dataset and this masked, non-uniformity corrected dataset is
    used for segmentation.
    """

    @classmethod
    def parser(cls):
        """Return an argument parser for scripts that use SegT1 objects"""
        p = argparse.ArgumentParser(add_help=False, allow_abbrev=False,
                parents=[cls.__base__.parser()])
        g1 = p.add_argument_group('Options')
        g1.add_argument('-help', action='help',
            help='Show this help message and exit')
        return p

    @classmethod
    def main(cls, ns):
        """Run the SegT1 pipeline using an argparse namespace"""
        jurt.core._pipeline_main(cls, ns)

    def __init__(self):
        jurt.core.FsPipeline.__init__(self)
        jurt.core.FslPipeline.__init__(self)

    def __str__(self):
        return super().__str__()

    def pipeline(self):

        # Check the input datasets
        nu_mgz    = jurt.core.Dataset(self._prefix + '-t1-nu.mgz')
        brainmask = jurt.core.Dataset(self._prefix + '-t1-inorm-brain.mgz')

        # Check if the output already exists (delete if overwriting)
        nu_nii       = self._prefix + '-t1-nu.nii'
        nu_brain_nii = self._prefix + '-t1-nu-brain.nii'
        wmseg_nii    = self._prefix + '-t1-nu-brain-wmseg.nii'
        wmedge_nii   = self._prefix + '-t1-nu-brain-wmedge.nii'
        log          = self._prefix + '-SegT1.log'
        outfiles     = (nu_nii, nu_brain_nii, wmseg_nii, wmedge_nii, log)

        for f in outfiles:
            self._log.debug(f'output {f}')
            if os.path.isfile(f):
                if self._overwrite:
                    os.remove(f)
                else:
                    raise IOError(f'{f} already exists')

        wd = os.getcwd()
        try:
            env = os.environ
            env['OMP_NUM_THREADS'] = str(self._threads)
            env['FSLOUTPUTTYPE'] = 'NIFTI'
            with open(log, 'w', buffering=1) as lf:
                with tempfile.TemporaryDirectory(dir=self._scratch) as td:
                    os.chdir(td)
                    self._log.debug(f'Temporary directory: {td}')

                    # Apply the brainmask to the nu dataset
                    nu_brain_mgz = os.path.join(td, 'nu-brain.mgz')
                    self._cmd('mri_mask',
                        nu_mgz,
                        brainmask,
                        nu_brain_mgz,
                        env=env,
                        redirect=lf)

                    # Convert nu_mgz and nu_brainmask_mgz to NIfTI
                    # Reorient to standard FSL format

                    for i, o, t in zip(
                        (nu_mgz,        nu_brain_mgz),
                        (nu_nii,        nu_brain_nii),
                        ('tmp-nu.nii', 'tmp-nu-brain.nii')):

                        tf = os.path.join(td, t)
                        self._cmd('mri_convert',
                            '-odt', 'float',
                            i,
                            tf,
                            env=env,
                            redirect=lf)

                        self._cmd('fslreorient2std', tf, o, env=env, redirect=lf)

                    # Do the segmentation
                    fast_dset = 'brain-fast'
                    self._cmd('fast',
                        '-v',
                        '-o', fast_dset,
                        nu_brain_nii,
                        env=env,
                        redirect=lf)

                    # Get the white matter map
                    wmseg = 'wmseg'
                    self._cmd('fslmaths',
                        fast_dset + '_pve_2',
                        '-thr', str(0.5),
                        '-bin',
                        wmseg,
                        env=env,
                        redirect=lf)

                    # Create the white matter edge map
                    wmedge = 'wmedge'
                    self._cmd('fslmaths',
                        wmseg,
                        '-edge',
                        '-bin',
                        '-mas',
                        wmseg,
                        wmedge,
                        env=env,
                        redirect=lf)

                    # Copy output to destination
                    shutil.copy2(os.path.join(td, wmseg + '.nii'),  wmseg_nii)
                    shutil.copy2(os.path.join(td, wmedge + '.nii'), wmedge_nii)

        except:
            for f in outfiles:
                if os.path.isfile(f):
                    os.remove(f)
            raise
        finally:
            os.chdir(wd)

###############################################################################

if __name__ == '__main__':
    raise RuntimeError('jurt/t1.py cannot be directly executed')

###############################################################################

