import os
from threading import Thread
from queue import Queue

from xenon import (Scheduler, JobDescription)


def test_echo_job_oop(xenon_server, tmpdir):
    xenon = xenon_server
    with Scheduler.create(xenon, adaptor='local') as scheduler:
        file_name = str(tmpdir.join('hello.txt'))
        job_description = JobDescription(
            executable='/bin/bash',
            arguments=['-c', 'echo "Hello, World!"'],
            stdout=file_name)
        job = scheduler.submit_batch_job(job_description)
        job_status = scheduler.wait_until_done(job)

        if job_status.exit_code != 0:
            raise Exception(job_status.errorMessage)

    assert os.path.isfile(file_name)
    lines = [l.strip() for l in open(file_name)]
    assert lines[0] == 'Hello, World!'


def timeout(delay, call, *args, **kwargs):
    return_value = None

    def target():
        nonlocal return_value
        return_value = call(*args, **kwargs)

    t = Thread(target=target)
    t.start()
    t.join(delay)
    if t.is_alive():
        raise RuntimeError("Operation did not complete within time.")

    return return_value


def test_online_job_oop(xenon_server):
    xenon = xenon_server
    with Scheduler.create(xenon, adaptor='local') as scheduler:
        job_description = JobDescription(
            executable='cat',
            arguments=[],
            queue_name='multi')

        input_queue = Queue()

        def input_stream():
            while True:
                cmd, msg = input_queue.get()
                if cmd == 'end':
                    input_queue.task_done()
                    return
                else:
                    yield msg.encode()
                    input_queue.task_done()

        job, output_stream = scheduler.submit_interactive_job(
            description=job_description,
            stdin_stream=input_stream())

        def get_line(s):
            return s.next().stdout.decode().strip()

        lines = [
            "Mystic noble gas,",
            "Heavy yet fleeting from grasp,",
            "Blue like burning ice."
        ]

        try:
            for line in lines:
                input_queue.put(('msg', line + '\n'))
                msg = timeout(1.0, get_line, output_stream)
                assert msg == line
        finally:
            input_queue.put(('end', None))
            input_queue.join()

        scheduler.wait_until_done(job)
