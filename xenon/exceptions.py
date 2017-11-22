import grpc


class XenonException(Exception):
    """Xenon base exception."""
    def __init__(self, method, msg):
        super(XenonException, self).__init__(
            "Xenon: \"{}\" in {}".format(msg, method.name))


def make_exception(method, e):
    """Creates an exception for a given method, and RpcError."""
    if method.name == "create_directory" and \
            e.code() == grpc.StatusCode.ALREADY_EXISTS:
        return PathAlreadyExistsException(method, e.details())

    else:
        return UnknownRpcException(method, e.details())


def exception_factory(name, docstring, BaseClass=XenonException):
    def __init__(self, method, exc_msg):
        BaseClass.__init__(self, method, exc_msg)

    newclass = type(name, (BaseClass,), {"__init__": __init__})
    newclass.__doc__ = docstring

    return newclass


xenon_exceptions = {
    "UnknownRpcException":
        """Default exception if nothing is known.""",
    "AttributeNotSupportedException": None,
    "CopyCancelledException": None,
    "DirectoryNotEmptyException": None,
    "FileSystemClosedException": None,
    "IncompleteJobDescriptionException": None,
    "InvalidCredentialException": None,
    "InvalidJobDescriptionException": None,
    "InvalidLocationException": None,
    "InvalidOptionsException": None,
    "InvalidPathException": None,
    "InvalidPropertyException": None,
    "InvalidResumeTargetException": None,
    "NoSuchCopyException": None,
    "NoSuchJobException": None,
    "NoSuchPathException": None,
    "NoSuchQueueException": None,
    "PathAlreadyExistsException":
        """Exception that is raised if :py:meth:`FileSystem.create_directory`
        fails due to an existing path.""",
    "PropertyTypeException": None,
    "UnknownAdaptorException": None,
    "UnknownPropertyException": None,
    "UnsupportedJobDescriptionException": None,
    "UnsupportedOperationException": None,
    "XenonRuntimeException": None}


for name, docstring in xenon_exceptions.items():
    globals()[name] = exception_factory(name, docstring)
