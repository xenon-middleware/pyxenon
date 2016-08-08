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

from . import exceptions
import jpype
import io

Scanner = None
HashMap = None
PrintStream = None

def _init():
    global Scanner, HashMap, PrintStream

    Scanner = jpype.java.util.Scanner
    HashMap = jpype.java.util.HashMap
    PrintStream = jpype.java.io.PrintStream


def read_lines(input_stream):
    """
    Read all lines from a java.io.InputStream, assuming the stream is
    text-based. Internally this routine uses java.util.Scanner to return
    a stream of lines.

    :param input_stream:
        the input stream
    :type input_stream: java.io.InputStream

    :returns:
        generator iterating the lines read from `input_stream`.
    """
    for line in InputStream(input_stream):
        yield line


def dict_to_HashMap(d):
    """
    Converts a Python dictionary to a java.util.HashMap. The HashMap gives
    an implementation of java.util.Map, which is used as a parameter type in
    many calls to Xenon. It is the responsibility of the user to make sure
    that the elements in the dictionary have consistent types.

    :param d:
        the dictionary
    :type d: dict

    :returns:
        a java.util.HashMap
    """
    global HashMap

    if d is None:
        return None

    m = HashMap()
    for k, v in d.items():
        m.put(k, v)
    return m


def Map_to_dict(m):
    """
    Converts a java.util.Map compatible object to a Python dict.

    :param m:
        the map object
    :type m: java.util.Map

    :returns:
        the equivalent dictionary
    :rtype: dict
    """
    return dict((entry.getKey(), entry.getValue()) for entry in m.entrySet())


class InputStream(object):
    """
    Iterator class, returning lines in a stream. The java.io.InputStream is
    composed with a java.util.Scanner object to achieve higher level input
    operations."""
    def __init__(self, java_input_stream):
        global Scanner
        if java_input_stream is None:
            raise ValueError("Stream may not be none")
        self.scan = Scanner(java_input_stream)

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


class OutputStream(io.TextIOBase):
    """
    Output stream object, this should be used as an opened output file::

        print("Hello, World!", file=OutputStream(my_java_stream), flush=True)

    The java.io.OutputStream is composed with a java.io.PrintStream to
    get to the higher level I/O operations in Java.
    """
    def __init__(self, java_output_stream, *args, **kwargs):
        global PrintStream
        super(OutputStream, self).__init__(*args, **kwargs)
        self.stream = PrintStream(java_output_stream)

    def write(self, string):
        """Write a string to stream, using java.io.PrintStream.print"""
        self.stream.print_(jpype.JString(string))
        return len(string)

    def close(self):
        """Closes the underlying java stream."""
        self.stream.close()
        super(OutputStream, self).close()

    def flush(self):
        """Flushes the underlying java stream."""
        self.stream.flush()

    def read(self, *args, **kwargs):
        """Raises IOError"""
        raise IOError()

    def fileno(self):
        """Raises OSError"""
        raise IOError()

    def writable(self):
        """Returns True"""
        return True

    def detach(self):
        """Separate the underlying raw stream from the buffer and return
        it.

        :rtype: None
        """
        raise io.UnsupportedOperation()

    def writelines(self, lines):
        for line in lines:
            self.write(line + '\n')
