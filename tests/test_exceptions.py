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

""" Test Xenon exceptions """

from test_init import make_init
import xenon
from nose.tools import assert_raises, assert_true


def test_xenon_raises():
    """ Test that Xenon raises a XenonException when given faulty arguments """
    make_init()
    with xenon.Xenon() as x:
        creds = x.credentials()
        cred = creds.newPasswordCredential('ssh', 'wrong-user',
                                           list('wrong-password'), None)
        assert_raises(xenon.exceptions.XenonException, x.jobs().newScheduler,
                      'ssh', 'localhost', cred, None)


def test_xenon_except():
    """ Test that Xenon try-catch works with XenonException """
    make_init()
    with xenon.Xenon() as x:
        try:
            creds = x.credentials()
            cred = creds.newPasswordCredential('ssh', 'wrong-user',
                                               list('wrong-password'), None)
            x.jobs().newScheduler('ssh', 'localhost', cred, None)
            # exception not thrown
            assert_true(False)
        except xenon.exceptions.XenonException:
            # exception thrown
            assert_true(True)
