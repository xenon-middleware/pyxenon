from .oop import (GrpcMethod, OopProxy, transform_map, mirror_enum, unwrap)
from .proto import (xenon_pb2, xenon_pb2_grpc)
import pathlib
import inspect
import functools
import os


# CopyMode = mirror_enum('CopyMode')
PosixFilePermission = mirror_enum('PosixFilePermission')


class PathAttributes(OopProxy):
    def __init__(self, service, wrapped):
        super(PathAttributes, self).__init__(service, wrapped)

    @property
    def path(self):
        return Path(self.__wrapped__.path.path)


class CopyOperation(OopProxy):
    pass


class Job(OopProxy):
    pass


class Is(OopProxy):
    def __bool__(self):
        return self.value


def append_request_stream(self, path, data_stream):
    yield xenon_pb2.AppendToFileRequest(
            filesystem=unwrap(self), path=unwrap(path))
    yield from (xenon_pb2.AppendToFileRequest(buffer=b)
                for b in data_stream)


def write_request_stream(self, path, data_stream):
    yield xenon_pb2.WriteToFileRequest(
            filesystem=unwrap(self), path=unwrap(path))
    yield from (xenon_pb2.WriteToFileRequest(buffer=b)
                for b in data_stream)


class Path(object):
    """Wrapper around `pathlib.PosixPath`. This class reveals a string
    representation of the underlying path object to GRPC. You may use
    this class like a `pathlib.PosixPath`, including using it as an
    argument to `open` calls as it derives from `os.PathLike`."""
    __is_proxy__ = True
    __servicer__ = xenon_pb2_grpc.FileSystemServiceServicer

    def __init__(self, path):
        if isinstance(path, pathlib.PosixPath):
            self._pathlib_path = path
        elif isinstance(path, xenon_pb2.Path):
            self._pathlib_path = pathlib.PosixPath(path.path)
        else:
            self._pathlib_path = pathlib.PosixPath(path)

    def __str__(self):
        return str(self._pathlib_path)

    @property
    def __wrapped__(self):
        return xenon_pb2.Path(
            path=str(self._pathlib_path),  # .__fspath__(),
            separator='/')

    def __fspath__(self):
        return self._pathlib_path.__fspath__()

    def __getattr__(self, attr):
        if attr == '__wrapped__':
            print("Warning: faulty Python behaviour.")
            return xenon_pb2.Path(
                path=str(self._pathlib_path),  # .__fspath__(),
                separator='/')

        member = getattr(self._pathlib_path, attr)
        if inspect.ismethod(member):
            @functools.wraps(member)
            def wrapped_member(*args, **kwargs):
                value = member(*args, **kwargs)
                if isinstance(value, pathlib.PosixPath):
                    return Path(value)
                else:
                    return value

            return wrapped_member

        elif isinstance(member, pathlib.PosixPath):
            return Path(member)

        else:
            return member

    def __dir__(self):
        return dir(self._pathlib_path) + dir(self)

    def is_hidden(self):
        """Checks if a file is hidden. Just compares the first character in the
        filename with `'.'`."""
        return self.name[0] == '.'


class FileSystem(OopProxy):
    """Wraps the FileSystems sub-system."""
    __servicer__ = xenon_pb2_grpc.FileSystemServiceServicer
    __field_name__ = 'filesystem'

    @classmethod
    def __methods__(cls):
        return [
            GrpcMethod('get_adaptor_name', output_transform=lambda self, x: x.name),
            GrpcMethod(
                'rename', uses_request=True),
            GrpcMethod(
                'create_symbolic_link', uses_request=True),
            GrpcMethod(
                'get_working_directory',
                output_transform=Path),
            GrpcMethod(
                'set_working_directory',
                uses_request='PathRequest'),
            GrpcMethod(
                'is_open',
                output_transform=Is),
            GrpcMethod('close'),
            GrpcMethod(
                'cancel',
                uses_request='CopyOperationRequest'),
            GrpcMethod(
                'get_status',
                uses_request='CopyOperationRequest'),
            GrpcMethod(
                'wait_until_done',
                uses_request=True),

            # Path methods
            GrpcMethod(
                'create_directories',
                uses_request='PathRequest'),
            GrpcMethod(
                'create_directory',
                uses_request='PathRequest'),
            GrpcMethod(
                'create_file',
                uses_request='PathRequest'),
            GrpcMethod(
                'exists',
                uses_request='PathRequest',
                output_transform=Is),
            GrpcMethod(
                'read_from_file',
                uses_request='PathRequest'),
            GrpcMethod(
                'get_attributes',
                uses_request='PathRequest',
                output_transform=PathAttributes),
            GrpcMethod(
                'read_symbolic_link',
                uses_request='PathRequest',
                output_transform=Path),

            GrpcMethod(
                'write_to_file',
                input_transform=write_request_stream),
            GrpcMethod(
                'append_to_file',
                input_transform=append_request_stream),

            GrpcMethod('delete', uses_request=True),
            GrpcMethod(
                'copy', uses_request=True,
                output_transform=CopyOperation),
            GrpcMethod('set_posix_file_permissions', uses_request=True),
            GrpcMethod(
                'list', uses_request=True,
                output_transform=transform_map(PathAttributes))
        ]

    @staticmethod
    def create(server, *args, **kwargs):
        return FileSystem(
            server.file_systems.stub,
            server.file_systems.create(*args, **kwargs))

    def __init__(self, service, wrapped):
        super(FileSystem, self).__init__(service, wrapped)

    def path(self, path):
        return Path(
            self.__service__,
            xenon_pb2.Path(filesystem=self.__wrapped__, path=path))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.close()

    def __eq__(self, other):
        return self.__wrapped__ == other.__wrapped__


def input_request_stream(self, description, stdin_stream):
    yield xenon_pb2.SubmitInteractiveJobRequest(
        scheduler=unwrap(self), description=description, stdin=b'')
    yield from (xenon_pb2.SubmitInteractiveJobRequest(
        scheduler=None, description=None, stdin=msg)
        for msg in stdin_stream)


def interactive_job_response(self, stream):
    job = stream.next().job
    return job, stream


class Scheduler(OopProxy):
    """Wraps the Schedulers subsystem."""
    __servicer__ = xenon_pb2_grpc.SchedulerServiceServicer
    __field_name__ = 'scheduler'

    @classmethod
    def __methods__(cls):
        return [
            GrpcMethod('get_adaptor_name', output_transform=lambda self, x: x.name),
            GrpcMethod('get_location', output_transform=lambda self, x: x.location),
            GrpcMethod('get_properties', output_transform=lambda self, x: x.properties),

            GrpcMethod(
                'get_jobs',
                uses_request='SchedulerAndQueues',
                output_transform=lambda self, x: x.jobs),
            GrpcMethod(
                'get_queue_names',
                output_transform=lambda self, x: x.name),
            GrpcMethod(
                'get_default_queue_name',
                output_transform=lambda self, x: x.name),
            GrpcMethod(
                'is_open',
                output_transform=lambda self, x: x.value),
            GrpcMethod('close'),
            GrpcMethod(
                'submit_batch_job',
                uses_request=True,
                output_transform=Job),
            GrpcMethod(
                'submit_interactive_job',
                input_transform=input_request_stream,
                output_transform=interactive_job_response),
            GrpcMethod('cancel_job', uses_request='JobRequest'),
            GrpcMethod('wait_until_done', uses_request='WaitRequest'),
            GrpcMethod('wait_until_running', uses_request='WaitRequest'),
            GrpcMethod('get_queue_status', uses_request=True),
            GrpcMethod('get_queue_statuses', uses_request='SchedulerAndQueues')
        ]

    @staticmethod
    def create(server, *args, **kwargs):
        return Scheduler(
            server.schedulers.stub,
            server.schedulers.create(*args, **kwargs))

    def __init__(self, service, wrapped):
        super(Scheduler, self).__init__(service, wrapped)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.close()
