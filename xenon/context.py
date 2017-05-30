from .proto import (xenon_pb2_grpc)
import grpc
import socket
import logging
import subprocess
import threading

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


def log_stream(file, name):
    logger = logging.getLogger('xenon.{}'.format(name))
    for line in file:
        logger.info("{}: {}".format(name, line.decode().strip()))


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
            self.process = subprocess.Popen(
                    ['xenon-grpc'],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE)

            stdout_thread = threading.Thread(
                target=log_stream, args=(self.process.stdout, 'stdout'))
            stdout_thread.start()
            self.threads.append(stdout_thread)

            stderr_thread = threading.Thread(
                target=log_stream, args=(self.process.stderr, 'stderr'))
            stderr_thread.start()
            self.threads.append(stderr_thread)

        logger.info('Connecting to server')
        self.channel = grpc.insecure_channel('localhost:{}'.format(self.port))
        self.files = xenon_pb2_grpc.XenonFilesStub(self.channel)
        self.jobs = xenon_pb2_grpc.XenonJobsStub(self.channel)

        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        if self.process:
            logger.info('Terminating Xenon-GRPC server.')
            self.process.terminate()
            try:
                self.process.wait(1)
            except subprocess.TimeoutExpired:
                logger.warning(
                    'Xenon-GRPC server is not terminating, killing it.')
                self.process.kill()

                try:
                    self.process.wait(1)
                except subprocess.TimeoutExpired:
                    logger.error('Could not kill server.')

        for t in self.threads:
            t.join()
