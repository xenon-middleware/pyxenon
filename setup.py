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
"""

from setuptools import setup
import os

# Get the long description from the README file
with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as f:
    long_description = f.read()

setup(name='pyxenon',
      version='0.3',
      description='Python wrapper for the Xenon API.',
      long_description=long_description,
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
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Topic :: System :: Distributed Computing',
      ],
      package_data={'xenon': ['libs/*.jar', 'libs/*.xml']},
      install_requires=['JPype1'],
      extras_require={
          'test': ['pytest', 'pytest-flake8', 'coverage'],
      },
      )
