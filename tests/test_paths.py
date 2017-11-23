import pytest
from xenon import (
    FileSystem, Path, PathAlreadyExistsException,
    PosixFilePermission)


def test_path_separator(xenon_server, tmpdir):
    with FileSystem.create(adaptor='file') as filesystem:
        assert filesystem.get_path_separator() == '/'


def test_path_already_exists_error(local_fs, tmpdir):
    tmpdir = Path(str(tmpdir))
    with pytest.raises(PathAlreadyExistsException):
        local_fs.create_directory(tmpdir / 'test')
        local_fs.create_directory(tmpdir / 'test')


def test_posix_file_permissions(local_fs, tmpdir):
    tmpdir = Path(str(tmpdir))
    filename = tmpdir / 'test.dat'
    local_fs.create_file(filename)
    local_fs.set_posix_file_permissions(filename, [
        PosixFilePermission.OWNER_READ])
