import pytest
import xenon


@pytest.fixture(scope='session', autouse=True)
def make_init():
    """
    Initialize Xenon.

    After first call, this is a no-op, since jpype cannot be reinitialized.
    """
    # Override log_level to get more details on the internals, e.g. 'DEBUG'
    assert xenon.jobs.JobDescription is None
    xenon.init()
    assert xenon.jobs.JobDescription is not None
