from .oop import (GrpcMethod, OopProxy, transform_map, mirror_enum, unwrap)
from .proto import (xenon_pb2, xenon_pb2_grpc)
import pathlib
import inspect
import functools
import os


CopyMode = mirror_enum('CopyMode')
PosixFilePermission = mirror_enum('PosixFilePermission')


class PathAttributes(OopProxy):
    def __init__(self, service, wrapped):
        super(PathAttributes, self).__init__(service, wrapped)

    @property
    def path(self):
        return Path(self.__wrapped__.path.path)


def append_request_stream(self, path, data_stream):
    yield xenon_pb2.AppendToFileRequest(
        path=xenon_pb2.Path(filesystem=self.__wrapped__,
                            path=unwrap(path)))
    yield from (xenon_pb2.AppendToFileRequest(buffer=b)
                for b in data_stream)


def write_request_stream(self, path, data_stream):
    yield xenon_pb2.WriteToFileRequest(
        path=xenon_pb2.Path(filesystem=self.__wrapped__,
                            path=unwrap(path)))
    yield from (xenon_pb2.WriteToFileRequest(buffer=b)
                for b in data_stream)


def path_transform(request_name, field_name='path'):
    request_type = getattr(xenon_pb2, request_name)

    def message_with_path(self, path, **kwargs):
        return request_type(
            path=xenon_pb2.Path(
                filesystem=self.__wrapped__,
                path=unwrap(path)),
            **kwargs)

    return message_with_path


def copy_request(self, source, dest_filesystem, dest_path,
                 mode=None, recursive=None):
    return xenon_pb2.CopyRequest(
        source=xenon_pb2.Path(filesystem=self.__wrapped__,
                              path=unwrap(source)),
        target=xenon_pb2.Path(filesystem=dest_filesystem.__wrapped__,
                              path=unwrap(dest_path)),
        mode=mode.value, recursive=recursive)


class Path(os.PathLike):
    __is_proxy__ = True
    __servicer__ = xenon_pb2_grpc.XenonFileSystemsServicer

    def __init__(self, path):
        if isinstance(path, pathlib.PosixPath):
            self._pathlib_path = path
        else:
            self._pathlib_path = pathlib.PosixPath(path)

    @property
    def __wrapped__(self):
        return self._pathlib_path.__fspath__()

    def __fspath__(self):
        return self._pathlib_path.__fspath__()

    def __getattr__(self, attr):
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
        return dir(self._pathlib_path)

    def is_hidden(self):
        return self.name[0] == '.'


# GrpcMethod('get_adaptor_descriptions', static=True),
# GrpcMethod(
#     'get_adaptor_description', static=True,
#     uses_request='AdaptorName'),


class FileSystem(OopProxy):
    __servicer__ = xenon_pb2_grpc.XenonFileSystemsServicer

    @classmethod
    def __methods__(cls):
        return [
            GrpcMethod(
                'rename', uses_request=True, field_name='filesystem'),
            GrpcMethod(
                'create_symbolic_link', uses_request=True,
                field_name='filesystem'),
            GrpcMethod(
                'get_working_directory',
                output_transform=lambda self, x: Path(x.path)),
            GrpcMethod(
                'set_working_directory',
                uses_request='Path', field_name='filesystem'),
            GrpcMethod(
                'is_open',
                output_transform=lambda self, x: x.value),
            GrpcMethod('close'),
            GrpcMethod(
                'cancel',
                uses_request='CopyOperation', field_name='filesystem'),
            GrpcMethod(
                'get_status',
                uses_request='CopyOperation', field_name='filesystem'),
            GrpcMethod(
                'wait_until_done',
                uses_request='CopyOperationWithTimeout',
                field_name='filesystem'),

            # Path methods
            GrpcMethod(
                'create_directories',
                uses_request='Path', field_name='filesystem'),
            GrpcMethod(
                'create_directory',
                uses_request='Path', field_name='filesystem'),
            GrpcMethod(
                'create_file',
                uses_request='Path', field_name='filesystem'),
            GrpcMethod(
                'exists',
                uses_request='Path', field_name='filesystem',
                output_transform=lambda self, x: x.value),
            GrpcMethod(
                'read_from_file',
                uses_request='Path', field_name='filesystem'),
            GrpcMethod(
                'get_attributes',
                uses_request='Path', field_name='filesystem',
                output_transform=PathAttributes),
            GrpcMethod(
                'read_symbolic_link',
                uses_request='Path', field_name='filesystem',
                output_transform=lambda self, x: Path(x.path)),

            GrpcMethod(
                'write_to_file',
                input_transform=write_request_stream),
            GrpcMethod(
                'append_to_file',
                input_transform=append_request_stream),

            GrpcMethod(
                'delete',
                input_transform=path_transform('DeleteRequest')),
            GrpcMethod(
                'copy',
                input_transform=copy_request,
                output_transform=lambda self, x: x.id),
            GrpcMethod(
                'set_posix_file_permissions',
                input_transform=path_transform(
                    'SetPosixFilePermissionsRequest')),
            GrpcMethod(
                'list',
                input_transform=path_transform(
                    'ListRequest', field_name='dir'),
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
        scheduler=self.__wrapped__, description=description, stdin=b'')
    yield from (xenon_pb2.SubmitInteractiveJobRequest(
        scheduler=None, description=None, stdin=msg)
        for msg in stdin_stream)


class Scheduler(OopProxy):
    __servicer__ = xenon_pb2_grpc.XenonSchedulersServicer

    @classmethod
    def __methods__(cls):
        return [
            GrpcMethod(
                'get_queues',
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
                uses_request=True, field_name='scheduler',
                output_transform=lambda self, x: x.id),
            GrpcMethod(
                'submit_interactive_job',
                input_transform=input_request_stream),
            GrpcMethod(
                'wait_until_done',
                uses_request='JobWithTimeout', field_name='scheduler'),
            GrpcMethod(
                'get_queue_status',
                uses_request='SchedulerAndQueue', field_name='scheduler'),
            GrpcMethod(
                'get_queue_statuses',
                uses_request='SchedulerAndQueues', field_name='scheduler')
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
