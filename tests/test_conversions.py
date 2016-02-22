from test_init import make_init
import xenon
from xenon.conversions import (
    OutputStream, InputStream, dict_to_HashMap, Map_to_dict)
import sys
from nose.tools import assert_equals

def test_output_stream():
    make_init()

    from jnius import autoclass, cast
    ByteArrayOutputStream = autoclass('java.io.ByteArrayOutputStream')
    stream = ByteArrayOutputStream()
    out = OutputStream(cast('java.io.OutputStream', stream))
    print("Hello, World!", file=out, flush=True)
    print(stream.toString(), file=sys.stderr)
    assert_equals(stream.toString(), "Hello, World!\n")


def test_input_stream():
    make_init()

    from jnius import autoclass, cast
    ByteArrayInputStream = autoclass('java.io.ByteArrayInputStream')
    stream = ByteArrayInputStream("Infinity, and beyond!\n".encode())
    inp = InputStream(cast('java.io.InputStream', stream))
    lines = list(inp)
    assert_equals(lines, ["Infinity, and beyond!"])


def test_dict_to_HashMap():
    d = {'a': '1', 'b': '2', 'c': '3'}
    to_and_fro = Map_to_dict(dict_to_HashMap(d))
    assert_equals(d, to_and_fro)
