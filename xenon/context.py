from .proto import (xenon_pb2_grpc, xenon_pb2)

import grpc
import socket
import fcntl
import logging
import subprocess
import signal
import threading
import os

from contextlib import closing

logger = logging.getLogger('xenon')
logger.setLevel(logging.INFO)

logger_handler = logging.StreamHandler()
logger_handler.setLevel(logging.INFO)

logger.addHandler(logger_handler)


def check_socket(host, port):
    """Checks if port is open on host."""
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        return sock.connect_ex((host, port)) == 0


def split_path(path):
    def do_split(p):
        while True:
            p, q = os.path.split(p)
            if q == '':
                return
            yield q

    return list(do_split(path))[::-1]


def find_xenon_grpc_jar():
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
            './lib/xenon-grpc-0.0.1-all.jar'))
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
        # ''.join(word.title() for word in method.split('_'))

    def __call__(self, *args, **kwargs):
        return getattr(xenon_pb2, self._method)(*args, **kwargs)


class Xenon(object):
    """Xenon Context Manager. This tries to find a running Xenon-GRPC server,
    or start one if not found. This implementation only works on Unix.
    """
    def __init__(self, port=50051):
        self.port = port
        self.process = None
        self.channel = None
        self.threads = []

        # Xenon proxies
        self.files = None
        self.jobs = None

    def __getattr__(self, attr):
        if attr in dir(self) or attr[0] == '_':
            return getattr(super(Xenon, self), attr)

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

        logger.info('Connecting to server')
        self.channel = grpc.insecure_channel('localhost:{}'.format(self.port))

        self.files = xenon_pb2_grpc.XenonFilesStub(self.channel)
        self.jobs = xenon_pb2_grpc.XenonJobsStub(self.channel)

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
