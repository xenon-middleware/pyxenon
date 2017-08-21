from .oop import (GrpcMethod, OopProxy, transform_map, mirror_enum)
from .proto import (xenon_pb2, xenon_pb2_grpc)


CopyMode = mirror_enum('CopyMode')
PosixFilePermission = mirror_enum('PosixFilePermission')


class PathAttributes(OopProxy):
    def __init__(self, service, wrapped):
        super(PathAttributes, self).__init__(service, wrapped)
        self.path = Path(service, wrapped.path)


def append_request_stream(self, data_stream):
    yield xenon_pb2.AppendToFileRequest(path=self.__wrapped__)
    yield from (xenon_pb2.AppendToFileRequest(buffer=b)
                for b in data_stream)


def write_request_stream(self, data_stream):
    yield xenon_pb2.WriteToFileRequest(path=self.__wrapped__)
    yield from (xenon_pb2.WriteToFileRequest(buffer=b)
                for b in data_stream)


class Path(OopProxy):
    __servicer__ = xenon_pb2_grpc.XenonFileSystemsServicer

    @classmethod
    def __methods__(cls):
        return [
            GrpcMethod('create_directories'),
            GrpcMethod('create_directory'),
            GrpcMethod('create_file'),
            GrpcMethod(
                'exists',
                output_transform=lambda self, x: x.value),
            GrpcMethod('read_from_file'),
            GrpcMethod(
                'get_attributes',
                output_transform=PathAttributes),
            GrpcMethod('set_working_directory'),
            GrpcMethod(
                'read_symbolic_link',
                output_transform=cls),
            GrpcMethod(
                'write_to_file',
                input_transform=write_request_stream),
            GrpcMethod(
                'append_to_file',
                input_transform=append_request_stream),
            GrpcMethod(
                'delete', uses_request=True, field_name='path'),
            GrpcMethod(
                'copy', uses_request=True, field_name='source',
                output_transform=lambda self, x: x.id),
            GrpcMethod(
                'set_posix_file_permissions',
                uses_request=True, field_name='path'),
            GrpcMethod(
                'list', uses_request=True, field_name='dir',
                output_transform=transform_map(PathAttributes))
        ]

    def __init__(self, service, wrapped):
        super(Path, self).__init__(service, wrapped)

    @property
    def filesystem(self):
        return FileSystem(self.__service__, self.__wrapped__.filesystem)

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
                output_transform=Path),
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
