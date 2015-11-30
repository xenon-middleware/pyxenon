# Python interface to Xenon

[![Build Status](https://travis-ci.org/NLeSC/pyxenon.svg?branch=master)](https://travis-ci.org/NLeSC/pyxenon)

Python interface to the Xenon library. Already functional, but will be improved.

## Installation

Simply run

    make install

## Usage

```python
import xenon
import os

# set classpath
xenon.init(['path/to/xenon.jar', 'path/to/xenon/lib/*.jar'])

# start xenon
x = xenon.XenonFactory.newXenon(None)
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
Underneath, it exposes the full Xenon API.

## Contributing

To add a feature, first run

    make test

until no warnings appear. This checks against PEP8 code standards. Then commit, to make sure the change didn't break any code. Before a creating a pull-request, run

    make fulltest
