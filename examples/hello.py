from xenon import Xenon
import time


with Xenon() as xenon:
    time.sleep(1)

    scheduler = xenon.jobs.newScheduler(
        xenon.NewSchedulerRequest(adaptor='local'))

    job_description = xenon.JobDescription(
        executable='echo',
        arguments=['"Hello, World!"'],
        stdOut='hello.txt')

    job = xenon.jobs.submitJob(xenon.SubmitJobRequest(
        scheduler=scheduler, description=job_description))
    job_status = xenon.jobs.waitUntilDone(job)
    if job_status.exitCode != 0:
        raise Exception(job_status.errorMessage)
    xenon.jobs.deleteJob(job)
    xenon.jobs.closeScheduler(scheduler)

