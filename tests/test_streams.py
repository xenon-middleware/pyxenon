import uuid
import os
import random


def read_lines(stream):
    def read_chunks():
        for chunk in stream:
            yield chunk.buffer.decode()

    for chunk in read_chunks():
        yield from chunk.split('\n')


def test_files_reading(xenon_server):
    xenon = xenon_server

    # localfs = xenon.files.newFileSystem(
    #         xenon.NewFileSystemRequest(adaptor='file'))
    remotefs = xenon.files.newFileSystem(
            xenon.NewFileSystemRequest(adaptor='sftp', location='localhost'))

    test_data = [random.randint(0, 255) for i in range(16)]

    test_id = str(uuid.uuid4())
    jobdir = '/tmp/pyxenon-{}'.format(test_id)
    os.mkdir(jobdir)
    f = open(os.path.join(jobdir, 'test-reading.txt'), 'w')
    for x in test_data:
        print(x, file=f)
    f.close()

    data_path = xenon.Path(
            filesystem=remotefs, path=os.path.join(jobdir, 'test-reading.txt'))
    stream = xenon.files.read(data_path)

    out_data = [int(line) for line in read_lines(stream) if line != '']

    assert test_data == out_data
