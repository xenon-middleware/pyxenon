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
        return PathAlreadyExistsException(method, e.details())  # noqa

    else:
        return UnknownRpcException(method, e.details())  # noqa


def exception_factory(name, docstring, BaseClass=XenonException):
    def __init__(self, method, exc_msg):
        BaseClass.__init__(self, method, exc_msg)

    newclass = type(name, (BaseClass,), {"__init__": __init__})
    newclass.__doc__ = docstring

    return newclass


xenon_exceptions = {
    "UnknownRpcException":
        """Default exception if nothing is known.""",
    "AttributeNotSupportedException":
        """TODO: add doc-string.""",
    "CopyCancelledException":
        """TODO: add doc-string.""",
    "DirectoryNotEmptyException":
        """TODO: add doc-string.""",
    "FileSystemClosedException":
        """TODO: add doc-string.""",
    "IncompleteJobDescriptionException":
        """TODO: add doc-string.""",
    "InvalidCredentialException":
        """TODO: add doc-string.""",
    "InvalidJobDescriptionException":
        """TODO: add doc-string.""",
    "InvalidLocationException":
        """TODO: add doc-string.""",
    "InvalidOptionsException":
        """TODO: add doc-string.""",
    "InvalidPathException":
        """TODO: add doc-string.""",
    "InvalidPropertyException":
        """TODO: add doc-string.""",
    "InvalidResumeTargetException":
        """TODO: add doc-string.""",
    "NoSuchCopyException":
        """TODO: add doc-string.""",
    "NoSuchJobException":
        """TODO: add doc-string.""",
    "NoSuchPathException":
        """TODO: add doc-string.""",
    "NoSuchQueueException":
        """TODO: add doc-string.""",
    "PathAlreadyExistsException":
        """Exception that is raised if :py:meth:`FileSystem.create_directory`
        fails due to an existing path.""",
    "PropertyTypeException":
        """TODO: add doc-string.""",
    "UnknownAdaptorException":
        """TODO: add doc-string.""",
    "UnknownPropertyException":
        """TODO: add doc-string.""",
    "UnsupportedJobDescriptionException":
        """TODO: add doc-string.""",
    "UnsupportedOperationException":
        """TODO: add doc-string.""",
    "XenonRuntimeException":
        """TODO: add doc-string."""}


for name, docstring in xenon_exceptions.items():
    globals()[name] = exception_factory(name, docstring)
