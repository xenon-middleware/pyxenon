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

_JClass = None
_JPackage = None


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
    global _JClass, _JPackage
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

    _JPackage = jpype.JPackage
    _JClass = jpype.JClass

    # test whether the classpath contains Xenon
    # it will raise a TypeError otherwise
    nl.esciencecenter.xenon.Xenon.__javaclass__.getName()


class JavaPackage(object):
    """
    Wrapper around jpype.JPackage to avoid segmentation faults.

    Instead it will raise EnvironmentError if xenon.init has not yet been
    called.
    """
    def __init__(self, name):
        """ wraps jpype.JPackage.__init__ """
        self.__name = name
        self.__j_package = None

    @property
    def _j_package(self):
        """
        Actual package class
        @raise EnvironmentError: if xenon.init has not yet been called.
        """
        if self.__j_package is None:
            global _JPackage
            if _JPackage is None:
                raise EnvironmentError("Xenon is not yet initialized")
            self.__j_package = _JPackage(self.__name)

        return self.__j_package

    def __getattr__(self, n, *args, **kwargs):
        """
        wraps jpype.JPackage.__getattribute__, with the addition of
        constructing a new JPackage if it was not already done.
        """
        if n == '__test__':  # avoid pytest inspection
            raise AttributeError('Attribute {0} not found'.format(n))
        else:
            return self._j_package.__getattribute__(n, *args, **kwargs)

    def __setattr__(self, n, v, *args, **kwargs):
        """ wraps jpype.JPackage.__setattr__ """
        if n in ['_JavaPackage__j_package', '_JavaPackage__name']:
            object.__setattr__(self, n, v)
        else:
            self._j_package.__setattr__(n, v, *args, **kwargs)


class JavaClass(object):
    """ Wrapper around jpype.JClass to avoid segmentation faults. """
    def __init__(self, name):
        """ wraps jpype.JClass(name) """
        self.__name = name
        self.__j_class = None

    def __call__(self, *args, **kwargs):
        """
        wraps jpype._JavaClass.__new__
        """
        return self._j_class(*args, **kwargs)

    def __getattribute__(self, n):
        """
        wraps jpype._JavaClass.__getattribute__, with the addition of
        constructing a new JClass if it was not already done.
        """
        # Unlike __getattr__, this method processes ALL attribute invocations,
        # including ones that are set internally. Handle those separately.
        # On object attributes that we want to access, call
        # object.__getattribute__, this is the superclass implementation that
        # DOES look up the actual attributes.
        if n in ['_JavaClass__j_class', '_JavaClass__name']:
            return object.__getattribute__(self, n)
        elif n == '__test__':  # avoid pytest inspection
            raise AttributeError('Cannot unit test class {0}'.format(n))

        jcl = self.__j_class
        # fields and some members are part of dict. We include our own dict
        # and when the java class is initialized, we include the fields and
        # members of that class as well
        d = object.__getattribute__(self, '__dict__')
        if jcl is None:
            global _JClass
            if _JClass is None:
                raise EnvironmentError("Xenon is not yet initialized")

            jcl = _JClass(self.__name)
            self.__j_class = jcl

            # static Java functions and fields are stored in the dict
            d.update(jcl.__dict__)

        # handle attributes _j_class, __dict__ and __dict__ members before
        # calling wrapped class.
        if n == '_j_class':
            return jcl
        elif n == '__dict__':
            return d
        elif n in d:
            return d[n]

        return jcl.__getattribute__(jcl, n)

    def __setattr__(self, n, v, *args, **kwargs):
        """ wraps jpype._JavaClass.__setattr__ """
        if n in ['_JavaClass__j_class', '_JavaClass__name']:
            object.__setattr__(self, n, v)
        else:
            self._j_class.__setattr__(n, v, *args, **kwargs)


nl = JavaPackage('nl')
java = JavaPackage('java')
javax = JavaPackage('javax')
