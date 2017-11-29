from .server import (init)

from .oop import (
    list_attributes)

from .objects import (
    FileSystem, Scheduler, Path, Job,
    PosixFilePermission, CopyMode, CopyStatus, JobStatus, QueueStatus)

from .proto.xenon_pb2 import (
    JobDescription,
    CopyRequest, CertificateCredential, PasswordCredential,
    PropertyDescription, CredentialMap, DefaultCredential,
    UserCredential)

from .exceptions import (
    UnknownRpcException, XenonException, PathAlreadyExistsException)

from .version import (
    pyxenon_version)


JobDescription.__doc__ = \
    """This class describes a job to a Scheduler instance.\n\n""" \
    + "\n".join(
            ["    :ivar {0}: {0}\n    :vartype {0}: {1}\n".format(*x)
             for x in list_attributes(JobDescription.DESCRIPTOR)])


__version__ = pyxenon_version
__all__ = [
    'init',
    'FileSystem', 'Scheduler', 'Path',
    'PosixFilePermission', 'Job',
    'JobDescription', 'CopyRequest', 'QueueStatus', 'JobStatus',
    'CopyStatus', 'CertificateCredential', 'PasswordCredential',
    'PropertyDescription', 'CredentialMap', 'DefaultCredential',
    'UserCredential', 'CopyMode',

    'UnknownRpcException', 'XenonException', 'PathAlreadyExistsException']
