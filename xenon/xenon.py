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
Primary Xenon API

To instantiate and use the Java Xenon API with. The `package` variable stores
the Java package name of the Xenon jobs API.
"""

from .java import JavaClass

package = 'nl.esciencecenter.xenon'
XenonFactory = JavaClass(package + '.XenonFactory')


class Xenon(object):
    """
    Xenon class, reflecting the Java Xenon class.

    With this object, the need for XenonFactory is obviated.
    It can be used in the Python with-resources construct.
    """
    def __init__(self, options=None):
        """
        Create a Xenon class using the XenonFactory

        Parameters
        ----------
        options : dict or None
            options to Xenon, takes Xenon properties as keys
        """
        global XenonFactory
        self.xenon = XenonFactory.newXenon(options)

    def __getattr__(self, name, *args, **kwargs):
        """ Call Xenon functions, defined in the Java Xenon API """
        if name == 'xenon':
            return None

        if self.xenon is None:
            raise ValueError("Xenon is already closed")

        return getattr(self.xenon, name, *args, **kwargs)

    def close(self):
        """
        Close and remove Xenon.
        """
        global XenonFactory
        if self.xenon is None:
            raise ValueError("Xenon is already closed")

        XenonFactory.endXenon(self.xenon)
        del self.xenon

    def __del__(self):
        """
        Close xenon after deletion if close was not called.

        Java Xenon might not quit by itself, so we have to explicitly do this.
        """
        if self.xenon is not None:
            self.close()

    def __enter__(self):
        """ Enter with-resources, Xenon __init__ already did everything """
        return self

    def __exit__(self, type, value, traceback):
        """ Exit with-resources, close and remove Xenon """
        self.close()
