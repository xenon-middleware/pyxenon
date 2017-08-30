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

from __future__ import print_function

from xenon.conversions import (
    OutputStream, InputStream, dict_to_HashMap, Map_to_dict)
import sys
from xenon import cast, java


def test_output_stream():
    stream = java.io.ByteArrayOutputStream()
    out = OutputStream(cast(java.io.OutputStream, stream))
    print("Hello, World!", file=out)
    out.flush()
    print(stream.toString(), file=sys.stderr)
    assert stream.toString() == "Hello, World!\n"


def test_input_stream():
    stream = java.io.ByteArrayInputStream("Infinity, and beyond!\n".encode())
    inp = InputStream(cast(java.io.InputStream, stream))
    lines = list(inp)
    assert lines == ["Infinity, and beyond!"]


def test_dict_to_HashMap():
    d = {'a': '1', 'b': '2', 'c': '3'}
    to_and_fro = Map_to_dict(dict_to_HashMap(d))
    assert d == to_and_fro
