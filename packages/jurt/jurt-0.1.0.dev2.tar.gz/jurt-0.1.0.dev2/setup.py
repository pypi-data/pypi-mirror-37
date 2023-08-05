# jurt: Jeff's Unified Registration Tool
#
# Copyright (c) 2018, Jeffrey M. Engelmann
#
# jurt is released under the revised (3-clause) BSD license.
# For details, see LICENSE.txt
#

import sys
import os
import io
import setuptools

def main():
    """Configure and build the jurt package"""

    # Set the version string
    # This is automatically updated by bumpversion (see .bumpversion.cfg)
    version = '0.1.0.dev2'

    # Dependency lists
    python_requires='>=3.6'
    install_requires=[]

    # Set package metadata
    name = 'jurt'
    description = "Jeff's Unified Registration Tool"
    jme = 'Jeffrey M. Engelmann'
    jme_email = 'jme2041@icloud.com'
    url = 'https://github.com/jme2041/jurt'

    # Get the package's long description from README.md
    here = os.path.abspath(os.path.dirname(__file__))
    with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = f.read().replace(
            '(LICENSE.txt)',
            '(%s/blob/master/LICENSE.txt)' % url)
    long_description_content_type = 'text/markdown'

    # Entry points
    entry_points = { 'console_scripts': 'jurt = jurt.__main__:main' }

    # Call setuptools.setup for the package
    setuptools.setup(
        name=name,
        version=version,
        description=description,
        long_description=long_description,
        long_description_content_type=long_description_content_type,
        license='BSD 3-Clause License',
        url=url,
        author=jme,
        author_email=jme_email,
        maintainer=jme,
        maintainer_email=jme_email,
        classifiers=[
            'Development Status :: 2 - Pre-Alpha',
            'License :: OSI Approved :: BSD License',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: Implementation :: CPython',
            'Operating System :: MacOS :: MacOS X',
            'Operating System :: POSIX :: Linux',
            'Environment :: Console',
            'Natural Language :: English',
            'Intended Audience :: Science/Research',
            'Topic :: Scientific/Engineering :: Bio-Informatics'
        ],
        keywords='mri fmri analysis preprocessing registration normalization',
        packages=setuptools.find_packages(exclude=['test']),
        test_suite='test.get_suite',
        python_requires=python_requires,
        install_requires=install_requires,
        entry_points=entry_points)

if __name__ == '__main__':
    sys.exit(main())

