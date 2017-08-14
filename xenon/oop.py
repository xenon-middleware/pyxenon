from .proto import xenon_pb2


class GrpcMethod:
    def __init__(self, name, input_transforms=None, output_transform=None):
        self.name = name
        self.input_transforms = input_transforms or ()
        self.output_transform = output_transform

    @property
    def is_simple(self):
        return not self.input_transforms and not self.output_transform


def apply_transform(service)
    def applier(t, x):
        if t is None:
            return x
        else:
            return t(service, x)

    return applier


def method_wrapper(m):
    def simple_method(self, *args):
        return getattr(self.__service__, m.name)(self.__wrapped__, *args)

    if m.is_simple:
        return simple_method

    def transforming_method(self, *args):
        f = getattr(self.__service__, m.name)
        args = map(apply_transform(self), m.input_transforms, args)
        return apply_transform(self)(m.output_transform, f(*args))

    return transforming_method


class OopMeta(type):
    def __new__(cls, name, parents, dct):
        super(OopMeta, cls).__new__(cls, name, parents, dct)

    def __init__(cls, name, parents, dct):
        super(OopMeta, cls).__init__(cls, name, parents, dct)

        for name in methods:
            setattr(cls, name, method_wrapper(name))


class OopProxy:
    __metaclass__ = OopMeta

    methods = []

    def __init__(self, service, wrapped):
        self.__service__ = service
        self.__wrapped__ = wrapped

    def __getattr__(self, attr):
        return getattr(self.__wrapped__, attr)


class FileSystem(OopProxy):
    methods = [
        GrpcMethod(
            'get_working_directory', None,
            output_transform=Path),
        GrpcMethod(
            'is_open', None,
            output_transform=lambda self, x: x.value),
        GrpcMethod('close')
    ]

    def __init__(self, service, *args):
        super(FileSystem, self).__init__(service, service.create(*args))


class Path(OopProxy):
    methods = [
        GrpcMethod('create_directories'),
        GrpcMethod('create_directory'),
        GrpcMethod('create_file'),
        GrpcMethod(
            'exists', None,
            output_transform=lambda self, x: x.value),
        GrpcMethod('read_from_file'),
        GrpcMethod('get_attributes'),
        GrpcMethod('set_working_directory'),
        GrpcMethod(
            'read_symbolic_link', None,
            output_transform=Path),
        GrpcMethod('delete'),
        GrpcMethod('copy'),
        GrpcMethod('set_posix_file_permissions'),
        GrpcMethod(
            'list', None,
            output_transform=lambda self, xs: (PathAttribute(self.__service__, x) for x in xs))
    ]

    def __init__(self, service, wrapped):
        super(Path, self).__init__(service, wrapped)


class PathAttribute(OopProxy):
    def __init__(self, service, wrapped):
        super(PathAttribute, self).__init__(service, wrapped)
        self.path = Path(service, wrapped.path)


class Scheduler(OopProxy):
    methods = [
        GrpcMethod('get_queues',
            output_transform=lambda self, x: x.name),
        GrpcMethod('get_default_queue_name',
            output_transform=lambda self, x: x.name),
        GrpcMethod(
            'is_open',
            output_transform=lambda self, x: x.value)
        GrpcMethod('close'),

        GrpcMethod('submit_batch_job'),
        GrpcMethod('submit_interactive_job'),
        GrpcMethod('get_queue_status'),
        GrpcMethod('get_queue_statuses')
    ]

    def __init__(self, service, *args):
        super(Scheduler, self).__init__(service, service.create(*args))

    def path(self, *args):
        return Path(self.__service__, xenon_pb2.Path(self.__wrapped__, *args))
