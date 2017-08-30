import docker
import os

from archive import Archive


class DockerContainer(object):
    """Easy interface to Docker API.

    This class encapsulates a part of the Docker API, with the goal
    of making it easier to start a container, add some files, run a
    few scripts, read the output, and then remove the container
    again.

    The object is a context manager for the created Docker container,
    in that it starts the container upon entry and exterminates the
    same container upon exit.
    """

    client = docker.from_env()
    containers = client.containers

    def __init__(self, image, working_dir=None, **kwargs):
        self.image = image
        self.working_dir = working_dir

        self.container = self.client.containers.create(
            image=image, detach=True, stdin_open=True,
            working_dir=working_dir, **kwargs)

    def put_archive(self, archive, path="."):
        """Put the contents of an archive into the Docker container.

        :param archive:
            The `Archive` instance that contains the files that need
            to be injected.
        :type archive: Archive

        :param path:
            Where to extract the archive within the container.
        :type path: str
        """
        if self.working_dir is not None:
            path = os.path.join(self.working_dir, path)

        self.container.put_archive(
            path, archive.buffer)

    def get_archive(self, path):
        """Get a file or directory from the container and make it into
        an `Archive` object."""
        if self.working_dir is not None and not os.path.isabs(path):
            path = os.path.join(self.working_dir, path)

        strm, stat = self.container.get_archive(path)

        return Archive('r', strm.read())

    def run(self, cmd, **kwargs):
        """Run a command.

        :param cmd:
            Command to be run and arguments as a list.
        :type cmd: List[str]

        :param kwargs:
            Forwarded to Docker-py `exec_create` function call.

        :return:
            Output of command.
        :rtype: bytes
        """
        return self.container.exec_run(
            cmd=cmd, **kwargs)

    def start(self):
        self.container.start()

    def kill(self):
        self.container.kill()

    def remove(self, force=False):
        self.container.remove(force=force)

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_value, exc_st):
        self.kill()
        self.remove()
