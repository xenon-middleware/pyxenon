from .proto import xenon_pb2
from .server import __server__
from .exceptions import make_exception
import grpc


try:
    from enum import Enum
except ImportError as e:
    use_enum = False

    class Enum(object):
        """Minimal Enum replacement."""
        def __init__(self, name, items):
            for k, v in items:
                setattr(self, k, v)

else:
    use_enum = True

try:
    from inspect import (Signature, Parameter, signature)
except ImportError as e:
    use_signature = False
else:
    use_signature = True


def mirror_enum(parent, name):
    grpc_enum = getattr(parent, name)
    return Enum(name, grpc_enum.items())


def to_camel_case(name):
    return ''.join(w.title() for w in name.split('_'))


def to_lower_camel_case(name):
    words = name.split('_')
    return words[0] + ''.join(w.title() for w in words[1:])


def get_fields(msg_type):
    """Get a list of field names for Grpc message."""
    return list(f.name for f in msg_type.DESCRIPTOR.fields)


def get_field_type(f):
    """Obtain the type name of a GRPC Message field."""
    types = (t[5:] for t in dir(f) if t[:4] == 'TYPE' and
             getattr(f, t) == f.type)
    return next(types)


def get_field_description(f):
    """Get the type description of a GRPC Message field."""
    type_name = get_field_type(f)
    if type_name == 'MESSAGE' and \
            {sf.name for sf in f.message_type.fields} == {'key', 'value'}:
        return 'map<string, string>'
    elif type_name == 'MESSAGE':
        return f.message_type.full_name
    elif type_name == 'ENUM':
        return f.enum_type.full_name
    else:
        return type_name.lower()


def list_attributes(msg_type):
    """List all attributes with type description of a GRPC Message class."""
    return [(f.name, get_field_description(f))
            for f in msg_type.fields]


class GrpcMethod:
    """Data container for a GRPC method.

    :ivar name: underscore style of method name
    :ivar uses_request: wether this method has a request, if this value is
        `True`, the name is generated from `name`, if it is a string the
        contents of this string are used.
    :ivar field_name: name of `self` within the request.
    :ivar input_transform: custom method to generate a request from the
        method's arguments.
    :ivar output_transform: custom method to extract the return value from
        the return value.
    """
    def __init__(self, name, uses_request=False, field_name=None,
                 input_transform=None, output_transform=None,
                 static=False):
        self.name = name
        self.uses_request = uses_request
        self.field_name = field_name
        self.input_transform = input_transform
        self.output_transform = output_transform
        self.static = static

    @property
    def is_simple(self):
        return not self.uses_request and not self.input_transform \
            and not self.static

    @property
    def request_name(self):
        """Generate the name of the request."""
        if self.static and not self.uses_request:
            return 'Empty'

        if not self.uses_request:
            return None

        if isinstance(self.uses_request, str):
            return self.uses_request

        return to_camel_case(self.name) + "Request"

    @property
    def request_type(self):
        """Retrieve the type of the request, by fetching it from
        `xenon.proto.xenon_pb2`."""
        if self.static and not self.uses_request:
            return getattr(xenon_pb2, 'Empty')

        if not self.uses_request:
            return None

        return getattr(xenon_pb2, self.request_name)

    # python 3 only
    @property
    def signature(self):
        """Create a signature for this method, only in Python > 3.4"""
        if not use_signature:
            raise NotImplementedError("Python 3 only.")

        if self.static:
            parameters = \
                (Parameter(name='cls',
                           kind=Parameter.POSITIONAL_ONLY),)

        else:
            parameters = \
                (Parameter(name='self',
                           kind=Parameter.POSITIONAL_ONLY),)

        if self.input_transform:
            return signature(self.input_transform)

        if self.uses_request:
            fields = get_fields(self.request_type)
            if not self.static:
                if self.field_name not in fields:
                    raise NameError("field '{}' not found in {}".format(
                        self.field_name, self.request_name))
                fields.remove(self.field_name)
            parameters += tuple(
                Parameter(name=name, kind=Parameter.POSITIONAL_OR_KEYWORD,
                          default=None)
                for name in fields)

        return Signature(parameters)

    # TODO extend documentation rendered from proto
    def docstring(self, servicer):
        """Generate a doc-string."""
        s = getattr(servicer, to_lower_camel_case(self.name)).__doc__ \
            or "TODO: no docstring in .proto file"

        if self.uses_request:
            s += "\n"
            for field in get_fields(self.request_type):
                if field != self.field_name:
                    type_info = get_field_description(
                        self.request_type.DESCRIPTOR.fields_by_name[field])
                    s += "    :param {}: {}\n".format(field, field)
                    s += "    :type {0}: {1}\n".format(field, type_info)

        return s


def unwrap(arg):
    if hasattr(arg, '__is_proxy__'):
        return arg.__wrapped__
    else:
        return arg


def make_static_request(method, *args, **kwargs):
    """Creates a request from a static method function call."""
    if args and not use_signature:
        raise NotImplementedError("Only keyword arguments allowed in Python2")

    if use_signature:
        new_kwargs = {kw: unwrap(value) for kw, value in kwargs.items()}
        new_args = tuple(unwrap(value) for value in args)
        bound_args = method.signature.bind(
            None, *new_args, **new_kwargs).arguments

        # if we encounter any Enum arguments, replace them with their value
        for k in bound_args:
            if isinstance(bound_args[k], Enum):
                bound_args[k] = bound_args[k].value

        new_kwargs = {kw: v for kw, v in bound_args.items() if kw != 'cls'}

    else:
        new_kwargs = {kw: unwrap(value) for kw, value in kwargs.items()}

    return method.request_type(**new_kwargs)


def make_request(self, method, *args, **kwargs):
    """Creates a request from a method function call."""
    if args and not use_signature:
        raise NotImplementedError("Only keyword arguments allowed in Python2")

    new_kwargs = {kw: unwrap(value) for kw, value in kwargs.items()}

    if use_signature:
        new_args = tuple(unwrap(value) for value in args)
        bound_args = method.signature.bind(
            unwrap(self), *new_args, **new_kwargs).arguments

        # if we encounter any Enum arguments, replace them with their value
        def translate_enum(arg):
            return arg.value if isinstance(arg, Enum) else arg

        for k in bound_args:
            if isinstance(bound_args[k], str):
                continue
            if isinstance(bound_args[k], dict):
                continue

            try:
                x = [translate_enum(arg) for arg in bound_args[k]]
                bound_args[k] = x
            except TypeError:
                bound_args[k] = translate_enum(bound_args[k])

        # replace `self` with the correct keyword
        new_kwargs = {(kw if kw != 'self' else method.field_name): v
                      for kw, v in bound_args.items()}
        # args = tuple(x.value if isinstance(x, Enum) else x for x in args)

    else:
        new_kwargs[self.field_name] = unwrap(self)

    return method.request_type(**new_kwargs)


def apply_transform(service, t, x):
    """Apply a transformation using `self` as object reference."""
    if t is None:
        return x
    else:
        return t(service, x)


def transform_map(f):
    def t(self, xs):
        return (f(self, x) for x in xs)

    return t


def grpc_call(service, method, request):
    f = getattr(service, to_lower_camel_case(method.name))
    try:
        result = f(request)
    except grpc.RpcError as e:
        raise make_exception(method, e) from None

    return result


def method_wrapper(m):
    """Generates a method from a `GrpcMethod` definition."""

    if m.is_simple:
        def simple_method(self):
            """TODO: no docstring!"""
            return apply_transform(
                self.__service__, m.output_transform,
                grpc_call(self.__service__, m, unwrap(self)))

        return simple_method

    elif m.input_transform is not None:
        def transform_method(self, *args, **kwargs):
            """TODO: no docstring!"""
            request = m.input_transform(self, *args, **kwargs)
            return apply_transform(
                self.__service__, m.output_transform,
                grpc_call(self.__service__, m, request))

        return transform_method

    elif m.static:
        def static_method(cls, *args, **kwargs):
            """TODO: no docstring!"""
            request = make_static_request(m, *args, **kwargs)
            return apply_transform(
                cls.__stub__(__server__), m.output_transform,
                grpc_call(cls.__stub__(__server__), m, request))

        return static_method

    else:
        def request_method(self, *args, **kwargs):
            """TODO: no docstring!"""
            request = make_request(self, m, *args, **kwargs)
            return apply_transform(
                self.__service__, m.output_transform,
                grpc_call(self.__service__, m, request))

        return request_method


class OopMeta(type):
    """Meta class for Grpc Object wrappers."""
    def __new__(cls, name, parents, dct):
        return super(OopMeta, cls).__new__(cls, name, parents, dct)

    def __init__(cls, name, parents, dct):
        super(OopMeta, cls).__init__(name, parents, dct)

        for m in cls.__methods__():
            if m.uses_request and not m.field_name:
                m.field_name = cls.__field_name__

            f = method_wrapper(m)
            if use_signature:
                f.__signature__ = m.signature

            if cls.__servicer__:
                f.__doc__ = m.docstring(cls.__servicer__)

            f.__name__ = m.name

            if m.static:
                setattr(cls, m.name, classmethod(f))
            else:
                setattr(cls, m.name, f)

        try:
            grpc_cls = getattr(xenon_pb2, name)
            if cls.__doc__ is None:
                cls.__doc__ = "Wrapped proto message."
            cls.__doc__ += "\n\n"
            for attr in list_attributes(grpc_cls.DESCRIPTOR):
                cls.__doc__ += \
                    "    :ivar {0}: {0}\n    :vartype {0}: {1}\n".format(*attr)

        except AttributeError:
            pass


class OopProxy(metaclass=OopMeta):
    """Base class for Grpc Object wrappers. Ensures basic object sanity,
    namely the existence of `__service__` and `__wrapped__` members and
    the using of `OopMeta` meta-class. Also manages retrieving attributes
    from the wrapped instance.

    :ivar __is_proxy__: If True, this value represents a wrapped value,
        from which the GRPC message can be extraced by getting the
        `__wrapped__` attribute.
    :ivar __servicer__: If applicable, this gives the GRPC servicer class
        associated with the proxy object; this is used to retrieve doc-strings.
    :ivar __field_name__: The default name to which an object of this class
        should be bound in a request. This can be overridden by specifying
        the `field_name` property in the `GRPCMethod` definition. For a
        well-designed API this should not be necessary though.
    """

    __is_proxy__ = True
    __servicer__ = None
    __field_name__ = None

    @classmethod
    def __methods__(cls):
        """This method should return a list of GRPCMethod objects."""
        return []

    def __init__(self, service, wrapped):
        self.__service__ = service
        self.__wrapped__ = wrapped

    @staticmethod
    def __stub__(server):
        """Return the GRPC stub class to which this object interfaces."""
        raise NotImplementedError()

    def __getattr__(self, attr):
        """Accesses fields of the corresponding GRPC message."""
        return getattr(self.__wrapped__, attr)

    def _repr_html_(self):
        members = [f.name for f in self.__wrapped__.DESCRIPTOR.fields]
        s = type(self).__name__ + ": <ul>"
        for m in members:
            s += "<li><b>{}:</b> {}".format(m, getattr(self, m))
            if m not in dir(self.__wrapped__):
                s += " <i>(default)</i>"
            s += "</li>"
        s += "</ul>"
        return s

    def __str__(self):
        members = [f.name for f in self.__wrapped__.DESCRIPTOR.fields]
        s = type(self).__name__ + ":\n"
        for m in members:
            s += "    {}: {}".format(m, getattr(self, m))
            if m not in dir(self.__wrapped__):
                s += " (default)"
            s += "\n"
        return s

    def __dir__(self):
        members = [f.name for f in self.__wrapped__.DESCRIPTOR.fields]
        return dir(super(OopProxy, self)) + members
