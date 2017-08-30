Python interface to Xenon, GRPC Branch
======================================

We're rewriting PyXenon on top of the GRPC API for Xenon. This work will result in version 2.0 of PyXenon.

Development
-----------
Until we release PyXenon 2.0, we don't ship the `xenon-grpc` `jar` file in this repository. Build it manually, following instructions at `Xenon-GRPC <https://github.com/nlesc/xenon-grpc>`__, and place the contents of the `build/install/xenon-grpc-shadow` folder somewhere findable.

To generate the `grpc` code, run `scripts/protoc.sh` from the project root.

Testing
-------

Run the following docker container to test against remote slurm

.. code-block:: bash

    docker run --detach --publish 10022:22 nlesc/xenon-slurm:17


Old README
==========

|Python versions| |DOI| |PyPi version| |Apache 2 License| |Build Status|
|Codacy Badge|


Python interface to the `Xenon middleware
library <http://nlesc.github.io/Xenon/>`__. Xenon provides a simple
programming interface to various pieces of software that can be used to
access distributed compute and storage resources. Underneath it uses
`JPype <https://jpype.readthedocs.io>`__, which uses the Java Native
Interface to interface with a Java Virtual Machine.

Installation
------------

The package is available on PyPi, to use that release, just install
with:

::

    pip install -U pyxenon

To install from source, run,

::

    pip install -U .

If the install fails due to a missing Java requirement, export
environment variable ``JAVA_HOME`` pointing to your Java installation
and try again.

Currently, Xenon library version 1.1.0 is placed in the ``xenon/libs``
directory with its dependencies. To use another version, replace these
jar files with alternative jar files and run ``pip install -U .``.
Alternatively, a custom classpath can be provided to ``xenon.init()``.

Usage
-----

Except for initialization and finalization, the API follows the `Xenon
1.1.0 Java
API <http://nlesc.github.io/Xenon/versions/1.1.0/javadoc/>`__. First
``xenon.init()`` must be called to set up the Java Virtual Machine and
its classpath. Then ``x = xenon.Xenon()`` creates a new Xenon instance.
Either use with-resources syntax, as shown the following example, or
call ``x.close()`` to end Xenon. If neither is done, the object
destructor will try to finalize Xenon. However, Python does not
guarantee that this destructor is called, which may cause a Java process
running after python has finished execution.

See `JPype documentation <https://jpype.readthedocs.io>`__ for how to
use Java classes in Python.

.. code-block:: python

    import xenon
    import os

    # use default classpath
    xenon.init()

    # start xenon
    with xenon.Xenon() as x:
        # create a new job scheduler, using SSH to localhost to submit new jobs.
        jobs = x.jobs()
        sched = jobs.newScheduler('ssh', 'localhost', None, None)

        # make a new job description. The executable must already be present on the target host.
        desc = xenon.jobs.JobDescription()
        desc.setExecutable('hostname')
        desc.setStdout(os.getcwd() + '/stdout.txt')

        # submit a job
        job = jobs.submitJob(sched, desc)
        jobs.waitUntilDone(job, 1000)

        # read the standard output of the job. We can do this directly because
        # we ran on localhost, otherwise, we need to transfer the file first.
        with open(job.getJobDescription().getStdout()) as f:
            print(f.read())

API
---

The API consists of all methods and classes exported in ``__init__.py``,
``xenon.files``, ``xenon.jobs``, ``xenon.exceptions``, and
``xenon.conversions``. Of each of the classes, find further
documentation in the corresponding Xenon class. To construct Java classes, use
``from xenon import java, nl`` to get the ``java`` and ``nl`` root packages.
For other custom classes or packages the ``xenon.JavaClass`` or
``xenon.JavaPackage`` classes.

.. code-block:: python

    import xenon
    xenon.init()

    from xenon import java
    array = java.util.ArrayList()

    from xenon import JavaClass
    logger = JavaClass('org.slf4j.LoggerFactory').getLogger('python')
    logger.debug('Hello world')

.. caution::
   ``JavaClass``, ``JavaPackage``, ``java``, ``javax`` and ``nl`` can be used
   throughout the code, but functions or attribute access on them can only be
   made AFTER ``xenon.init()`` is called. Before that time, access will raise
   an ``EnvironmentError``.

For limitations on Java with Python see the `JPype
documentation <http://jpype.readthedocs.io/en/latest/>`__. In
particular, everywhere where in the Java API a varargs is expected as a
function argument (e.g.
``public getJobs(Scheduler scheduler, Job... jobs))``), provide an list
instead of a variable number of arguments. The easiest way to make a Java
char-array from a Python string is to use
``java.lang.String(mystring).toCharArray()``. To easily pass a ``dict`` or read
a ``HashMap``, use the ``xenon.conversions.{dict_to_HashMap, Map_to_dict}``
functions.

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
standards and syntax errors on Python 2.7 and 3.5. Then commit, to make sure
the change didn't break any code. The pull request will be evaluated in
`Travis <https://travis-ci.org/NLeSC/pyxenon>`__.

.. note::
    If different versions of Python are installed locally, modify ``tox.ini``
    to reflect your installed Python versions.

.. |DOI| image:: https://zenodo.org/badge/doi/10.5281/zenodo.60929.svg
   :target: http://dx.doi.org/10.5281/zenodo.60929
.. |PyPi version| image:: https://img.shields.io/pypi/v/pyxenon.svg
   :target: https://pypi.python.org/pypi/pyxenon
.. |Apache 2 License| image:: https://img.shields.io/github/license/NLeSC/pyxenon.svg?branch=master
   :target: https://raw.githubusercontent.com/NLeSC/pyxenon/master/LICENSE
.. |Python versions| image:: https://img.shields.io/pypi/pyversions/pyxenon.svg
.. |Build Status| image:: https://travis-ci.org/NLeSC/pyxenon.svg?branch=master
   :target: https://travis-ci.org/NLeSC/pyxenon
.. |Codacy Badge| image:: https://api.codacy.com/project/badge/grade/35e155e3bb08459aa2c24622d5fdb0d3
   :target: https://www.codacy.com/app/NLeSC/pyxenon
