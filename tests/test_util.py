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
import os
import xenon
from nose.tools import assert_equals


def test_module_path():
    """ Test module path recognition """
    cd = os.path.join(os.getcwd(), 'tests', 'test_util.py')
    mpath = xenon.module_path(test_module_path)
    assert_equals(os.path.realpath(cd), os.path.realpath(mpath))


def test_module_path_default():
    """ Test module path recognition """
    cd = os.path.join(os.getcwd(), 'xenon', 'util.py')
    mpath = xenon.module_path()
    assert_equals(os.path.realpath(cd), os.path.realpath(mpath))
