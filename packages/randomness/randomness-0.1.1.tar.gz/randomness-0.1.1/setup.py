#!/usr/bin/env python3
#  -*- coding: utf-8 -*-

"""Setup for randomness."""

import errno
import re
import subprocess

from ast import literal_eval
from os import chdir
from os.path import dirname
from setuptools import setup, find_packages


def get_version(filename='version.py'):
    """Build version number from git repository tag."""

    try:
        f = open(filename, 'r')

    except IOError as e:
        if e.errno != errno.ENOENT:
            raise

        m = None

    else:
        m = re.match(r'^\s*__version__\s*=\s*(?P<version>.*)$', f.read(), re.M)
        f.close()

    __version__ = literal_eval(m.group('version')) if m else None

    try:
        git_version = subprocess.check_output(['git',
                                               'describe',
                                               '--dirty',
                                               '--tags',
                                               '--long',
                                               '--always']).decode()

    except subprocess.CalledProcessError:
        if __version__ is None:
            raise ValueError("cannot determine version number")

        return __version__

    m = re.match(r'^\s*'
                 r'(?P<version>\S+?)'
                 r'(-(?P<post>\d+)-(?P<commit>g[0-9a-f]+))?'
                 r'(-(?P<dirty>dirty))?'
                 r'\s*$', git_version)
    if not m:
        raise ValueError("cannot parse git describe output")

    git_version = m.group('version')
    post = m.group('post')
    commit = m.group('commit')
    dirty = m.group('dirty')

    local = []

    if post and int(post) != 0:
        git_version += '.post%d' % (int(post),)
        if commit:
            local.append(commit)

    if dirty:
        local.append(dirty)

    if local:
        git_version += '+' + '.'.join(local)

    if git_version != __version__:
        with open(filename, 'w') as f:
            f.write("__version__ = %r\n" % (git_version,))

    return git_version


def get_long_description(filename='README.md'):
    """Convert description to reStructuredText format."""

    try:
        with open(filename, 'r') as f:
            description = f.read()

    except OSError as e:
        if e.errno != errno.ENOENT:
            raise

        return None

    try:
        process = subprocess.Popen([
                'pandoc',
                '-f', 'markdown_github',
                '-t', 'rst',
            ],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            universal_newlines=True,
            )

    except OSError as e:
        if e.errno == errno.ENOENT:
            return None

        raise

    description, __ = process.communicate(input=description)

    if process.poll() is None:
        process.kill()
        raise Exception("pandoc did not terminate")

    if process.poll():
        raise Exception("pandoc terminated abnormally")

    return description


if __name__ == '__main__':
    chdir(dirname(__file__))
    setup(
            name='randomness',
            version=get_version(),
            author='Niels Boehm',
            author_email='blubberdiblub@gmail.com',
            description="Provide several randomness sources"
                        " in Python with a common API",
            long_description=get_long_description(),
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
                'Tracker': 'https://github.com/blubberdiblub/randomness/issues',
            },
            python_requires='>=3.6',
            install_requires=[
            ],
            # extras_require={
            #     },
            test_suite='tests',
            py_modules=[
                'randomness',
            ],
            # packages=find_packages(exclude=[
            #     'tests',
            #     'tests.*',
            #     '*.tests',
            #     '*.tests.*',
            # ]),
            include_package_data=True,
            zip_safe=False,
            # entry_points={
            #     'console_scripts': [
            #     ],
            # },
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
