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
Python bindings of the Xenon Java API.

Xenon is a middleware library to schedule jobs and manipulate files on local
and remote machines. This binding is a thin wrapper around the Java API, so
except initialization, all functions from the Java API can directly be called.

As for initialization, run xenon.init() before anything else, then use
xenon.Xenon() or 'with xenon.Xenon() as x' to start using the Xenon API. Find
the function parameters through the documentation on
https://nlesc.github.io/Xenon.
"""

from . import files, jobs, exceptions, conversions
from .xenon import Xenon
from .java import (init_jvm, java_class, cast, nl, JavaBoundMethod, JavaClass,
                   JavaMethod, JavaField, xenon_lib_dir, xenon_classpath)
from jpype import java, javax
from .util import module_path

__all__ = [
    'cast',
    'conversions',
    'exceptions',
    'files',
    'init',
    'java',
    'java_class',
    'JavaBoundMethod',
    'JavaClass',
    'JavaMethod',
    'JavaField',
    'javax',
    'jobs',
    'module_path',
    'nl',
    'Xenon',
    'xenon_classpath',
    'xenon_lib_dir',
]
_is_initialized = False


def init(classpath=None, log_level=None):
    """
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
    """
    global _is_initialized
    if _is_initialized:
        raise ValueError("xenon.init can be called only once")

    try:
        init_jvm(classpath, log_level)
    except TypeError:
        raise ValueError("Classpath does not correctly specify Xenon and "
                         "its dependencies. This exception is fatal: calling "
                         "init again will not resolve this error.")

    # import after setting the classpath or Xenon will not be found
    _is_initialized = True

    files._init()
    jobs._init()
    exceptions._init()
    conversions._init()
