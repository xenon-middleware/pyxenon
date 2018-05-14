import pytest
from xenon import Path
from xenon.exceptions import NoSuchPathException


def test_file_does_not_exist(local_filesystem, tmpdir):
    tmpdir = Path(str(tmpdir))
    with pytest.raises(NoSuchPathException):
        filename = tmpdir / 'this-file-does-not-exist'
        result = bytearray()
        for chunk in local_filesystem.read_from_file(filename):
            result.extend(chunk)
