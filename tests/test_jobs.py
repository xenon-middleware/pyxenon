import os
from threading import Thread
from queue import Queue


def test_echo_job(xenon_server, tmpdir):
    xenon = xenon_server

    scheduler = xenon.jobs.newScheduler(adaptor='local')

    file_name = str(tmpdir.join('hello.txt'))
    job_description = xenon.JobDescription(
        executable='/bin/bash',
        arguments=['-c', 'echo "Hello, World!"'],
        stdOut=file_name)

    job = xenon.jobs.submitJob(
        scheduler=scheduler, description=job_description)
    job_status = xenon.jobs.waitUntilDone(job)
    if job_status.exitCode != 0:
        raise Exception(job_status.errorMessage)
    xenon.jobs.deleteJob(job)
    xenon.jobs.close(scheduler)

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


def test_online_job(xenon_server):
    xenon = xenon_server
    scheduler = xenon.jobs.newScheduler(adaptor='local')

    job_description = xenon.JobDescription(
        executable='cat',
        arguments=[],
        queueName='multi',
        interactive=True)

    job = xenon.jobs.submitJob(
        scheduler=scheduler, description=job_description)
    xenon.jobs.waitUntilRunning(job)

    input_queue = Queue()

    def input_stream():
        while True:
            cmd, msg = input_queue.get()
            if cmd == 'end':
                input_queue.task_done()
                return
            else:
                yield xenon.JobInputStream(job=job, stdin=msg.encode())
                input_queue.task_done()

    output_stream = xenon.jobs.getStreams(input_stream())

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

    xenon.jobs.waitUntilDone(job)
    xenon.jobs.deleteJob(job)
    xenon.jobs.close(scheduler)
