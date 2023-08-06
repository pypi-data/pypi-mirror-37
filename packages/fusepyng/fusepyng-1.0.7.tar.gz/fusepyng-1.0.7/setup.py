#!/usr/bin/env python

from __future__ import with_statement

from setuptools import setup

with open('README') as readme:
    documentation = readme.read()

setup(
    name = 'fusepyng',
    version='1.0.7',
    description = 'Simple ctypes bindings for FUSE',
    long_description = documentation,
    author = 'Giorgos Verigakis',
    author_email = 'verigak@gmail.com',
    maintainer = 'Rian Hunter',
    maintainer_email = 'rian@alum.mit.edu',
    license = 'ISC',
    py_modules=['fusepyng'],
    url = 'http://github.com/rianhunter/fusepyng',

    classifiers = [
        'Intended Audience :: Developers',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Operating System :: MacOS',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 3',
        'Topic :: System :: Filesystems',
    ]
)
