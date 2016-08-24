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
import glob
import jpype
from jpype._jclass import _jpype

# we can reference the package already, just not use it yet
JavaBoundMethod = _jpype._JavaBoundMethod
JavaMethod = _jpype._JavaMethod
JavaClass = _jpype._JavaClass
JavaField = _jpype._JavaField


def xenon_lib_dir():
    """ The lib directory that can be used in the code. """
    local_dir = os.path.dirname(os.path.realpath(module_path()))
    return os.path.join(local_dir, 'libs')


def xenon_classpath():
    """ list of classpath entries that xenon needs, using wildcards. """
    lib_dir = xenon_lib_dir()
    return [lib_dir, os.path.join(lib_dir, '*.jar')]


def cast(name_or_class, value):
    """ Cast a Java object to another Java object.

    Parameters
    ----------
    name_or_class : Java class or name of Java class.
    value : Java object
    """
    return jpype.JObject(value, tp=name_or_class)


def java_class(class_name):
    """ Get a class from given class name.

    Parameters
    ----------
    class_name : string like 'java.package.ClassName'

    Raises
    ------
    TypeError : if the class does not exist.
    """
    try:
        package_index = class_name.rindex('.')
    except ValueError:
        raise ValueError(
            'Cannot resolve class \'{0}\' without a package name'
            .format(class_name))
    else:
        cls = getattr(jpype.JPackage(class_name[:package_index]),
                      class_name[package_index + 1:])

        # test whether the classpath contains the class
        # it will raise a TypeError otherwise
        cls.__javaclass__.getName()

        return cls


def init_jvm(classpath=None, log_level=None, log_configuration_file=None,
             *args):
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
    if log_configuration_file is None:
        log_configuration_file = os.path.join(xenon_lib_dir(), 'logback.xml')
    jvm_args.append('-Dlogback.configurationFile={0}'
                    .format(log_configuration_file))

    if log_level is not None:
        log_level = log_level.upper()
        levels = 'ERROR', 'WARN', 'INFO', 'DEBUG', 'TRACE'
        if log_level not in levels:
            raise ValueError('Log level is {0} but it must be one of {1}'
                             .format(log_level, levels))
        jvm_args.append('-Dloglevel={0}'.format(log_level))

    jvm_args += args

    jpype.startJVM(jpype.getDefaultJVMPath(), *jvm_args)

    # test whether the classpath contains Xenon
    # it will raise a TypeError otherwise
    JavaPackage.JPackageClass = jpype.JPackage
    JavaPackage('nl').esciencecenter.xenon.Xenon.__javaclass__.getName()


class JavaPackage(object):
    """ Wrapper around JPackage to avoid segmentation faults. """
    JPackageClass = None

    def __init__(self, name):
        """ mirrors jpype.JPackage.__init__ """
        self.__name = name
        self.__object = None

    def __getattribute__(self, n):
        """
        mirrors jpype.JPackage.__getattribute__, with the addition of
        constructing a new JPackage if it was not already done.
        """
        if n == '_object':
            obj = self.__object
            if obj is None:
                try:
                    obj = JavaPackage.JPackageClass(self.__name)
                    self.__object = obj
                except TypeError:
                    raise EnvironmentError("Xenon is not yet initialized")
            return obj
        elif '__' in n:
            return object.__getattribute__(self, n)
        else:
            return self._object.__getattribute__(n)

    def __setattr__(self, n, v, intern=False):
        """ mirrors jpype.JPackage.__setattr__ """
        if '__' in n:
            object.__setattr__(self, n, v)
        else:
            self.__object.__setattr__(n, v, intern=intern)

    def __str__(self):
        """ copy of jpype.JPackage.__str__ """
        return "<Java package {0}>".format(self.__name)

    def __call__(self, *arg, **kwarg):
        """ copy of jpype.JPackage.__call__ """
        raise TypeError("Package {0} is not Callable".format(self.__name))

nl = JavaPackage('nl')
java = JavaPackage('java')
javax = JavaPackage('javax')
