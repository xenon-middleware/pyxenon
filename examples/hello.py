from xenon import Xenon


with Xenon() as xenon:
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
