import grpc
import xenon_pb2
import xenon_pb2_grpc


def run_job():
    channel = grpc.insecure_channel('localhost:50051')
    files = xenon_pb2_grpc.XenonFilesStub(channel)
    # put input
    localfs = files.newFileSystem(xenon_pb2.NewFileSystemRequest(adaptor='file'))
    remotefs = files.newFileSystem(xenon_pb2.NewFileSystemRequest(adaptor='sftp', location='localhost'))
    jobdir = '/tmp/myxenonjob'
    jobdir_path = xenon_pb2.Path(fs=remotefs, path=jobdir)
    files.createDirectories(jobdir_path)
    files.copy(xenon_pb2.CopyRequest(
        source=xenon_pb2.Path(fs=localfs, path='/etc/passwd'),
        target=xenon_pb2.Path(fs=remotefs, path=jobdir + '/somefile.txt')
    ))
    # call wc
    jobs = xenon_pb2_grpc.XenonJobsStub(channel)
    scheduler = jobs.newScheduler(xenon_pb2.NewSchedulerRequest(adaptor='ssh', location='localhost'))
    job_description = xenon_pb2.JobDescription(
        executable='wc',
        arguments=[jobdir + '/somefile.txt'],
        stdOut=[jobdir + '/stdout.txt'],
    )
    job = jobs.submitJob(xenon_pb2.SubmitJobRequest(scheduler=scheduler, description=job_description))
    job_status = jobs.waitUntilDone(job)
    if job_status.exitCode != 0:
        raise Exception(job_status.errorMessage)
    # get output
    files.copy(xenon_pb2.CopyRequest(
        source=xenon_pb2.Path(fs=remotefs, path=jobdir + '/stdout.txt'),
        target=xenon_pb2.Path(fs=localfs, path='stdout.txt')
    ))
    # $CWD/stdout.txt should contain output
    # cleanup
    files.delete(jobdir_path)
    files.closeFileSystem(remotefs)
    files.closeFileSystem(localfs)
    jobs.deleteJob(job)
    jobs.closeScheduler(scheduler)


def run_trigger_exception(adaptor, location=''):
    """
    Examples:

    >>> import client
    >>> client.run_trigger_exception("local")
    id: "local:/"
    request {
        adaptor: "local"
    }
    >>> client.run_trigger_exception("ssh", 'localhost')
    <_Rendezvous of RPC that terminated with (StatusCode.FAILED_PRECONDITION, ssh adaptor: Auth cancel)>
    >>> client.run_trigger_exception("sfdfdsh", 'localhost')
    <_Rendezvous of RPC that terminated with (StatusCode.FAILED_PRECONDITION, engine adaptor: Could not find adaptor for adaptor sfdfdsh)>

    """
    channel = grpc.insecure_channel('localhost:50051')
    jobs = xenon_pb2_grpc.XenonJobsStub(channel)
    try:
        return jobs.newScheduler(xenon_pb2.NewSchedulerRequest(adaptor=adaptor, location=location))
    except Exception as e:
        print(repr(e))
        # message is in e.details()
        return e


def run_adaptordescriptions():
    channel = grpc.insecure_channel('localhost:50051')
    stub = xenon_pb2_grpc.XenonJobsStub(channel)
    response = stub.getAdaptorDescriptions(xenon_pb2.Empty())
    print(response)

def run_exists(path):
    channel = grpc.insecure_channel('localhost:50051')
    files = xenon_pb2_grpc.XenonFilesStub(channel)
    localfss = files.localFileSystems(xenon_pb2.Empty())
    localfs = localfss[0]
    # localfs = files.newFileSystem(xenon_pb2.NewFileSystemRequest(adaptor='file'))
    response = files.exists(xenon_pb2.Path(filesystem=localfs, path=path))
    print(response)


if __name__ == '__main__':
    run_adaptors()
