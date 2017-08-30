import xenon
from xenon import (Scheduler, JobDescription, JobStatus, Path)


xenon.init()

with Scheduler.create(adaptor='local') as scheduler:
    target = Path('hello.txt')
    if target.exists():
        target.unlink()

    job_description = JobDescription(
        executable='/bin/bash',
        arguments=['-c', 'echo "Hello, World!"'],
        stdout='hello.txt')

    job = scheduler.submit_batch_job(job_description)
    job_status = scheduler.wait_until_done(job)

    if job_status.error_type != JobStatus.NONE:
        raise Exception(job_status.error_message)

    print(''.join(open('hello.txt', 'r')))
