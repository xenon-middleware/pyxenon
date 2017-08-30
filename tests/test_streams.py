import random
from xenon import (FileSystem, Path)


def read_lines(stream):
    def read_chunks():
        for chunk in stream:
            yield chunk.buffer.decode()

    for chunk in read_chunks():
        yield from chunk.split('\n')


def test_files_reading_oop(xenon_server, tmpdir):
    with FileSystem.create(
            adaptor='sftp', location='localhost') as remotefs:
        test_data = [random.randint(0, 255) for i in range(16)]

        test_file = str(tmpdir.join('test-reading.txt'))

        f = open(test_file, 'w')
        for x in test_data:
            print(x, file=f)
        f.close()

        stream = remotefs.read_from_file(Path(test_file))

        out_data = [int(line) for line in read_lines(stream) if line != '']

        assert test_data == out_data


def test_files_writing_oop(xenon_server, tmpdir):
    with FileSystem.create(
            adaptor='sftp', location='localhost') as remotefs:
        test_data = [random.randint(0, 255) for i in range(16)]

        test_file = str(tmpdir.join('test-writing.txt'))
        remotefs.create_file(Path(test_file))

        data_stream = iter("{}\n".format(x).encode() for x in test_data)
        remotefs.append_to_file(Path(test_file), data_stream)

        out_data = [int(line.strip())
                    for line in open(test_file) if line != '']
        assert test_data == out_data
