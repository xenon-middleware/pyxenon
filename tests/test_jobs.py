import os


def test_echo_job(xenon_server):
    xenon = xenon_server

    scheduler = xenon.jobs.newScheduler(
        xenon.NewSchedulerRequest(adaptor='local'))

    job_description = xenon.JobDescription(
        executable='/bin/bash',
        arguments=['-c', 'echo "Hello, World!"'],
        stdOut='hello.txt')

    job = xenon.jobs.submitJob(xenon.SubmitJobRequest(
        scheduler=scheduler, description=job_description))
    job_status = xenon.jobs.waitUntilDone(job)
    if job_status.exitCode != 0:
        raise Exception(job_status.errorMessage)
    xenon.jobs.deleteJob(job)
    xenon.jobs.close(scheduler)

    assert os.path.isfile('./hello.txt')
    lines = [l.strip() for l in open('./hello.txt')]
    assert lines[0] == 'Hello, World!'
    os.remove('./hello.txt')
