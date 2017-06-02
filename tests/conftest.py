import pytest
from xenon import Xenon


@pytest.fixture(scope="module")
def xenon(request):
    m = Xenon()
    request.addfinalizer(lambda: m.__exit__(None, None, None))
    return m.__enter__()
