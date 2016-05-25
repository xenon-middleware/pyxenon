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
Conversion Utility functions

This module contains functions to help converting Python objects to their
Java equivalents. We need these to converse with Xenon IO.
"""

from __future__ import print_function
from . import exceptions
import jpype
from jpype import java

PrintStream = None
BufferedReader = None
InputStreamReader = None
Scanner = None
HashMap = None


def _init():
    """ Initialize classes. Only called from xenon.init(). """
    global PrintStream, BufferedReader, InputStreamReader, Scanner, HashMap

    PrintStream = java.io.PrintStream
    BufferedReader = java.io.BufferedReader
    InputStreamReader = java.io.InputStreamReader
    Scanner = java.util.Scanner
    HashMap = java.util.HashMap


def read_lines(input_stream):
    """Read all lines from a java.io.InputStream, assuming the stream is
    text-based. Internally this routine uses java.util.Scanner to return
    a stream of lines.

    :param input_stream:
        the input stream
    :type input_stream: java.io.InputStream

    :returns:
        generator iterating the lines read from `input_stream`.
    """
    reader = Scanner(input_stream)

    while True:
        yield reader.nextLine()


def dict_to_HashMap(d):
    """Converts a Python dictionary to a java.util.HashMap. The HashMap gives
    an implementation of java.util.Map, which is used as a parameter type in
    many calls to Xenon. It is the responsibility of the user to make sure
    that the elements in the dictionary have consistent types.

    :param d:
        the dictionary
    :type d: dict

    :returns:
        a java.util.HashMap
    """
    if d is None:
        return None

    m = HashMap()
    for k, v in d.items():
        m.put(k, v)
    return m


class JavaIterator(object):
    """Wraps a Java iterator."""
    def __init__(self, iter):
        self.iter = iter

    def __iter__(self):
        return self

    def next(self):
        return self.__next__()

    def __next__(self):
        if self.iter.hasNext():
            return self.iter.next()
        else:
            raise StopIteration()


def Map_to_dict(m):
    """Converts a java.util.Map compatible object to a Python dict.

    :param m:
        the map object
    :type m: java.util.Map

    :returns:
        the equivalent dictionary
    :rtype: dict
    """
    d = {}
    for k in JavaIterator(m.keySet().iterator()):
        d[k] = m.get(k)
    return d


class InputStream(object):
    """Iterator class, returning lines in a stream. The java.io.InputStream is
    composed with a java.util.Scanner object to achieve higher level input
    operations."""
    def __init__(self, java_input_stream):
        self.jis = java_input_stream
        self.scan = Scanner(self.jis)

    def __iter__(self):
        return self

    def next(self):
        return self.__next__()

    def __next__(self):
        try:
            line = self.scan.nextLine()
        except exceptions.XenonException:
            raise StopIteration()
        return line


class OutputStream(object):
    """Output stream object, this should be used as an opened output file::

        print("Hello, World!", file=OutputStream(my_java_stream), flush=True)

    The java.io.OutputStream is composed with a java.io.PrintStream to
    get to the higher level I/O operations in Java.
    """
    def __init__(self, java_output_stream):
        self.jos = java_output_stream
        self.stream = PrintStream(self.jos)
        self.closed = False

    def write(self, str):
        """Write a string to stream, using java.io.PrintStream.print"""
        self.stream.print_(jpype.JString(str))

    def close(self):
        """Closes the underlying java stream."""
        self.stream.close()
        self.closed = True

    def flush(self):
        """Flushes the underlying java stream."""
        self.stream.flush()

    def fileno(self):
        """Raises OSError"""
        raise OSError()

    def readable(self):
        """Returns False"""
        return False

    def seekable(self):
        """Returns False"""
        return False

    def writable(self):
        """Returns True"""
        return True
