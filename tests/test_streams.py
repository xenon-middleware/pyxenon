import uuid
import os
import random


def read_lines(stream):
    def read_chunks():
        for chunk in stream:
            yield chunk.buffer.decode()

    for chunk in read_chunks():
        yield from chunk.split('\n')


def test_files_reading(xenon_server, tmpdir):
    xenon = xenon_server

    remotefs = xenon.files.newFileSystem(adaptor='sftp', location='localhost')

    test_data = [random.randint(0, 255) for i in range(16)]

    test_file = str(tmpdir.join('test-reading.txt'))

    f = open(test_file, 'w')
    for x in test_data:
        print(x, file=f)
    f.close()

    data_path = xenon.Path(filesystem=remotefs, path=test_file)
    stream = xenon.files.read(data_path)

    out_data = [int(line) for line in read_lines(stream) if line != '']

    assert test_data == out_data


def test_files_writing(xenon_server, tmpdir):
    xenon = xenon_server

    remotefs = xenon.files.newFileSystem(adaptor='sftp', location='localhost')

    test_data = [random.randint(0, 255) for i in range(16)]

    test_file = str(tmpdir.join('test-writing.txt'))
    file_path = xenon.Path(filesystem=remotefs, path=test_file)

    xenon.files.createFile(file_path)
    request = iter(
        xenon.WriteRequest(
            path=file_path,
            buffer="{}\n".format(x).encode(),
            options=[xenon.WriteRequest.OPEN, xenon.WriteRequest.APPEND])
        for x in test_data)
    xenon.files.write(request)

    out_data = [int(line.strip()) for line in open(test_file) if line != '']

    assert test_data == out_data
