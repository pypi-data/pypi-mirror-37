#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import codecs

from glob import glob
from os.path import basename
from os.path import splitext
from setuptools import setup
from setuptools import find_packages


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding='utf-8').read()


setup(
    name='live-testing-coverage',
    version='0.1.0',
    author='François Perin',
    author_email='francois_perin@hotmail.fr',
    maintainer='François Perin',
    maintainer_email='francois_perin@hotmail.fr',
    license='MIT',
    url='https://github.com/sGeeK44/python-live-testing/live-testing-coverage',
    description='Detect code covered by tests',
    long_description=read('README.rst'),
    packages=find_packages('live-testing-coverage'),
    package_dir={'': 'live-testing-coverage'},
    py_modules=[splitext(basename(path))[0] for path in glob('live-testing-coverage/*.py')],
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*',
    install_requires=['pytest>=3.5.0'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Pytest',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
    ],
    entry_points={
        'pytest11': [
            'live-testing-coverage = plugin',
        ],
    },
)
