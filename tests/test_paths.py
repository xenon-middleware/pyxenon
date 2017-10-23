from xenon import (FileSystem, Path, CopyRequest)

def test_path_separator(xenon_server, tmpdir):
    with FileSystem.create(adaptor='file') as filesystem:
        assert filesystem.get_path_separator() == '/'
