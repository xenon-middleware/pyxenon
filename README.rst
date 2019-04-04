Python interface to Xenon 2.0
=============================
|ZenodoBadge| |ReadTheDocsBadge| |Apache2License| |BuildStatus| |CodacyBadge|

Python interface to the `Xenon middleware library, v. 2.0
<http://nlesc.github.io/Xenon/>`__. Xenon provides a simple programming
interface to various pieces of software that can be used to access distributed
compute and storage resources.

Underneath it uses `GRPC <https://grpc.io>`__, to connect to the `Xenon-GRPC
<https://github.com/NLeSC/xenon-grpc>`__ service.
We've taken care to mirror the original Java API in this Python module as much
as possible.

Installing
----------
Clone this repository, and do::

    pip install .

The code will appear on PyPI when it is ready for release.

Documentation
-------------
The compiled documentation is hosted on `Read the Docs
<http://pyxenon.readthedocs.io/en/latest>`__. This includes a quick-start
guide.

Development
-----------
PyXenon ships with the `Xenon-GRPC` jar-file and command-line executable. If
these need upgrading, build them manually, following instructions at
`Xenon-GRPC <https://github.com/nlesc/xenon-grpc>`__, and place the contents of the
``build/install/xenon-grpc-shadow`` folder (``lib`` and ``bin``) here.

To generate the `GRPC` code, run ``scripts/protoc.sh`` from the project root.

Testing
-------
Unit tests all run against the `local` scheduler and the `file` adaptor for
filesystems. To run them, just do::

    $ pytest ./tests

For faster testing it may be useful to start the ``xenon-grpc`` daemon
manually; start it in a separate terminal as it may give useful output for
debugging.

For integration testing, run the following docker container to test against
remote slurm

.. code-block:: bash

    docker run --detach --publish 10022:22 nlesc/xenon-slurm:17

An example of some code running against this container is in
``examples/tutorial.py``.

Example
-------

.. code-block:: python

    import xenon
    from pathlib import Path
    import os

    xenon.init()

    # create a new job scheduler, using SSH to localhost to submit new jobs.
    with xenon.Scheduler.create(
            adaptor='ssh', location='localhost') as scheduler:

        # make a new job description. The executable must already be present on
        # the target host.
        target = Path('.') / 'stdout.txt'
        desc = xenon.JobDescription(
            executable='hostname',
            stdout=str(target.resolve()))

        # submit a job
        job = scheduler.submit_batch_job(desc)
        status = scheduler.wait_until_done(job, 1000)

        # read the standard output of the job. We can do this directly because
        # we ran on localhost, otherwise, we need to transfer the file first.
        with open(target) as f:
            print(f.read())

Contributing
------------

Contributions can be made using GitHub pull requests. To add a feature,
first install the test requirements

::

    pip install -U tox

and then run

::

    tox

until all tests succeed. The command checks against flake8 code
standards and syntax errors on Python 3.5 and 3.6. Then commit, to make sure
the change didn't break any code. The pull request will be evaluated in
`Travis <https://travis-ci.org/NLeSC/pyxenon>`__.

.. |DOI| image:: https://zenodo.org/badge/doi/10.5281/zenodo.60929.svg
   :target: http://dx.doi.org/10.5281/zenodo.60929
.. |PyPi version| image:: https://img.shields.io/pypi/v/pyxenon.svg
   :target: https://pypi.python.org/pypi/pyxenon
.. |Apache2License| image:: https://img.shields.io/github/license/NLeSC/pyxenon.svg?branch=master
   :target: https://raw.githubusercontent.com/NLeSC/pyxenon/master/LICENSE
.. |PythonVersions| image:: https://img.shields.io/pypi/pyversions/pyxenon.svg
.. |BuildStatus| image:: https://travis-ci.org/xenon-middleware/pyxenon.svg?branch=master
   :target: https://travis-ci.org/NLeSC/pyxenon
.. |CodacyBadge| image:: https://api.codacy.com/project/badge/grade/35e155e3bb08459aa2c24622d5fdb0d3
   :target: https://www.codacy.com/app/NLeSC/pyxenon
.. |ReadTheDocsBadge| image:: https://readthedocs.org/projects/pyxenon/badge/?version=latest
   :target: http://pyxenon.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status
.. |ZenodoBadge| image:: https://zenodo.org/badge/47132292.svg
   :target: https://zenodo.org/badge/latestdoi/47132292
