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
from .util import module_path
from past.builtins import basestring
import glob
import jpype
from jpype._jclass import _jpype

# we can reference the package already, just not use it yet
nl = jpype.JPackage('nl')
JavaBoundMethod = _jpype._JavaBoundMethod
JavaMethod = _jpype._JavaMethod
JavaClass = _jpype._JavaClass
JavaField = _jpype._JavaField


def xenon_classpath():
    """ list of classpath entries that xenon needs, using wildcards. """
    local_dir = os.path.dirname(os.path.realpath(module_path()))
    lib_dir = os.path.join(local_dir, '..', 'libs')
    return [lib_dir, os.path.join(lib_dir, '*.jar')]


def cast(name_or_class, value):
    """ Cast a Java object to another Java object.

    Parameters
    ----------
    name_or_class : Java class or name of Java class.
    value : Java object
    """
    if isinstance(name_or_class, basestring):
        tp = java_class(name_or_class)
    else:
        tp = name_or_class

    return jpype.JObject(value, tp=tp)


def java_class(class_name):
    try:
        package_index = class_name.rindex('.')
    except ValueError:
        raise ValueError(
            'Cannot resolve class \'{0}\' without a package name'
            .format(class_name))
    else:
        return getattr(jpype.JPackage(class_name[:package_index]),
                       class_name[package_index + 1:])


def init_jvm(classpath=None, log_level=None, *args):
    """ Initialize the Java virtual machine.

    Parameters
    ----------
    classpath : list of strings with classpath entries. This must include Xenon
        dependencies. If None, xenon_classpath() is used as classpath.
    log_level : one of 'ERROR', 'WARN', 'INFO', 'DEBUG', 'TRACE'
    args :
    """
    if classpath is None:
        classpath = xenon_classpath()

    jvm_args = ['-ea']

    cp = [filename for elem in classpath for filename in glob.glob(elem)]

    jvm_args.append('-Djava.class.path={0}'.format(os.path.pathsep.join(cp)))

    if log_level is not None:
        log_level = log_level.upper()
        levels = 'ERROR', 'WARN', 'INFO', 'DEBUG', 'TRACE'
        if log_level not in levels:
            raise ValueError('Log level is {0} but it must be one of {1}'
                             .format(log_level, levels))
        jvm_args.append('-Dloglevel={0}'.format(log_level))

    jvm_args += args

    jpype.startJVM(jpype.getDefaultJVMPath(), *jvm_args)
