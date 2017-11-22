import grpc


class XenonException(Exception):
    """Xenon base exception."""
    def __init__(self, method, msg):
        super(XenonException, self).__init__(
            "Xenon: \"{}\" in {}".format(msg, method.name))


class UnknownRpcError(XenonException):
    """Default exception if nothing is known."""
    def __init__(self, method, e):
        super(UnknownRpcError, self).__init__(
            method,
            "unknown exception \"{}\"".format(e))


class PathAlreadyExistsException(XenonException):
    """Exception that is raised if :py:meth:`FileSystem.create_directory`
    fails due to an existing path."""
    def __init__(self, method, e):
        super(PathAlreadyExistsException, self).__init__(
            method,
            e.details())


def make_exception(method, e):
    """Creates an exception for a given method, and RpcError."""
    if method.name == "create_directory" and \
            e.code() == grpc.StatusCode.ALREADY_EXISTS:
        return PathAlreadyExistsException(method, e)
