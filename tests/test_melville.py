import os
import sys
from pathlib import Path

from threading import Thread
from queue import Queue
from xenon import (JobDescription)


def output_lines(byte_stream, result):
    for b in byte_stream:
        if b.stdout:
            text = b.stdout.decode()
            lines = text.splitlines(keepends=True)
            if lines:
                if result and (result[-1] == '' or result[-1][-1] != '\n'):
                    result[-1] += lines[0]
                    result.extend(lines[1:])
                else:
                    result.extend(lines)

        if b.stderr:
            text = b.stderr.decode()
            for line in text.splitlines():
                print("stderr:", line, file=sys.stderr)


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


def test_moby_dick(local_scheduler, tmpdir):
    tmpdir = Path(str(tmpdir))
    source = Path('./tests/moby-dick.txt')
    file1 = tmpdir / 'moby-dick-1.txt'
    file2 = tmpdir / 'moby-dick-2.txt'

    job_description = JobDescription(
        executable='cat',
        arguments=[],
        queue_name='multi')

    queue, stream = make_input_queue()

    data = source.open().readlines()
    of = file1.open('w')
    for line in data:
        of.write(line)
    of.close()

    job, output_stream = local_scheduler.submit_interactive_job(
        description=job_description,
        stdin_stream=stream())

    result = []
    t = Thread(target=output_lines, args=(output_stream, result), daemon=True)
    t.start()

    for line in data:
        queue.put(line)
    queue.put(EndOfWork)

    local_scheduler.wait_until_done(job)
    t.join()

    of = file2.open('w')
    for line in result:
        of.write(line)
    of.close()

    assert len(data) == len(result)
    assert data == result
