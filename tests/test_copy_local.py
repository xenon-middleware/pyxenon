from xenon import (FileSystem, Path, CopyRequest)

import os


def test_copy_local_absolute(xenon_server, tmpdir):
    xenon = xenon_server

    # use the local file system adaptor to create a file system
    # representation
    with FileSystem.create(xenon, adaptor='file') as filesystem:
        # create Paths for the source and destination files, using absolute
        # paths
        dest_file_name = str(tmpdir.join('thefile.bak'))
        source_file_name = str(tmpdir.join('thefile.txt'))

        with open(source_file_name, 'w') as f:
            print("Hello, World!", file=f)
        assert os.path.exists(source_file_name)

        source_path = Path(source_file_name)
        dest_path = Path(dest_file_name)

        # create the destination file only if the destination path doesn't
        # exist yet; perform the copy and wait 1000 ms for the successful or
        # otherwise completion of the operation
        copy_id = filesystem.copy(
            source_path, filesystem, dest_path,
            mode=CopyRequest.CREATE, recursive=False)
        timeout_milli_secs = 1000
        copy_status = filesystem.wait_until_done(copy_id, timeout_milli_secs)

        print("State: ", copy_status.state)
        if not copy_status.done:
            raise RuntimeError(copy_status.error)
        else:
            assert os.path.exists(dest_file_name)


def test_copy_local_relative(xenon_server, tmpdir):
    with open(str(tmpdir.join('thefile.txt')), 'w') as f:
        print("Hello, World!", file=f)

    xenon = xenon_server

    # use the local file system adaptor to create a file system
    # representation
    filesystem = FileSystem.create(xenon, adaptor='file')
    filesystem.set_working_directory(Path(str(tmpdir)))

    # create Paths for the source and destination files, using absolute
    # paths
    working_directory = filesystem.get_working_directory()
    dest_file = working_directory.joinpath('thefile.bak')
    source_file = working_directory.joinpath('thefile.txt')

    # create the destination file only if the destination path doesn't
    # exist yet; perform the copy and wait 1000 ms for the successful or
    # otherwise completion of the operation
    copy_id = filesystem.copy(
        source_file, filesystem, dest_file,
        mode=CopyRequest.CREATE, recursive=False)
    timeout_milli_secs = 1000
    copy_status = filesystem.wait_until_done(copy_id, timeout_milli_secs)

    print("State: ", copy_status.state)
    if not copy_status.done:
        raise RuntimeError(copy_status.error)
    else:
        dest_file_name = str(tmpdir.join('thefile.bak'))
        assert os.path.exists(dest_file_name)

    filesystem.close()
