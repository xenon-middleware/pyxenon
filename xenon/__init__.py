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
from .xenon import Xenon
import os
import glob
import inspect

__all__ = ['init', 'files', 'jobs', 'exceptions', 'Xenon']


def init(classpath=None):
    '''
    Initialize the Java Runtime Environment with jnius and set the classpath.

    Parameters
    ----------
    classpath : list of str
        A list of Java classpath locations that may include wildcards.
    '''
    import jnius_config

    if classpath is None:
        localdir = os.path.dirname(os.path.realpath(_module_path(init)))
        classpath = [os.path.join(localdir, '..', 'libs', '*.jar')]
        print(classpath)

    cp = []
    for c in classpath:
        cp += glob.glob(c)
    jnius_config.set_classpath(*cp)

    import jnius

    try:
        files._init()
        jobs._init()
        exceptions._init()
    except jnius.JavaException as ex:
        raise ValueError("Classpath does not correctly specify Xenon and "
                         "its dependencies.", ex)


def _module_path(local_function):
    '''
    Returns the module path without the use of __file__.

    Requires a function defined locally in the module.
    From http://stackoverflow.com/questions/729583
    '''
    return os.path.abspath(inspect.getsourcefile(local_function))
