import pytest
from xenon import (
    Path, PathAlreadyExistsException,
    PosixFilePermission)


def test_path_separator(local_filesystem):
    assert local_filesystem.get_path_separator() == '/'


def test_path_already_exists_error(local_filesystem, tmpdir):
    tmpdir = Path(str(tmpdir))
    with pytest.raises(PathAlreadyExistsException):
        local_filesystem.create_directory(tmpdir / 'test')
        local_filesystem.create_directory(tmpdir / 'test')


def test_posix_file_permissions(local_filesystem, tmpdir):
    tmpdir = Path(str(tmpdir))
    filename = tmpdir / 'test.dat'
    local_filesystem.create_file(filename)
    local_filesystem.set_posix_file_permissions(filename, [
        PosixFilePermission.OWNER_READ])
