import pytest
from xenon import (FileSystem, Path, PathAlreadyExistsException)


def test_path_separator(xenon_server, tmpdir):
    with FileSystem.create(adaptor='file') as filesystem:
        assert filesystem.get_path_separator() == '/'


def test_path_already_exists_error(xenon_server, tmpdir):
    tmpdir = Path(tmpdir)
    with FileSystem.create(adaptor='file') as filesystem:
        with pytest.raises(PathAlreadyExistsException):
            filesystem.create_directory(tmpdir / 'test')
            filesystem.create_directory(tmpdir / 'test')
