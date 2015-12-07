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

from test_init import make_init
import xenon
from nose.tools import (assert_raises, assert_not_equal, assert_equals)


def test_xenon():
    make_init()
    import jnius
    x = xenon.Xenon()
    assert_not_equal(None, x.xenon)
    assert_equals(jnius.JavaMethod, type(x.jobs))
    x.close()
    assert_equals(None, x.xenon)
    assert_raises(ValueError, x.__getattr__, 'jobs')
    assert_raises(ValueError, x.close)


def test_xenon_closeable():
    make_init()
    import jnius
    with xenon.Xenon() as x:
        assert_equals(jnius.JavaMethod, type(x.jobs))


def test_xenon_destructor():
    x = xenon.Xenon()
    del x
