from xenon import (
    PasswordCredential, FileSystem, CopyRequest, Path, CopyStatus,
    Scheduler, JobDescription)


def test_rse_tutorial(xenon_server, tmpdir, slurm_container):
    xenon = xenon_server
    tmpdir = Path(str(tmpdir))
    location = '0.0.0.0:10022'

    #
    # step 0: write our script
    #
    sleep_script = [
        "#!/bin/bash",
        "echo \"Sleeping for $1 second(s).\"",
        "sleep $1"
    ]

    with open(tmpdir / 'sleep.sh', 'w') as f:
        for line in sleep_script:
            print(line, file=f)

    #
    # step 1: upload input  files
    #
    # create the local filesystem representation
    local_fs = FileSystem.create(xenon, adaptor='file')

    # the remote system requires credentials, create them here:
    credential = PasswordCredential(
            username='xenon',
            password='javagat')

    # create the remote filesystem representation and specify the
    # executable's path
    remote_fs = FileSystem.create(
            xenon,
            adaptor='sftp',
            location=location,
            password_credential=credential)

    # when waiting for jobs or copy operations to complete, wait
    # indefinitely
    WAIT_INDEFINITELY = 0

    # specify the path of the script file on the local and on the remote
    local_file = tmpdir / 'sleep.sh'
    remote_file = Path('/home/xenon/sleep.sh')

    # start the copy operation; no recursion, we're just copying a file
    copy_id = local_fs.copy(local_file, remote_fs, remote_file,
                            mode=CopyRequest.REPLACE, recursive=False)

    # wait for the copy operation to complete (successfully or otherwise)
    copy_status = local_fs.wait_until_done(copy_id, WAIT_INDEFINITELY)
    if copy_status.error_message:
        raise RuntimeError(copy_status.error)

    #
    # step 2: submit job and capture its job identifier
    #
    scheduler = Scheduler.create(
            xenon,
            adaptor='slurm',
            location=location,
            password_credential=credential)

    # compose the job description:
    job_description = JobDescription(
            executable='bash',
            arguments=['sleep.sh', '0'],
            stdout='sleep.stdout.txt')

    job_id = scheduler.submit_batch_job(job_description)

    # wait for the job to finish before attempting to copy its output
    # file(s)
    job_status = scheduler.wait_until_done(job_id, 1000)

    # rethrow the Exception if we got one
    if job_status.error_message:
        raise RuntimeError(job_status.error_message)

    # make sure to synchronize the remote filesystem
    job_id = scheduler.submit_batch_job(JobDescription(
            executable='sync'))
    scheduler.wait_until_done(job_id)

    #
    # step 3: download generated output file(s)
    #
    # specify the path of the stdout file on the remote and on the local
    # machine
    remote_file = Path('/home/xenon/sleep.stdout.txt')
    local_file = Path(tmpdir / 'sleep.stdout.txt')

    # start the copy operation; no recursion, we're just copying a file
    copy_id = remote_fs.copy(remote_file, local_fs, local_file,
                             mode=CopyRequest.REPLACE, recursive=False)

    # wait for the copy operation to complete (successfully or otherwise)
    copy_status = remote_fs.wait_until_done(copy_id, 1000)
    assert copy_status.done

    # rethrow the Exception if we got one
    assert copy_status.error_type == CopyStatus.NONE, \
        copy_status.error_message

    local_fs.close()
    remote_fs.close()
    scheduler.close()

    print('Done')

    assert (tmpdir / 'sleep.stdout.txt').exists()
    lines = [l.strip() for l in open(tmpdir / 'sleep.stdout.txt', 'r')]
    assert lines == ["Sleeping for 0 second(s)."]
