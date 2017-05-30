from .proto import (xenon_pb2_grpc)
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


def start_xenon_server():
    process = subprocess.Popen(
        ['xenon-grpc'],
        bufsize=1,
        shell=True,
        universal_newlines=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        preexec_fn=os.setsid)
    return process


def print_streams(process, event):
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


class Xenon:
    def __init__(self, port=50051):
        self.port = port
        self.process = None
        self.channel = None
        self.threads = []

        # Xenon proxies
        self.files = None
        self.jobs = None
        self.credentials = None

    def __enter__(self):
        if check_socket('localhost', self.port):
            logger.info('Xenon-GRPC servers seems to be running.')
        else:
            logger.info('Starting Xenon-GRPC server.')
            self.process = start_xenon_server()
            e = threading.Event()
            t = threading.Thread(
                target=print_streams,
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
            os.killpg(os.getpgid(self.process.pid), signal.SIGINT)
            self.process.wait()

        for (t, e) in self.threads:
            e.set()
            t.join()
