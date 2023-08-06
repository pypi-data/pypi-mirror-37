"""jurt's Registration module

Unified motion correction, coregistration, and spatial normalization.
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

def nvols(dset):
    """Return the number of volumes in a dataset"""
    import subprocess

    if not os.path.isfile(dset):
        raise IOError(f'Could not find dataset: {dset}')
    cmd = subprocess.Popen(['fslnvols', dset], stdout=subprocess.PIPE)
    o, e = cmd.communicate()
    if cmd.returncode != 0:
        raise RuntimeError('fslnvols failed')
    return int(o.decode().splitlines()[0])

###############################################################################

class PrepFunc(jurt.core.FslPipeline):
    """Preprocess functional dataset

    Convert the functional dataset to FSL's preferred orientation and data
    type, extract the base volume, and run motion-correction using FSL's
    MCFLIRT.
    """

    @classmethod
    def parser(cls):
        """Return an argument parser for scripts that use PrepFunc objects"""
        p = argparse.ArgumentParser(add_help=False, allow_abbrev=False,
            parents=[cls.__base__.parser()])
        g1 = p.add_argument_group('Required parameters')
        g1.add_argument('-func', required=True, metavar='DSET',
            help=PrepFunc.func.__doc__)
        g1.add_argument('-basevol', required=True, metavar='v', type=int,
            help=PrepFunc.basevol.__doc__)
        g2 = p.add_argument_group('Options')
        g2.add_argument('-help', action='help',
            help='Show this help message and exit')
        return p

    @classmethod
    def main(cls, ns):
        """Run the PrepFunc pipeline using an argparse namespace"""
        jurt.core._pipeline_main(cls, ns)

    def __init__(self):
        super().__init__()

        # Set defaults
        self._func    = None
        self._basevol = None
        self._nvols   = 0       # Number of volumes in _func

    def __str__(self):
        return super().__str__() + (
            '\n  %-20s : %s\n  %-20s : %s\n  %-20s : %d' % (
            'Functional dataset', self._func,
            'Base volume', self._basevol,
            'fMRI volumes', self._nvols))

    @property
    def func(self):
        """Functional dataset"""
        return self._func

    @func.setter
    def func(self, func):
        self._func = jurt.core.Dataset(func)
        self._nvols = nvols(func)

    @property
    def basevol(self):
        """Registration base volume (functional dataset)"""
        return self._basevol

    @basevol.setter
    def basevol(self, basevol):
        if type(basevol) is not int:
            raise TypeError('basevol must be an integer')
        if basevol < 0:
            raise ValueError('basevol cannot be negative')
        self._basevol = basevol

    def pipeline(self):

        if self.func is None:
            raise RuntimeError(
                f'func must be set prior to {type(self).__name__}.run()')

        if self.basevol is None:
            raise RuntimeError(
                f'basevol must be set prior to {type(self).__name__}.run()')

        if self.basevol >= self._nvols:
            raise ValueError(
                f'basevol out of range for dataset {self.func} [0, {self._nvols})')

        # Check if output already exists (delete if overwriting)
        ts_out   = self._prefix + '-func.nii'       # fMRI time series
        base_out = self._prefix + '-func-base.nii'  # fMRI base volume
        mcf_out  = self._prefix + '-func-mc.nii'    # Motion-corrected time series
        mat_dir  = self._prefix + '-func-mc.mat'    # Tx matrix directory
        par_out  = self._prefix + '-func-mc.par'    # Tx parameters file
        log      = self._prefix + '-PrepFunc.log'   # Log
        outfiles = (ts_out, base_out, mcf_out, par_out, log)

        self._log.debug(f'output: {mat_dir}')
        if os.path.isdir(mat_dir):
            if self._overwrite:
                shutil.rmtree(mat_dir)
            else:
                raise IOError(f'{mat_dir} already exists')

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

                    # Re-orient the input data to FSL's preferred orientation
                    tf = os.path.join(td, 'tmp.nii')
                    self._cmd('fslreorient2std',
                        self._func,
                        tf.replace('.nii', ''),
                        env=env,
                        redirect=lf)

                    # Convert the input data to floating-point format
                    self._cmd('fslmaths',
                        tf,
                        ts_out.replace('.nii', ''),
                        '-odt', 'float',
                        env=env,
                        redirect=lf)

                    # Extract the base volume
                    self._cmd('fslroi',
                        ts_out,
                        base_out.replace('.nii',''),
                        str(self.basevol),
                        str(1),
                        env=env,
                        redirect=lf)

                    # Run motion correction using mcflirt
                    self._cmd('mcflirt',
                        '-in', ts_out,
                        '-out', mcf_out.replace('.nii',''),
                        '-mats',
                        '-plots',
                        '-reffile', base_out.replace('.nii',''),
                        '-spline_final',
                        env=env,
                        redirect=lf)
        except:
            if os.path.isdir(mat_dir):
                shutil.rmtree(mat_dir)
            for f in outfiles:
                if os.path.isfile(f):
                    os.remove(f)
            raise
        finally:
            os.chdir(wd)

###############################################################################

class FuncToT1(jurt.core.FslPipeline):
    """Co-register functional dataset to T1-weighted dataset"""

    _valid_methods = ('bbr', '6dof')


    @classmethod
    def parser(cls):
        """Return an argument parser for scripts that use FuncToT1 objects"""
        p = argparse.ArgumentParser(add_help=False, allow_abbrev=False,
            parents=[cls.__base__.parser()])
        g1 = p.add_argument_group('Required parameters')
        g1.add_argument('-method', required=True,
            choices=FuncToT1._valid_methods,
            help=FuncToT1.method.__doc__)
        g2 = p.add_argument_group('Options')
        g2.add_argument('-help', action='help',
            help='Show this help message and exit')
        return p

    @classmethod
    def main(cls, ns):
        """Run the FuncToT1 pipeline using an argparse namespace"""
        jurt.core._pipeline_main(cls, ns)

    def __init__(self):
        super().__init__()

        # Set defaults
        self._method = None

    def __str__(self):
        return super().__str__() + (
            '\n  %-20s : %s' % ('Registration method', self._method))

    @property
    def method(self):
        return self._method

    @method.setter
    def method(self, method):
        if not isinstance(method, str):
            raise TypeError('method must be a string')
        if not method in FuncToT1._valid_methods:
            raise ValueError('method must be one of: {0:s}'.format(
                ', '.join(FuncToT1._valid_methods)))
        self._method = method

    def pipeline(self):

        if self.method is None:
            raise RuntimeError(
                f'method must be set prior to {type(self).__name__}.run()')

        # Check input datasets
        func     = jurt.core.Dataset(self._prefix + '-func-base.nii')
        t1_head  = jurt.core.Dataset(self._prefix + '-t1-nu.nii')
        t1_brain = jurt.core.Dataset(self._prefix + '-t1-nu-brain.nii')

        # Check if the output already exists (delete if overwriting)
        out  = self._prefix + '-func-base-t1.nii'
        omat = self._prefix + '-func-base-to-t1.mat'
        log  = self._prefix + '-FuncToT1.log'
        outfiles = (out, omat, log)

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

                    init_out = os.path.join(td, 'tmp.nii')
                    init_mat = os.path.join(td, 'tmp.mat')

                    if self._method == '6dof':
                        init_mat = omat

                    # 6-DOF registration
                    # This serves as the "initial" registration for BBR and
                    # as the "final" registration for 6dof
                    # Specify "normal" search radius of 90 degrees b/c all data
                    # have been reoriented to FSL standard orientation

                    self._cmd('flirt',
                        '-ref'      , t1_brain,
                        '-in'       , func,
                        '-out'      , init_out.replace('.nii',''),
                        '-omat'     , init_mat,
                        '-cost'     , 'corratio',
                        '-dof'      , str(6),
                        '-searchrx' , str(-90), str(90),
                        '-searchry' , str(-90), str(90),
                        '-searchrz' , str(-90), str(90),
                        '-interp'   , 'trilinear',
                        env=env,
                        redirect=lf)

                    # BBR

                    if self._method == 'bbr':

                        bbr_out = os.path.join(td, 'bbr.nii')
                        wmseg   = jurt.Dataset(self._prefix +
                                  '-t1-nu-brain-wmseg.nii')
                        sch     = os.path.join(os.environ['FSLDIR'], 'etc',
                                  'flirtsch', 'bbr.sch')
                        if not os.path.isfile(sch):
                            raise IOError(
                                f'Could not find FLIRT BBR schedule: {sch}')

                        self._cmd('flirt',
                            '-ref'      , t1_head,
                            '-in'       , func,
                            '-dof'      , str(6),
                            '-cost'     , 'bbr',
                            '-searchrx' , str(-90), str(90),
                            '-searchry' , str(-90), str(90),
                            '-searchrz' , str(-90), str(90),
                            '-wmseg'    , wmseg,
                            '-init'     , init_mat,
                            '-omat'     , omat,
                            '-out'      , bbr_out.replace('.nii',''),
                            '-interp'   , 'trilinear',
                            '-schedule' , sch)

                    # Final output with sinc interpolation
                    # Apply the transformation in omat using sinc interpolation

                    self._cmd('applywarp',
                        '-i', func,
                        '-r', t1_head,
                        '-o', out.replace('.nii',''),
                        f'--premat={omat}',
                        '--interp=spline',
                        env=env,
                        redirect=lf)

        except:
            for f in outfiles:
                if os.path.isfile(f):
                    os.remove(f)
            raise

        finally:
            os.chdir(wd)

###############################################################################

class T1ToStd(jurt.core.FslPipeline):
    """Spatially normalize T1-weighted dataset to standard space

    Transform the nonuniformity-corrected T1-weighted dataset into standard
    stereotaxic space using a 12-DOF (full affine) registration.

    The standard space dataset is MNI152_T1_2mm_brain
    """

    @classmethod
    def parser(cls):
        """Return an argument parser for scripts that use T1ToStd objects"""
        p = argparse.ArgumentParser(add_help=False, allow_abbrev=False,
            parents=[cls.__base__.parser()])
        g1 = p.add_argument_group('Options')
        g1.add_argument('-help', action='help',
            help='Show this help message and exit')
        return p

    @classmethod
    def main(cls, ns):
        """Run the T1ToStd pipeline using an argparse namespace"""
        jurt.core._pipeline_main(cls, ns)

    def __init__(self):
        super().__init__()

    def __str__(self):
        return super().__str__()

    def pipeline(self):

        # Check the input datasets (template already verified by FslPipeline)
        t1_head  = jurt.core.Dataset(self._prefix + '-t1-nu.nii')
        t1_brain = jurt.core.Dataset(self._prefix + '-t1-nu-brain.nii')

        # Check if the output already exists (delete if overwriting)
        out  = self._prefix + '-t1-std.nii'
        omat = self._prefix + '-t1-to-std.mat'
        log  = self._prefix + '-T1ToStd.log'
        outfiles = (out, omat, log)

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
            env['FSLOUTPUTTYPE'] = 'NIFTI'
            with open(log, 'w', buffering=1) as lf:
                self._cmd('flirt',
                    '-in'       ,  t1_brain,
                    '-ref'      , self._template,
                    '-out'      , out,
                    '-omat'     , omat,
                    '-cost'     , 'corratio',
                    '-dof'      , str(12),
                    '-searchrx' , str(-90), str(90),
                    '-searchry' , str(-90), str(90),
                    '-searchrz' , str(-90), str(90),
                    '-interp'   , 'trilinear',
                    env=env,
                    redirect=lf)

        except:
            for f in outfiles:
                if os.path.isfile(f):
                    os.remove(f)
            raise

###############################################################################

class FuncToStd(jurt.core.FslPipeline):
    """Spatially normalize functional dataset"""

    @classmethod
    def parser(cls):
        """Return an argument parser for scripts that use FuncToStd objects"""
        p = argparse.ArgumentParser(add_help=False, allow_abbrev=False,
            parents=[cls.__base__.parser()])
        g1 = p.add_argument_group('Options')
        g1.add_argument('-help', action='help',
            help='Show this help message and exit')
        return p

    @classmethod
    def main(cls, ns):
        """Run the FuncToStd pipeline using an argparse namespace"""
        jurt.core._pipeline_main(cls, ns)

    def __init__(self):
        super().__init__()

    def __str__(self):
        return super().__str__()

    def pipeline(self):

        # Check the input datasets and matrix files
        func    = jurt.core.Dataset(self._prefix + '-func.nii')
        base2t1 = jurt.core.Dataset(self._prefix + '-func-base-to-t1.mat')
        t12std  = jurt.core.Dataset(self._prefix + '-t1-to-std.mat')

        mcmat = self._prefix + '-func-mc.mat'
        if not os.path.isdir(mcmat):
            raise IOError(f'Could not find directory: {mcmat}')

        n = nvols(func)
        for v in range (0, n):
            f = os.path.join(mcmat, 'MAT_{0:04d}'.format(v))
            if not os.path.isfile(f):
                raise IOError(f'Could not find file: {f}')

        # Check if the output already exists (delete if overwriting)
        out      = self._prefix + '-func-std.nii'
        log      = self._prefix + '-FuncToStd.log'
        base2std = self._prefix + '-func-base-to-std.mat'
        omats    = self._prefix + '-func-to-std.mat'
        outfiles = (out, log)

        self._log.debug(f'output {omats}')
        if os.path.isdir(omats):
            if self._overwrite:
                shutil.rmtree(omats)
            else:
                raise IOError(f'{omats} already exists')

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
            env['FSLOUTPUTTYPE'] = 'NIFTI'
            with open(log, 'w', buffering=1) as lf:

                # Concatenate func-to-t1.mat and t1-to-std.mat
                self._cmd('convert_xfm',
                    '-omat', base2std,
                    '-concat',
                    t12std,
                    base2t1,
                    env=env,
                    redirect=lf)

                # Concatenate func2base matrices and base2std to get func2std
                os.mkdir(omats)

                for v in range(0, n):
                    func2std = os.path.join(omats, 'F2S_{0:04d}'.format(v))
                    func2base = os.path.join(mcmat, 'MAT_{0:04d}'.format(v))
                    self._cmd('convert_xfm',
                        '-omat', func2std,
                        '-concat',
                        base2std,
                        func2base,
                        env=env,
                        redirect=lf)

                # Apply the transforms to get func-std.nii
                self._cmd('applyxfm4D',
                    func,
                    self._template,
                    out,
                    omats,
                    '-userprefix', 'F2S_',
                    env=env,
                    redirect=lf)

        except:
            if os.path.isdir(omats):
                shutil.rmtree(omats)
            for f in outfiles:
                if os.path.isfile(f):
                    os.remove(f)

###############################################################################

if __name__ == '__main__':
    raise RuntimeError('jurt/reg.py cannot be directly executed')

###############################################################################

