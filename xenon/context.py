from .proto import (xenon_pb2_grpc, xenon_pb2)

import grpc
import socket
import fcntl
import logging
import subprocess
import signal
import threading
import os
import time

from contextlib import closing

logger = logging.getLogger('xenon')
logger.setLevel(logging.INFO)

logger_handler = logging.StreamHandler()
logger_handler.setLevel(logging.INFO)

logger.addHandler(logger_handler)


def check_socket(host, port):
    """Checks if port is open on host. This is used to check if the
    Xenon-GRPC server is running."""
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        return sock.connect_ex((host, port)) == 0


def split_path(path):
    """Split a path into a list of directories."""
    def do_split(p):
        while True:
            p, q = os.path.split(p)
            if q == '':
                return
            yield q

    return list(do_split(path))[::-1]


def find_xenon_grpc_jar():
    """Find the Xenon-GRPC jar file. This first looks for the `xenon-grpc`
    shell script by running `which xenon-grcp` and then takes the relative
    path `../lib/xenon-grpc-0.0.1-all.jar` from there.

    TODO: install xenon-grpc jar-file in the Python distribution."""
    logger = logging.getLogger('xenon')
    which_xenon = subprocess.run(
            ['which', 'xenon-grpc'],
            universal_newlines=True,
            stdout=subprocess.PIPE)
    if which_xenon.returncode != 0:
        return None

    xenon_prefix = os.path.join('/', *split_path(which_xenon.stdout)[:-2])
    xenon_jar_path = os.path.abspath(os.path.join(
            xenon_prefix,
            './lib/xenon-grpc-1.0.0-all.jar'))
    logger.info("Found Xenon-GRPC at: {}".format(xenon_jar_path))
    return xenon_jar_path


def start_xenon_server():
    jar_file = find_xenon_grpc_jar()
    if not jar_file:
        raise RuntimeError("Could not find 'xenon-grpc' jar file.")

    process = subprocess.Popen(
        ['java', '-jar', jar_file],
        bufsize=1,
        universal_newlines=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        preexec_fn=os.setsid)
    return process


def to_camel_case(n):
    words = n.split('_')
    return words[0] + ''.join([w.title() for w in words[1:]])


def print_stream(file, name):
    logger = logging.getLogger('xenon.{}'.format(name))
    for line in file:
        logger.info('[{}] {}'.format(name, line.strip()))


def print_streams_posix(process, event):
    """Reads stdout and stderr of process by settings both files
    in non-blocking mode, and polling every 0.1 seconds. The loop
    is broken by setting the event. Only works on POSIX (linux) systems."""
    def set_nonblocking(file):
        fd = file.fileno()
        fl = fcntl.fcntl(fd, fcntl.F_GETFL)
        fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)

    def forward_lines(file, name):
        logger = logging.getLogger('xenon.{}'.format(name))

        line = ''
        while True:
            try:
                char = file.read(1)
                if char == '':
                    break
                if char == '\n':
                    logger.info('{} {}'.format(name, line))
                    line = ''
                else:
                    line += char

            except:
                pass

    set_nonblocking(process.stdout)
    set_nonblocking(process.stderr)

    while not event.is_set():
        event.wait(0.1)
        forward_lines(process.stdout, '[out]')
        forward_lines(process.stderr, '[err]')


class GRPCProxy:
    def __init__(self, method):
        self._method = method
        # self._method = to_camel_case(method)

    def __call__(self, *args, **kwargs):
        return getattr(xenon_pb2, self._method)(*args, **kwargs)

    def __getattr__(self, attr):
        return getattr(getattr(xenon_pb2, self._method), attr)


def request_wrapper(stub, name, request_name = None):
    request_name = request_name or "{first}{rest}Request" \
        .format(first=name[0].upper(), rest=name[1:])

    def send_request(**kwargs):
        request = getattr(xenon_pb2, request_name)(**kwargs)
        return getattr(stub, name)(request)

    return send_request


class ProxyBase(object):
    def __init__(self, stub, object_name, wrappers):
        self.stub = stub
        self.wrappers = wrappers
        self.object_name = object_name

    def __getattr__(self, attr):
        if attr in dir(self) or attr[0] == '_':
            return getattr(super(ProxyBase, self), attr)

        # translate to camelCase
        if '_' in attr:
            attr = to_camel_case(attr)

        # create method is special
        if attr == 'create':
            request_name = "Create{}Request".format(self.object_name)
            return request_wrapper(self.stub, attr, request_name)

        if attr in self.wrappers:
            return request_wrapper(self.stub, attr)

        return getattr(self.stub, attr)


class SchedulersProxy(ProxyBase):
    def __init__(self, channel):
        super(SchedulersProxy, self).__init__(
            xenon_pb2_grpc.XenonSchedulersStub(channel),
            'Scheduler',
            ['submitBatchJob'])

    def submit_interactive_job(self, scheduler, description, stdin_stream):
        def input_request_stream():
            yield xenon_pb2.SubmitInteractiveJobRequest(
                scheduler=scheduler, description=description, stdin=b'')
            yield from (xenon_pb2.SubmitInteractiveJobRequest(
                scheduler=scheduler, description=description, stdin=msg)
                for msg in stdin_stream)

        return self.stub.submitInteractiveJob(input_request_stream())


class FileSystemsProxy(ProxyBase):
    def __init__(self, channel):
        super(FileSystemsProxy, self).__init__(
            xenon_pb2_grpc.XenonFileSystemsStub(channel),
            'FileSystem',
            ['createSymbolicLink', 'copy', 'rename', 'delete',
             'list', 'setPosixFilePermissions'])


class Server(object):
    """Xenon Server. This tries to find a running Xenon-GRPC server,
    or start one if not found. This implementation only works on Unix.

    As an added feature, all messages defined in the protocol are grafted
    onto this class. This allows the user to access all of Xenon through
    an instance of the Xenon Server object.
    """
    def __init__(self, port=50051):
        self.port = port
        self.process = None
        self.channel = None
        self.threads = []

        # Xenon proxies
        self.schedulers = None
        self.file_systems = None

    def __getattr__(self, attr):
        if attr in dir(self) or attr[0] == '_':
            return getattr(super(Server, self), attr)

        return GRPCProxy(attr)

    def __enter__(self):
        if check_socket('localhost', self.port):
            logger.info('Xenon-GRPC servers seems to be running.')
        else:
            logger.info('Starting Xenon-GRPC server.')
            self.process = start_xenon_server()
            e = threading.Event()
            t = threading.Thread(
                target=print_streams_posix,
                args=(self.process, e))
            t.start()
            self.threads.append((t, e))

        while not check_socket('localhost', self.port):
            time.sleep(0.1)

        logger.info('Connecting to server')
        self.channel = grpc.insecure_channel('localhost:{}'.format(self.port))

        self.file_systems = FileSystemsProxy(self.channel)
        self.schedulers = SchedulersProxy(self.channel)

        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        if self.process:
            logger.info('Terminating Xenon-GRPC server.')
            os.kill(self.process.pid, signal.SIGINT)
            # os.killpg(os.getpgid(self.process.pid), signal.SIGINT)
            self.process.wait()

        for (t, e) in self.threads:
            e.set()
            t.join()
