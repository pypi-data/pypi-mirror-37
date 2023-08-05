"""
fastq_deconcatenate setup.py
Created on: 9th October, 2018
Proprietary and confidential information of Oxford Nanopore Technologies, Limited
All rights reserved; (c)2018: Oxford Nanopore Technologies, Limited

Provides a simple script to attempt to fix errors in fastq files where two
records have been concatenated together.

e.g.

@id1
AAA
+
\\\@id2
CCC
+
\\\

"""

import os
from setuptools import find_packages, setup
import re

__pkg_name__ = 'ont_fastq_deconcatenate'

initfile = open(os.path.join(__pkg_name__, '__init__.py'), 'r').read()
version_regex = r"^__version__ = ['\"]([^'\"]*)['\"]"
mo = re.search(version_regex, initfile, re.M)
if mo:
    version = mo.group(1)
else:
    raise RuntimeError('Unable to find version string in '
                       '"ont_fastq_deconcatentate/__init__.py".')

setup_kwargs = {
    'name': __pkg_name__.replace('_', '-'),
    'description': 'Fixes concatenated fastq records',
    'long_description': '',
    'author': 'Oxford Nanopore Technologies, Limited',
    'author_email': 'unknown@unknown.com',
    'version': version,
    'url': 'http://www.nanoporetech.com',
    'packages': find_packages(),
    'install_requires': ['biopython >= 1.66', 'progressbar33'],
    'classifiers': [
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: C++',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
    ],
    'entry_points': {'console_scripts': [
        'fix_concatenated_fastqs={}.cli:main'.format(__pkg_name__)
    ]}
}

setup(**setup_kwargs)
