import xenon
import pathlib
import os

xenon.init()

target = pathlib.Path('hello.txt')

# if we're on linux
if os.name == 'posix':
    job_description = xenon.JobDescription(
        executable='/bin/bash',
        arguments=['-c', 'echo "Hello, World!"'],
        stdout=str(target))

# if we're on windows
elif os.name == 'nt':
    job_description = xenon.JobDescription(
        executable='cmd.exe',
        arguments=['/c', 'echo Hello, World!'],
        stdout=str(target))

else:
    raise RuntimeError("Unknown OS {}".format(os.name))

# open the local scheduler
with xenon.Scheduler.create(adaptor='local') as scheduler:
    # submit the job
    job = scheduler.submit_batch_job(job_description)
    # wait until done
    job_status = scheduler.wait_until_done(job)

    # if we were not successful, raise an exception
    if job_status.error_type != xenon.JobStatus.ErrorType.NONE:
        raise Exception(job_status.error_message)

# display the result
print(open(target, 'r').read(), end='')

# clean-up
target.unlink()
