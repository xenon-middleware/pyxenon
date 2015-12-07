# Python interface to Xenon

[![Build Status](https://travis-ci.org/NLeSC/pyxenon.svg?branch=master)](https://travis-ci.org/NLeSC/pyxenon)

Python interface to the [Xenon library](http://nlesc.github.io/Xenon/). Already functional, but will be improved.

## Installation

Simply run

```shell
make install
```

Currently, Xenon library version 1.1.0-SNAPSHOT is placed in the `libs` directory with its dependencies. To use another version by default, replace these jar files with alternative jar files and run `make reinstall`. Alternatively, the classpath can be overridden with `xenon.init()`.

## Usage

Except for initialization and finalization, the API follows the [Xenon 1.1.0 Java API](http://nlesc.github.io/Xenon/versions/1.1.0/javadoc/). First `xenon.init()` must be called to set up the Java classpath. Then `x = xenon.Xenon()` can be used to create a new Xenon instance. Either with-resources syntax is used, as shown the following example, or `x.close()` must be called to end Xenon. If neither is done, the object destructor will try to finalize Xenon. However, Python does not guarantee that the destructor is called.

```python
import xenon
import os

# set default classpath
xenon.init()
# override the classpath
# xenon.init(['path/to/xenon.jar', 'path/to/xenon/lib/*.jar'])

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

until no warnings appear. This checks against PEP8 code standards. Then commit, to make sure the change didn't break any code. Before a creating a pull request, run

    make fulltest

The pull request will be evaluated in [Travis](https://travis-ci.org/NLeSC/pyxenon).
