"""
GRPC server connection.
"""

import atexit
import logging
import socket
import threading
import time

from pathlib import Path
from contextlib import closing

import grpc
from xdg import BaseDirectory

from .proto import (xenon_pb2_grpc)
from .compat import (start_xenon_server, kill_process)


def check_socket(host, port):
    """Checks if port is open on host. This is used to check if the
    Xenon-GRPC server is running."""
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        return sock.connect_ex((host, port)) == 0


def get_secure_channel(port=50051):
    """Try to connect over a secure channel."""
    config_dir = Path(BaseDirectory.xdg_config_home) / 'xenon-grpc'
    crt_file = config_dir / 'server.crt'
    key_file = config_dir / 'server.key'

    creds = grpc.ssl_channel_credentials(
        root_certificates=open(str(crt_file), 'rb').read(),
        private_key=open(str(key_file), 'rb').read(),
        certificate_chain=open(str(crt_file), 'rb').read())

    address = "{}:{}".format(socket.gethostname(), port)
    channel = grpc.secure_channel(address, creds)
    return channel


def find_free_port():
    """Finds a free port."""
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        sock.bind(('', 0))
        return sock.getsockname()[1]


def print_stream(file, name):
    """Print stream from file to logger."""
    logger = logging.getLogger('xenon.{}'.format(name))
    for line in file:
        logger.info('[{}] {}'.format(name, line.strip()))


class Server(object):
    """Xenon Server. This tries to find a running Xenon-GRPC server,
    or start one if not found. This implementation may only work on Unix.
    """
    def __init__(self, port=50051, disable_tls=False):
        self.port = port
        self.process = None
        self.channel = None
        self.threads = []
        self.disable_tls = disable_tls

        # Xenon proxies
        self.scheduler_stub = None
        self.file_system_stub = None

    def __enter__(self):
        logger = logging.getLogger('xenon')

        if check_socket(socket.gethostname(), self.port):
            logger.info('Xenon-GRPC servers seems to be running.')
        else:
            logger.info('Starting Xenon-GRPC server.')
            self.process = start_xenon_server(self.port, self.disable_tls)

            for name, output in [('out', self.process.stdout),
                                 ('err', self.process.stderr)]:
                thread = threading.Thread(
                    target=print_stream,
                    args=(output, name),
                    daemon=True)
                thread.start()

            for _ in range(50):
                if check_socket(socket.gethostname(), self.port):
                    break
                time.sleep(0.1)
            else:
                raise RuntimeError("GRPC started, but still can't connect.")

        logger.info('Connecting to server')
        if self.disable_tls:
            self.channel = grpc.insecure_channel(
                '{}:{}'.format(socket.gethostname(), self.port))
        else:
            self.channel = get_secure_channel(self.port)

        self.file_system_stub = \
            xenon_pb2_grpc.FileSystemServiceStub(self.channel)
        self.scheduler_stub = \
            xenon_pb2_grpc.SchedulerServiceStub(self.channel)
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        if self.process:
            kill_process(self.process)

        self.process = None


__server__ = Server()


def init(port=None, do_not_exit=False, disable_tls=False, log_level='WARNING'):
    """Start the Xenon GRPC server on the specified port, or, if a service
    is already running on that port, connect to that.

    If no port is given, a random port is selected. This means that, by
    default, every python instance will start its own instance of a xenon-grpc
    process.

    :param port: the port number
    :param do_not_exit: by default the GRPC server is shut down after Python
        exits (through the `atexit` module), setting this value to `True` will
        prevent that from happening."""
    logger = logging.getLogger('xenon')
    logger.setLevel(logging.INFO)

    logger_handler = logging.StreamHandler()
    logger_handler.setFormatter(logging.Formatter(style='{'))
    logger_handler.setLevel(getattr(logging, log_level))
    logger.addHandler(logger_handler)

    if port is None:
        port = find_free_port()

    if __server__.process is not None:
        logger.warning(
            "You tried to run init(), but the server is already running.")
        return __server__

    __server__.port = port
    __server__.disable_tls = disable_tls
    __server__.__enter__()

    if not do_not_exit:
        atexit.register(__server__.__exit__, None, None, None)

    return __server__
