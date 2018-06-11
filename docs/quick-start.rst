Quick Start
-----------

We like to test Xenon against a `Docker`_ image: `nlesc/xenon-slurm`_.
If you have docker all setup, you can run this image as follows::

    $ docker pull nlesc/xenon-slurm
    ...
    $ docker run --detach --publish 10022:22 nlesc/xenon-slurm

Try logging onto this image by `ssh`, to make sure everything works. The
username is `xenon`, the password `javagat`::

    $ ssh localhost -p 10022 -l xenon
    xenon@localhost's password: <javagat>
    $ exit
    Connection to localhost closed.

Starting the server
~~~~~~~~~~~~~~~~~~~
To get anything done in PyXenon, we need to start the GRPC server:

.. code-block:: python

    import xenon

    xenon.init()

Writing to a remote filesystem
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Next, let's try to copy a file to the container. We need credentials to
access anything on the remote side.

.. code-block:: python

    from xenon import PasswordCredential, FileSystem

    credential = PasswordCredential(
        username='xenon',
        password='javagat')

    remotefs = FileSystem.create(
        'sftp', location='localhost:10022',
        password_credential=credential)

We can write to a file by streaming. The second argument to
:py:meth:`write_to_file` should be an iterable. It will be read in a separate
thread, so it is allowed to be blocking. Here we'll do nothing so fancy:

.. code-block:: python

    from xenon import Path

    target = Path('hello.sh')

    if remotefs.exists(target):
        remotefs.delete(target)

    remotefs.write_to_file(
        target,
        [b'#!/bin/sh\n',
         b'echo "Hello, World!"\n'])

Running a script
~~~~~~~~~~~~~~~~
The remote machine runs a SLURM job scheduler. We describe a job in a
:py:class:`JobDescription` object. This seems a bit long-winded, but in
practice you'll be reusing the descriptions a lot.

.. code-block:: python

    from xenon import Scheduler

    scheduler = Scheduler.create(
        adaptor='slurm',
	location='ssh://localhost:10022',
	password_credential=credential)

    job_description = JobDescription(
        executable='/bin/sh',
        arguments=['hello.sh'],
        stdout='result.txt')

    job = scheduler.submit_batch_job(job_description)

    state = scheduler.wait_until_done(job)
    print(state)


Retrieving the result
~~~~~~~~~~~~~~~~~~~~~
Just as we can write data by sending an iterable, we can read data from a file
and recieve a generator yielding bytes objects. Here we realize the transfer by
joining the data chunks into a string:

.. code-block:: python

    text = ''.join(chunk.decode() for chunk in
        remotefs.read_from_file(Path('result.txt')))
    print(text)

.. _Docker: https://www.docker.com/
.. _nlesc/xenon-slurm: https://hub.docker.com/r/nlesc/xenon-slurm/
