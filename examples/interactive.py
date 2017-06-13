from xenon import (Server as Xenon)
from queue import Queue
from threading import Thread


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


with Xenon() as xenon:
    scheduler = xenon.jobs.newScheduler(
        xenon.NewSchedulerRequest(adaptor='local'))

    job_description = xenon.JobDescription(
        executable='tee',
        arguments=['test.txt'],
        interactive=True)

    job = xenon.jobs.submitJob(xenon.SubmitJobRequest(
        scheduler=scheduler, description=job_description))
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

    lines = [
        "Mystic noble gas,",
        "Heavy yet fleeting from grasp,",
        "Blue like burning ice."
    ]

    try:
        for line in lines:
            input_queue.put(('msg', line + '\n'))
            msg = timeout(1.0, lambda: output_stream.next().stdout.strip())
            assert msg == line
    finally:
        input_queue.put(('end', None))
        input_queue.join()

    xenon.jobs.waitUntilDone(job)
    xenon.jobs.deleteJob(job)
    xenon.jobs.close(scheduler)
