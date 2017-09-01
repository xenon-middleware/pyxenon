import xenon
from xenon import (Scheduler, JobDescription, JobStatus, Path)
import pathlib
import os

xenon.init()

with Scheduler.create(adaptor='local') as scheduler:
    target = pathlib.Path('hello.txt')
    if target.exists():
        target.unlink()

    if os.name == 'posix':
        job_description = JobDescription(
            executable='/bin/bash',
            arguments=['-c', 'echo "Hello, World!"'],
            stdout='hello.txt')
    elif os.name == 'nt':
        job_description = JobDescription(
            executable='cmd.exe',
            arguments=['/c', 'echo Hello, World!'],
            stdout='hello.txt')
    else:
        raise RuntimeError("Unknown OS")

    job = scheduler.submit_batch_job(job_description)
    job_status = scheduler.wait_until_done(job)

    if job_status.error_type != JobStatus.NONE:
        raise Exception(job_status.error_message)

    print(''.join(open(target, 'r')))
