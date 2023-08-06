#!/usr/bin/env python3
#  -*- coding: utf-8 -*-

"""Setup for randomness."""

import re
import subprocess

from ast import literal_eval
from os import chdir
from os.path import dirname
from setuptools import setup, find_packages

import packaging.version


class Version(packaging.version.Version):

    def _build_new(self, *extra: str) -> 'Version':

        parts = [self.base_version]

        if self.pre:
            parts.extend(str(part) for part in self.pre)

        parts.extend(extra)

        return self.__class__(''.join(parts))

    def _build_with_local(self, *extra: str) -> 'Version':

        if not self.local:
            return self._build_new(*extra)

        return self._build_new(*extra, '+', self.local)

    def get_base_and_pre(self) -> 'Version':

        return self._build_new()

    def replace_post(self, post: int) -> 'Version':

        if int(post) != post:
            raise TypeError("post must be integral")

        post = int(post)
        if post <= 0:
            raise ValueError("post must be greater than zero")

        return self._build_with_local('.post', str(post))

    def replace_dev(self, dev: int) -> 'Version':

        if int(dev) != dev:
            raise TypeError("dev must be integral")

        dev = int(dev)
        if dev <= 0:
            raise ValueError("dev must be greater than zero")

        extra = ['.post', str(self.post)] if self.post is not None else []

        return self._build_with_local(*extra, '.dev', str(dev))

    def replace_local(self, *local: str) -> 'Version':

        extra = []

        if self.post is not None:
            extra += ['.post', str(self.post)]

        if self.dev is not None:
            extra += ['.dev', str(self.dev)]

        local = [part for part in local if part]
        if local:
            extra += ['+', '.'.join(local)]

        return self._build_new(*extra)


def get_version(filename='version.py'):
    """Build version number from git repository tag."""

    try:
        with open(filename, 'r') as f:
            version_file_content = f.read()

    except FileNotFoundError:
        m = None

    else:
        m = re.match(r'^\s*__version__\s*=\s*(?P<version>.*)$',
                     version_file_content, re.M)

    __version__ = Version(literal_eval(m.group('version'))) if m else None

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

        return str(__version__)

    m = re.match(r'^\s*'
                 r'(?P<version>\S+?)'
                 r'(-(?P<increment>\d+)-(?P<commit>g[0-9a-f]+))?'
                 r'(-(?P<dirty>dirty))?'
                 r'\s*$', git_version)
    if not m:
        raise ValueError("cannot parse git describe output")

    git_version = Version(m.group('version'))
    increment = m.group('increment')
    commit = m.group('commit')
    dirty = m.group('dirty')

    if increment and int(increment) != 0:
        increment = int(increment)

        if (__version__ is not None and
                __version__.get_base_and_pre() >
                git_version.get_base_and_pre()):
            git_version = __version__.replace_dev(increment)

        else:
            git_version = git_version.replace_post(increment)

    if __version__ is None or git_version != __version__:
        with open(filename, 'w') as f:
            f.write('__version__ = {!r}\n'.format(str(git_version)))

    if dirty:
        if commit:
            git_version = git_version.replace_local(commit, dirty)

        else:
            git_version = git_version.replace_local(dirty)

    return str(git_version)


def get_long_description(filename='README.md'):
    """Read long description from file."""

    try:
        with open(filename, 'r') as f:
            description = f.read()

    except FileNotFoundError:
        return None

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
                'packaging',
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
