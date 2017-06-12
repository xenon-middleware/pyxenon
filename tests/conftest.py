import pytest
import xenon


@pytest.fixture(scope="session")
def xenon_server(request):
    m = xenon.Server()
    request.addfinalizer(lambda: m.__exit__(None, None, None))
    return m.__enter__()
