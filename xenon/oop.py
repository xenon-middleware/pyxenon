from .proto import xenon_pb2

try:
    from inspect import (Signature, Parameter)
except ImportError as e:
    use_signature = False
else:
    use_signature = True


def to_camel_case(name):
    return ''.join(w.title() for w in name.split('_'))


def to_lower_camel_case(name):
    words = name.split('_')
    return words[0] + ''.join(w.title() for w in words[1:])


def get_fields(msg_type):
    """Get a list of field names for Grpc message."""
    return list(f.name for f in msg_type.DESCRIPTOR.fields)


class GrpcMethod:
    def __init__(self, name, uses_request=False, field_name=None,
                 input_transform=None, output_transform=None):
        self.name = name
        self.uses_request = uses_request
        self.field_name = field_name
        self.input_transform = input_transform
        self.output_transform = output_transform

    @property
    def is_simple(self):
        return not self.uses_request

    @property
    def request_name(self):
        if self.uses_request is None:
            return None

        if isinstance(self.uses_request, str):
            return self.uses_request

        return to_camel_case(self.name) + "Request"

    @property
    def request_type(self):
        return getattr(xenon_pb2, self.request_name)

    # python 3 only
    @property
    def signature(self):
        if not use_signature:
            raise NotImplementedError("Python 3 only.")

        parameters = \
            (Parameter(name='self', kind=Parameter.POSITIONAL_ONLY),)

        if self.uses_request:
            fields = get_fields(self.request_type)
            assert self.field_name in fields
            fields.remove(self.field_name)
            parameters += tuple(
                Parameter(name=name, kind=Parameter.POSITIONAL_OR_KEYWORD,
                          default=None)
                for name in fields)

        return Signature(parameters)

    # TODO extend documentation rendered from proto
    def docstring(self, servicer):
        s = getattr(servicer, to_lower_camel_case(self.name)).__doc__
        s += "\n"
        for field in get_fields(self.request_type):
            if field != self.field_name:
                s += "    :param {}: {}\n".format(field, field)
        return s


def unwrap(arg):
    if hasattr(arg, '__is_proxy__'):
        return arg.__wrapped__
    else:
        return arg


def make_request(self, method, *args, **kwargs):
    if args and not use_signature:
        raise NotImplementedError("Only keyword arguments allowed in Python2")

    new_kwargs = {kw: unwrap(value) for kw, value in kwargs.items()}

    if use_signature:
        new_args = tuple(unwrap(value) for value in args)
        bound_args = method.signature.bind(
                unwrap(self), *new_args, **new_kwargs)
        new_kwargs = {(kw if kw != 'self' else method.field_name): v
                      for kw, v in bound_args.arguments.items()}
    else:
        new_kwargs[self.field_name] = unwrap(self)

    return getattr(xenon_pb2, method.request_name)(**new_kwargs)


def apply_transform(self, t, x):
    """Apply a transformation using `self` as object reference."""
    if t is None:
        return x
    else:
        return t(self.__service__, x)


def transform_map(f):
    def t(self, xs):
        return (f(self, x) for x in xs)

    return t


def method_wrapper(m):
    """Generates a method from a `GrpcMethod` definition."""

    def simple_method(self):
        f = getattr(self.__service__, to_lower_camel_case(m.name))
        return apply_transform(self, m.output_transform, f(unwrap(self)))

    if m.is_simple:
        return simple_method

    def request_method(self, *args, **kwargs):
        f = getattr(self.__service__, to_lower_camel_case(m.name))
        request = make_request(self, m, *args, **kwargs)
        return apply_transform(self, m.output_transform, f(request))

    return request_method


class OopMeta(type):
    """Meta class for Grpc Object wrappers."""
    def __new__(cls, name, parents, dct):
        print("initializing type {}".format(name))
        return super(OopMeta, cls).__new__(cls, name, parents, dct)

    def __init__(cls, name, parents, dct):
        super(OopMeta, cls).__init__(name, parents, dct)

        for m in cls.__methods__():
            print("defining {} in class {}".format(m.name, name))
            f = method_wrapper(m)
            if use_signature:
                f.__signature__ = m.signature
            setattr(cls, m.name, f)


class OopProxy(metaclass=OopMeta):
    """Base class for Grpc Object wrappers. Ensures basic object sanity,
    namely the existence of `__service__` and `__wrapped__` members and
    the using of `OopMeta` meta-class. Also manages retrieving attributes
    from the wrapped instance."""

    __is_proxy__ = True

    @classmethod
    def __methods__(cls):
        return []

    def __init__(self, service, wrapped):
        self.__service__ = service
        self.__wrapped__ = wrapped

    def __getattr__(self, attr):
        return getattr(self.__wrapped__, attr)


class PathAttributes(OopProxy):
    def __init__(self, service, wrapped):
        super(PathAttributes, self).__init__(service, wrapped)
        self.path = Path(service, wrapped.path)


class Path(OopProxy):
    @classmethod
    def __methods__(cls):
        return [
            GrpcMethod('create_directories'),
            GrpcMethod('create_directory'),
            GrpcMethod('create_file'),
            GrpcMethod(
                'exists',
                output_transform=lambda self, x: x.value),
            GrpcMethod('read_from_file'),  # TODO stream response
            GrpcMethod(
                'get_attributes',
                output_transform=PathAttributes),
            GrpcMethod('set_working_directory'),
            GrpcMethod(
                'read_symbolic_link',
                output_transform=cls),
            GrpcMethod(
                'delete', uses_request=True, field_name='path'),
            GrpcMethod(
                'copy', uses_request=True, field_name='source'),
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

    def append_to_file(self, data_stream):
        def append_request_stream():
            yield xenon_pb2.AppendToFileRequest(path=self.__wrapped__)
            yield from (xenon_pb2.AppendToFileRequest(buffer=b)
                        for b in data_stream)

        return self.__service__.appendToFile(append_request_stream())


class FileSystem(OopProxy):
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
            GrpcMethod('close')
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


class Scheduler(OopProxy):
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
            # GrpcMethod(  # TODO handle streams
            #     'submit_interactive_job',
            #     output_transform=lambda self, x: x.id),
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

    def submit_interactive_job(self, description, stdin_stream):
        def input_request_stream():
            yield xenon_pb2.SubmitInteractiveJobRequest(
                scheduler=unwrap(self), description=description, stdin=b'')
            yield from (xenon_pb2.SubmitInteractiveJobRequest(
                scheduler=None, description=None, stdin=msg)
                for msg in stdin_stream)

        return self.__service__.submitInteractiveJob(input_request_stream())

    def __init__(self, service, wrapped):
        super(Scheduler, self).__init__(service, wrapped)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.close()
