import xenon
from queue import Queue
from threading import Thread


xenon.init()


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


with xenon.Scheduler.create(adaptor='local') as scheduler:
    job_description = xenon.JobDescription(
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
        description=job_description, stdin_stream=input_stream())

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

    scheduler.wait_until_done(job)
