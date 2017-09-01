Advanced: Streaming & Interactive jobs
======================================

In several cases it is desireable to stream data from/to interactive jobs as
well as data to a remote filesystem. The GRPC API has build-in support for
asynchronous streaming through many simultaneous requests. In Python this API is
exposed in terms of generators.

Example: an online job
----------------------

In this example we'll show how to obtain
bi-directional communication with an online job. An online job is started with
:py:meth:`Scheduler.submit_online_job()`.

Streaming input, a.k.a. The Halting Problem
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We need to stream input to the online job. In the :doc:`quick-start`, we saw
that we could send data to a stream by simply giving a list of bytes objects.
Here we aim a bit more advanced to play a kind of real-time ping-pong with a
remote process. We need to provide `PyXenon` with an generator that pulls its
messages from a queue. The GRPC module ensures that this generator is being run
asynchonously from the main thread.

The tricky part is that we need to be able to tell the generator when the work
is done and no more input is to be expected. We could have it recieve strings and
make it check for end-of-file messages in some way, but in essence we'll always
have to define a little protocol to deal with the finiteness of the generator's
life. To make this explicit we define a little 2-tuple micro-language:

+-------------------------------+--------------------------+
| message                       | action                   |
+===============================+==========================+
| ``('msg', <value: string>)``  | ``yield value.encode()`` |
+-------------------------------+--------------------------+
| ``('end', None)``             | ``return``               |
+-------------------------------+--------------------------+

Implementing this:

.. code-block:: python

    from queue import Queue

    def make_input_stream():
        input_queue = Queue()

        def input_stream():
            while True:
                cmd, value = input_queue.get()
                if cmd == 'end':
                    input_queue.task_done()
                    return
                elif cmd == 'msg':
                    yield value.encode()
                    input_queue.task_done()

        return input_queue, input_stream

Reading output
~~~~~~~~~~~~~~
The return-value of :py:meth:`submit_online_job()` is an iterator yielding
objects of type `SubmitOnlineJobResponse`. These objects have a ``stdout``
field containing (binary) data that the job wrote to standard output, as well
as a ``stderr`` field containing data written to standard error. For any message
either field may be empty or not. In this example we're only interested in data
from ``stdout``:

.. code-block:: python

    def get_stdout(stream):
        return stream.next().stdout.decode()

The "remote" script
~~~~~~~~~~~~~~~~~~~
For the purpose of this example, we have defined a small Python ``rot13``
program:

.. code-block:: python
    :caption: rot13.py

    import codecs

    try:
        while True:
            line = input()
            print(codecs.encode(line, 'rot_13'))

    except EOFError:
        pass

Defining the job
~~~~~~~~~~~~~~~~
Online job descriptions are the same as normal job descriptions.

.. code-block:: python

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

Putting it together
~~~~~~~~~~~~~~~~~~~

The rest is history.

.. code-block:: python

    import xenon

    # start the xenon-grpc server
    xenon.init()

    # on the local adaptor
    with xenon.Scheduler.create(adaptor='local') as scheduler:
        input_queue, input_stream = make_input_stream()

        # submit an interactive job, this gets us the job-id and a stream
        # yielding job output from stdout and stderr.
        job, output_stream = scheduler.submit_interactive_job(
            description=job_description, stdin_stream=input_stream())

        # next we feed the input_queue with messages
        try:
            for line in input_lines:
                print(" [sending]   " + line)
                input_queue.put(('msg', line + '\n'))
                msg = get_stdout(output_stream)
                print("[received]   " + msg)

        # make sure to close our end whatever may happen
        finally:
            input_queue.put(('end', None))
            input_queue.join()

        scheduler.wait_until_done(job)


Protocol definitions
--------------------
It can be instructive to see what the GRPC protocol with respect to interactive
jobs looks like.

.. code-block:: proto

    message SubmitInteractiveJobRequest {
        Scheduler scheduler = 1;
        JobDescription description = 2;
        bytes stdin = 3;
    }

    message SubmitInteractiveJobResponse {
        Job job = 1;
        bytes stdout = 2;
        bytes stderr = 3;
    }

    service SchedulerService {
        rpc submitInteractiveJob(
                stream SubmitInteractiveJobRequest)
            returns (stream SubmitInteractiveJobResponse) {}
    }

In `PyXenon` the remote procedure call ``submitInteractiveJob`` is wrapped to
the method :py:meth:`submit_interactive_job()` of the :py:class:`Scheduler`
class. Note that the ``SubmitInteractiveJobRequest`` specifies (next to the
scheduler, which is obtained from ``self`` in the method call) the job
description and ``bytes`` for standard input. Requests of this type are
streamed.  This means that GRPC expects to get an iterator of
``SubmitInteractiveJobRequest`` objets.

The `PyXenon` :py:meth:`submit_interactive_job()` method separates the
job-description and input-stream arguments. Sending the ``scheduler`` and
``description`` fields in the first request, followed up by a sequence of
requests where only the ``stdin`` field is specified. This latter sequence
is yielded from the ``stdin_stream`` argument.

Similarly, the first item in the output stream is guaranteed to only contain
the job-id, this first item is available immediately. Subsequent calls to
``next(output_stream)`` will block until output is available. The
:py:meth:`submit_interactive_job()` method takes the first item of the
iterator, and extracts the job-id. The user recieves a tuple with the
extracted job-id and the iterator.
