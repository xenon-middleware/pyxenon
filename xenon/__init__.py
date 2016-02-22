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

'''
Python bindings of the Xenon Java API.

Xenon is a middleware library to schedule jobs and manipulate files on local
and remote machines. This binding is a thin wrapper around the Java API, so
except initialization, all functions from the Java API can directly be called.

As for initialization, run xenon.init() before anything else, then use
xenon.Xenon() or 'with xenon.Xenon() as x' to start using the Xenon API. Find
the function parameters through the documentation on
https://nlesc.github.io/Xenon.
'''

from . import files, jobs, exceptions, conversions
from .xenon import Xenon
import os
import glob
import inspect

__all__ = ['init', 'files', 'jobs', 'exceptions', 'conversions', 'Xenon']
_is_initialized = False


def init(classpath=None, log_level=None):
    '''
    Initialize the Java Runtime Environment with jnius and set the classpath.

    Parameters
    ----------
    classpath : list of str
        A list of Java classpath locations that may include wildcards.
    log_level: one of [ERROR, WARN, INFO, DEBUG, TRACE] (default: WARN)
        Logback log level for Java code, case insensitive

    Raises
    ------
    ValueError: if Xenon cannot be found on the classpath. This error is not
        recoverable: it requires python to restart before calling this function
        again.
    ValueError: if the function is called more than once.
    ValueError: if the provided log level is not recognized.
    '''
    global _is_initialized
    if _is_initialized:
        raise ValueError("xenon.init can be called only once")

    import jnius_config

    if classpath is None:
        localdir = os.path.dirname(os.path.realpath(_module_path(init)))
        libdir = os.path.join(localdir, '..', 'libs')
        classpath = [libdir, os.path.join(libdir, '*.jar')]

    cp = []
    for c in classpath:
        cp += glob.glob(c)
    jnius_config.set_classpath(*cp)

    if log_level is not None:
        log_level = log_level.upper()
        levels = ['ERROR', 'WARN', 'INFO', 'DEBUG', 'TRACE']
        if log_level not in levels:
            raise ValueError('Log level is {0} but it must be one of {1}'
                             .format(log_level, levels))
        jnius_config.add_options('-Dloglevel={0}'.format(log_level))

    # import jnius after setting the classpath or Xenon will not be found
    import jnius
    _is_initialized = True

    try:
        files._init()
        jobs._init()
        exceptions._init()
        conversions._init()

    except jnius.JavaException as ex:
        raise ValueError("Classpath does not correctly specify Xenon and "
                         "its dependencies. This exception is fatal: calling "
                         "init again will not resolve this error.", ex)


def _module_path(local_function):
    '''
    Returns the module path without the use of __file__.

    Requires a function defined locally in the module.
    From http://stackoverflow.com/questions/729583
    '''
    return os.path.abspath(inspect.getsourcefile(local_function))
