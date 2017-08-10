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
    scheduler = xenon.schedulers.create(adaptor='local')

    job_description = xenon.JobDescription(
        executable='cat',
        arguments=[],
        queueName='multi')

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

    output_stream = xenon.schedulers.submit_interactive_job(
        scheduler=scheduler, description=job_description, stdin_stream=input_stream())

    first_response = timeout(1.0, lambda: output_stream.next())
    # first_response = output_stream.next()
    job = first_response.job

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
            print(msg)
    finally:
        input_queue.put(('end', None))
        input_queue.join()

    xenon.schedulers.waitUntilDone(job)
    xenon.schedulers.close(scheduler)
