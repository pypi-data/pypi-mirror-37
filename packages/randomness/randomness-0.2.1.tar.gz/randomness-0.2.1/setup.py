#!/usr/bin/env python3
#  -*- coding: utf-8 -*-

"""Setup for randomness."""

import re

from ast import literal_eval
from os import chdir
from pathlib import Path
from setuptools import setup, find_packages


def get_version(filename='version.py', path=''):
    """Build version number from git repository tag."""

    version_file_path = Path(path).joinpath(filename)

    try:
        with open(version_file_path, 'r') as f:
            version_file_content = f.read()

    except FileNotFoundError:
        m = None

    else:
        m = re.match(r'^\s*version\s*=\s*(?P<version>.*)$',
                     version_file_content, re.M)

    return literal_eval(m.group('version')) if m else None


def get_long_description(filename='README.md', path=''):
    """Read long description from file."""

    description_file_path = Path(path).joinpath(filename)

    try:
        with open(description_file_path, 'r') as f:
            description_file_content = f.read()

    except FileNotFoundError:
        return None

    return description_file_content


if __name__ == '__main__':
    chdir(Path(__file__).parent)
    setup(
            name='randomness',
            # version=get_version(),
            use_scm_version={
                'write_to': 'randomness/_version.py',
            },
            author='Niels Boehm',
            author_email='blubberdiblub@gmail.com',
            description="Provide several randomness sources"
                        " in Python with a common API",
            long_description=get_long_description(),
            long_description_content_type='text/markdown',
            license='MIT',
            keywords=[
                'randomness',
                'random',
                'RNG',
                'entropy',
            ],
            url='https://github.com/blubberdiblub/randomness',
            project_urls={
                'Source': 'https://github.com/blubberdiblub/randomness',
                'Tracker':
                    'https://github.com/blubberdiblub/randomness/issues',
            },
            python_requires='>=3.6',
            setup_requires=[
                'setuptools_scm',
            ],
            install_requires=[
            ],
            extras_require={
                'rdrand': ['rdrand'],
                'test': ['pytest'],
            },
            test_suite='tests',
            packages=find_packages(exclude=[
                'tests',
                'tests.*',
                '*.tests',
                '*.tests.*',
            ]),
            zip_safe=True,
            classifiers=[
                'Development Status :: 3 - Alpha',
                'Intended Audience :: Developers',
                'Intended Audience :: Science/Research',
                'License :: OSI Approved :: MIT License',
                'Operating System :: OS Independent',
                'Programming Language :: Python',
                'Programming Language :: Python :: 3',
                'Programming Language :: Python :: 3 :: Only',
                'Programming Language :: Python :: 3.6',
                'Programming Language :: Python :: 3.7',
                'Topic :: Scientific/Engineering',
                'Topic :: Scientific/Engineering :: Mathematics',
                'Topic :: Software Development',
                'Topic :: Software Development :: Libraries',
                'Topic :: Software Development :: Libraries :: Python Modules',
            ],
        )
