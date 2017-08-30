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

""" Test Xenon class """

import xenon
from jpype._jclass import _jpype
import pytest


def test_xenon():
    """ Test Xenon initialization, attributes and closing. """
    x = xenon.Xenon()
    assert x.xenon is not None
    assert _jpype._JavaBoundMethod == type(x.jobs)  # noqa
    x.close()
    assert x.xenon is None
    with pytest.raises(ValueError):
        _ = x.jobs  # noqa
    with pytest.raises(ValueError):
        x.close()


def test_xenon_with():
    """ Test Xenons with-resources syntax """
    with xenon.Xenon() as x:
        assert _jpype._JavaBoundMethod == type(x.jobs)  # noqa


def test_xenon_destructor():
    """ Test Xenons del operator """
    x = xenon.Xenon()
    del x
