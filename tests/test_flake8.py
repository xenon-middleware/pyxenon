# pyxenon
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

""" Run flake8 tests on all Python files """

from flake8.api import legacy as flake8
import os
import logging

# flake8 is logging is really verbose. disable.
logging.disable(logging.CRITICAL)


def test_flake8():
    """ Syntax and style check with flake8. """
    for test in apply_flake8(directories=['tests', 'scripts', 'xenon'],
                             files=['setup.py']):
        yield test


def assert_zero(func, *args):
    """ Assert that given function with given arguments returns zero. """
    assert func(*args) == 0, "flake8 found a warning or error"


def apply_flake8(directories=(), files=()):
    """ Yield tests where flake8 runs recursively over given files and
    directories. """
    for directory in directories:
        for path, dirs, file_names in os.walk(directory):
            yield assert_zero, check_file_flake8, [
                os.path.join(os.path.abspath(path), file_name)
                for file_name in file_names
                if file_name.endswith('.py')
            ]

    yield assert_zero, check_file_flake8, [os.path.abspath(f) for f in files]


def check_file_flake8(paths):
    if len(paths) > 0:
        return flake8.get_style_guide().check_files(paths).total_errors
    else:
        return 0
