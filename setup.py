#!/usr/bin/env python
# PyXenon Xenon API wrapper
#
# Copyright 2015 Netherlands eScience Center
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Internal setup of the xenon package.

Use make install instead for correct dependency detection.
"""

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from glob import glob
import os

# install libraries
from distutils.command.install import INSTALL_SCHEMES
for scheme in INSTALL_SCHEMES.values():
    scheme['data'] = scheme['purelib']

jar_files = list(glob(os.path.join('libs', '*.jar')))
config_files = list(glob(os.path.join('libs', '*.xml')))
data_files = [('libs', jar_files + config_files)]

setup(name='pyxenon',
      version='0.1.0',
      description='Python wrapper for the Xenon API.',
      author='Joris Borgdorff',
      author_email='j.borgdorff@esciencecenter.nl',
      url='https://github.com/NLeSC/pyxenon',
      packages=['xenon'],
      classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Environment :: Console',
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: System :: Distributed Computing'
      ],
      data_files=data_files,
      install_requires=['cython', 'jnius'],
      tests_require=['nose', 'pyflakes', 'pep8', 'coverage']
     )
