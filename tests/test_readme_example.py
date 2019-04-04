import xenon
from pathlib import Path
import os

def test_download_remote(xenon_server, tmpdir):
    tmpdir = Path(str(tmpdir))

    # create a new job scheduler, using SSH to localhost to submit new jobs.
    with xenon.Scheduler.create(
            adaptor='ssh', location='localhost') as scheduler:

        # make a new job description. The executable must already be present on
        # the target host.
        target = tmpdir / 'stdout.txt'
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

