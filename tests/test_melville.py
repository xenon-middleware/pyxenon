import sys
from pathlib import Path
import pytest

from threading import Thread
from queue import Queue
from xenon import (JobDescription)


def coroutine(f):
    def g(*args, **kwargs):
        sink = f(*args, **kwargs)
        next(sink)
        return sink

    return g


@coroutine
def bytes_to_lines(sink):
    buf = b''

    while True:
        chunk = yield
        lines = chunk.splitlines(keepends=True)

        if len(lines) == 0:
            continue

        if len(lines) == 1 and lines[0][-1] != 10:
            buf += lines[0]
            continue

        sink.send((buf + lines[0]).decode())

        if len(lines) == 1:
            buf = b''
            continue

        for line in lines[1:-1]:
            sink.send(line.decode())

        if lines[-1][-1] != 10:
            buf = lines[-1]
        else:
            buf = b''
            sink.send(lines[-1].decode())


def redirect_output(byte_stream, stdout_sink, stderr_sink):
    for b in byte_stream:
        if b.stdout:
            stdout_sink.send(b.stdout)
        if b.stderr:
            stderr_sink.send(b.stderr)


@coroutine
def list_sink(result):
    while True:
        line = yield
        result.append(line)


class EndOfWork(object):
    pass


def make_input_queue():
    queue = Queue()

    def stream():
        while True:
            msg = queue.get()
            if msg is EndOfWork:
                queue.task_done()
                return
            else:
                yield msg.encode()
                queue.task_done()

    return queue, stream


@pytest.mark.skip(True, "Test takes very long")
def test_moby_dick_cat(local_scheduler, tmpdir):
    tmpdir = Path(str(tmpdir))
    source = Path('./tests/moby-dick.txt')

    job_description = JobDescription(
        executable='cat',
        arguments=[],
        queue_name='multi')

    data = source.open().readlines()
    job, output_stream = local_scheduler.submit_interactive_job(
        description=job_description,
        stdin_stream=(d.encode() for d in data))

    result = []
    accumulator = list_sink(result)

    @coroutine
    def echo_stderr():
        while True:
            line = yield
            print("err:", line)

    redirect_output(
        output_stream,
        stdout_sink=bytes_to_lines(accumulator),
        stderr_sink=bytes_to_lines(echo_stderr()))

    local_scheduler.wait_until_done(job)

    assert len(data) == len(result)
    assert data == result


def sink_map(f):
    @coroutine
    def g(sink):
        while True:
            x = yield
            sink.send(f(x))

    return g


def test_moby_dick_spliced(local_scheduler, tmpdir):
    tmpdir = Path(str(tmpdir))
    source = Path('./tests/moby-dick.txt')
    file2 = tmpdir / 'moby-dick-2.txt'

    job_description = JobDescription(
        executable=str(Path(sys.prefix) / 'bin' / 'python'),
        arguments=['./tests/splice-to-stderr.py'],
        queue_name='multi')

    data = source.open().readlines()
    queue, stream = make_input_queue()

    expected_word_count = [(i+1, len(line.split(' '))) for i, line in enumerate(data)]

    job, output_stream = local_scheduler.submit_interactive_job(
        description=job_description,
        stdin_stream=stream())

    numbered_lines = []
    accumulator = list_sink(numbered_lines)
    word_count = []
    wc_accumulator = list_sink(word_count)

    @sink_map
    def parse_ints(line):
        return tuple(int(x) for x in line.split(' '))

    t = Thread(
        target=redirect_output,
        args=(
            output_stream,
            bytes_to_lines(accumulator),
            bytes_to_lines(parse_ints(wc_accumulator))),
        daemon=True)
    t.start()

    for line in data:
        queue.put(line)
    queue.put(EndOfWork)

    local_scheduler.wait_until_done(job)
    t.join()

    result = [line[13:] for line in sorted(numbered_lines)]
    of = file2.open('w')
    for line in result:
        of.write(line)
    of.close()

    assert len(data) == len(result)
    assert data == result

    assert len(expected_word_count) == len(word_count)
    assert expected_word_count == word_count
