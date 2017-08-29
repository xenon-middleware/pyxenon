import random
import filecmp
from xenon.proto.xenon_pb2 import CopyRequest
from xenon.objects import Path


def test_download_remote(xenon_server, tmpdir):
    xenon = xenon_server
    tmpdir = Path(str(tmpdir))

    test_data = [random.randint(0, 255) for i in range(16)]
    test_file = tmpdir.joinpath('random.txt')
    f = open(str(test_file), 'w')
    for x in test_data:
        print(x, file=f)
    f.close()

    remote_fs = xenon.create_file_system(
            adaptor='sftp',
            location='localhost')

    # use the local file system adaptor to create a file system
    # representation
    local_fs = xenon.create_file_system(
            adaptor='file')

    # define which file to download
    remote_file = tmpdir.joinpath('random.txt')

    # define what file to download to
    local_dir = tmpdir.joinpath('local')
    local_dir.mkdir()
    local_file = local_dir.joinpath(remote_file.name)

    # create the destination file only if the destination path doesn't
    # exist yet
    mode = CopyRequest.CREATE

    # no need to recurse, we're just downloading a file
    recursive = False

    # perform the copy/download and wait 1000 ms for the successful or
    # otherwise completion of the operation
    copy_id = remote_fs.copy(
            remote_file, local_fs, local_file,
            mode=mode, recursive=recursive)
    copy_status = remote_fs.wait_until_done(copy_id, timeout=1000)

    if copy_status.error_message:
        print(copy_status.error_message)
    else:
        print('Done')

    assert filecmp.cmp(str(local_file), str(remote_file))

    # remember to close the FileSystem instances, or use them as
    # context managers
    remote_fs.close()
    local_fs.close()
