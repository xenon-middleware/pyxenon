import xenon
from queue import Queue
from timeout import timeout


def make_input_stream():
    """Creates a :py:class:`Queue` object and a co-routine yielding from that
    queue. The queue should be populated with 2-tuples of the form `(command,
    message)`, where `command` is one of [`msg`, `end`].

    When the `end` command is recieved, the co-routine returns, ending the
    stream.

    When a `msg` command is received, the accompanying message is encoded and
    yielded as a ``bytes`` object.

    :return: tuple of (queue, stream)"""
    input_queue = Queue()

    def input_stream():
        while True:
            cmd, msg = input_queue.get()
            if cmd == 'end':
                input_queue.task_done()
                return
            elif cmd == 'msg':
                yield msg.encode()
                input_queue.task_done()

    return input_queue, input_stream


def get_line(s):
    """The :py:meth:`submit_interactive_job()` method returns a stream of
    objects that contain a ``stdout`` and ``stderr`` field, containing a
    ``bytes`` object.  Here we're only reading from ``stdout``."""
    return s.next().stdout.decode().strip()


# our input lines
input_lines = [
    "Zlfgvp aboyr tnf,",
    "Urnil lrg syrrgvat sebz tenfc,",
    "Oyhr yvxr oheavat vpr."
]

# the job description, make sure you run the script from the examples
# directory!
job_description = xenon.JobDescription(
    executable='python',
    arguments=['rot13.py'],
    queue_name='multi')

# start the xenon-grpc server
xenon.init()

# on the local adaptor
with xenon.Scheduler.create(adaptor='local') as scheduler:
    input_queue, input_stream = make_input_stream()

    # submit an interactive job, this gets us the job-id and a stream yielding
    # job output from stdout and stderr.
    job, output_stream = scheduler.submit_interactive_job(
        description=job_description, stdin_stream=input_stream())

    # next we feed the input_queue with messages
    try:
        for line in input_lines:
            print(" [sending]   " + line)
            input_queue.put(('msg', line + '\n'))
            msg = timeout(1.0, get_line, output_stream)
            print("[received]   " + msg)

    # make sure to close our end whatever may happen
    finally:
        input_queue.put(('end', None))
        input_queue.join()

    scheduler.wait_until_done(job)
