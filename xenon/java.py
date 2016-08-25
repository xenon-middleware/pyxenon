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


def init_jvm(classpath=None, log_level=None, log_configuration_file=None,
             *args):
    """ Initialize the Java virtual machine.

    Parameters
    ----------
    classpath : list of strings with classpath entries. This must include Xenon
        dependencies. If None, xenon_classpath() is used as classpath.
    log_level : one of 'ERROR', 'WARN', 'INFO', 'DEBUG', 'TRACE'
    log_configuration_file : logback.xml configuration file path
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

    JavaPackage.JPackageClass = jpype.JPackage
    JavaClass.JClassClass = jpype.JClass

    # test whether the classpath contains Xenon
    # it will raise a TypeError otherwise
    nl.esciencecenter.xenon.Xenon.__javaclass__.getName()


class JavaPackage(object):
    """ Wrapper around jpype.JPackage to avoid segmentation faults. """
    JPackageClass = None

    def __init__(self, name):
        """ mirrors jpype.JPackage.__init__ """
        self.__name = name
        self.__j_package = None

    @property
    def _j_package(self):
        if self.__j_package is None:
            try:
                self.__j_package = JavaPackage.JPackageClass(self.__name)
            except TypeError:
                raise EnvironmentError("Xenon is not yet initialized")
        return self.__j_package

    def __getattr__(self, n, *args, **kwargs):
        """
        mirrors jpype.JPackage.__getattribute__, with the addition of
        constructing a new JPackage if it was not already done.
        """
        if n == '__test__':
            raise AttributeError('Attribute {0} not found'.format(n))
        else:
            return self._j_package.__getattribute__(n, *args, **kwargs)

    def __setattr__(self, n, v, *args, **kwargs):
        """ mirrors jpype.JPackage.__setattr__ """
        if n in ['_JavaPackage__j_package', '_JavaPackage__name']:
            object.__setattr__(self, n, v)
        else:
            self._j_package.__setattr__(n, v, *args, **kwargs)


class JavaClass(object):
    """ Wrapper around jpype.JClass to avoid segmentation faults. """
    JClassClass = None

    def __init__(self, name):
        """ mirrors jpype.JClass(name) """
        self.__name = name
        self.__j_class = None

    def __call__(self, *args, **kwargs):
        """
        mirrors jpype._JavaClass.__new__
        """
        return self._j_class(*args, **kwargs)

    def __getattribute__(self, n):
        """
        mirrors jpype._JavaClass.__getattribute__, with the addition of
        constructing a new JClass if it was not already done.
        """
        if n in ['_JavaClass__j_class', '_JavaClass__name']:
            return object.__getattribute__(self, n)
        elif n == '__test__':
            raise AttributeError('Cannot unit test class {0}'.format(n))

        jcl = self.__j_class
        d = object.__getattribute__(self, '__dict__')
        if jcl is None:
            try:
                jcl = JavaClass.JClassClass(self.__name)
            except TypeError:
                raise EnvironmentError("Xenon is not yet initialized")
            self.__j_class = jcl

            # static Java functions and fields are stored in the dict
            d.update(jcl.__dict__)

        if n == '_j_class':
            return jcl
        elif n == '__dict__':
            return d
        elif n in d:
            return d[n]

        return jcl.__getattribute__(jcl, n)

    def __setattr__(self, n, v, *args, **kwargs):
        """ mirrors jpype.JClass.__setattr__ """
        if n in ['_JavaClass__j_class', '_JavaClass__name']:
            object.__setattr__(self, n, v)
        else:
            self._j_class.__setattr__(n, v, *args, **kwargs)


nl = JavaPackage('nl')
java = JavaPackage('java')
javax = JavaPackage('javax')
