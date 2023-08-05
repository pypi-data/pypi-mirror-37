#!/usr/bin/env python3
#
# -----------------------------------------------------------------------------
# Copyright (c) 2018, Battelle National Biodefense Institute.
#
# This file is part of happer (http://github.com/bioforensics/happer) and is
# licensed under the BSD license: see LICENSE.txt.
# -----------------------------------------------------------------------------

from setuptools import setup
import versioneer


desc = 'Library for applying haplotypes to reference DNA sequences'
with open('README.md', 'r') as infile:
    longdesc = infile.read()

setup(
    name='happer',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description=desc,
    long_description=longdesc,
    long_description_content_type='text/markdown',
    url='https://github.com/bioforensics/happer',
    author='Daniel Standage',
    author_email='daniel.standage@nbacc.dhs.gov',
    packages=['happer', 'happer.tests'],
    package_data={
        'happer': ['happer/tests/data/*']
    },
    include_package_data=True,
    # install_requires=dependencies,
    entry_points={
        'console_scripts': ['happer = happer.__main__:main']
    },
    classifiers=[
        'Environment :: Console',
        'Framework :: IPython',
        'Framework :: Jupyter',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
    ],
    zip_safe=True,
)
