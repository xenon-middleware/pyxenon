# Python interface to Xenon

![License](https://img.shields.io/github/license/NLeSC/pyxenon.svg)
[![Build Status](https://travis-ci.org/NLeSC/pyxenon.svg?branch=master)](https://travis-ci.org/NLeSC/pyxenon)
[![Codacy Badge](https://api.codacy.com/project/badge/grade/35e155e3bb08459aa2c24622d5fdb0d3)](https://www.codacy.com/app/NLeSC/pyxenon)

Python interface to the [Xenon middleware library](http://nlesc.github.io/Xenon/). Xenon provides a simple programming interface to various pieces of software that can be used to access distributed compute and storage resources. Underneath it uses [pyjnius](https://github.com/kivy/pyjnius), which uses Cython and the Java Native Interface to interface with a Java Virtual Machine.

## Installation

First export environment variable `JDK_HOME` pointing to your JDK installation. Then run

```shell
make install
```
This will run `pip install` internally. If pip imports this package, make sure to install `Cython==0.23.4` before installing `pyxenon`, because `pyjnius` will otherwise deduce its dependencies in the wrong order.

Currently, Xenon library version 1.1.0-SNAPSHOT is placed in the `libs` directory with its dependencies. To use another version, replace these jar files with alternative jar files and run `make reinstall`. Alternatively, a custom classpath can be provided to `xenon.init()`.

## Usage

Except for initialization and finalization, the API follows the [Xenon 1.1.0 Java API](http://nlesc.github.io/Xenon/versions/1.1.0/javadoc/). First `xenon.init()` must be called to set up the Java Virtual Machine and its classpath. Then `x = xenon.Xenon()` creates a new Xenon instance. Either use with-resources syntax, as shown the following example, or call `x.close()` to end Xenon. If neither is done, the object destructor will try to finalize Xenon. However, Python does not guarantee that this destructor is called, which may cause a Java process running after python has finished execution.

```python
import xenon
import os

# use default classpath
xenon.init()

# start xenon
with xenon.Xenon() as x:
	jobs = x.jobs()
	sched = jobs.newScheduler('ssh', 'localhost', None, None)

	# make a new job description
	desc = xenon.jobs.JobDescription()
	desc.setExecutable('hostname')
	desc.setStdout(os.getcwd() + '/stdout.txt')

	# submit a job
	job = jobs.submitJob(sched, desc)
	jobs.waitUntilDone(job, 1000)

	with open(job.getJobDescription().getStdout()) as f:
	    print(f.read())
```

## API

The API consists of all methods exported in `__init__.py`, `xenon.files`, `xenon.jobs` and `xenon.exceptions`. 

## Contributing

Contributions can be made using GitHub pull requests. To add a feature, first run

    make test

until no warnings appear. This will also try to install test dependencies of `test_requirements.txt`. The command checks against PEP8 code standards and syntax errors. Then commit, to make sure the change didn't break any code. Before a creating a pull request, run

    make fulltest

The pull request will be evaluated in [Travis](https://travis-ci.org/NLeSC/pyxenon).
