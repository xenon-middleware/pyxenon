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

from . import files, jobs, exceptions


XenonFactory = None


def init(classpath=[]):
    global XenonFactory
    import jnius_config
    import glob

    cp = []
    for c in classpath:
        cp += glob.glob(c)
    jnius_config.set_classpath(*cp)

    import jnius

    try:
        XenonFactory = jnius.autoclass('nl.esciencecenter.xenon.XenonFactory')
        files._init()
        jobs._init()
        exceptions._init()
    except jnius.JavaException as ex:
        raise ValueError(
            "Classpath not correctly specified: {0}".format(ex.message), ex)

__all__ = ['files', 'jobs', 'exceptions', 'XenonFactory']
