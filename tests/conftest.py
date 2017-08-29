import pytest
import xenon
from easy_docker import DockerContainer
import time


@pytest.fixture(scope="session")
def slurm_container(request):
    m = DockerContainer(
        image='nlesc/xenon-slurm:17',
        ports={22: 10022})

    def stop():
        m.kill()
        m.remove(force=True)

    request.addfinalizer(stop)
    m.start()
    time.sleep(5)

    return m


@pytest.fixture(scope="session")
def xenon_server(request):
    m = xenon.Server()
    request.addfinalizer(lambda: m.__exit__(None, None, None))
    return m.__enter__()
