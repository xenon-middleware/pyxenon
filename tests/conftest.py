import pytest
import xenon


@pytest.fixture(scope='session', autouse=True)
def make_init():
    """
    Initialize Xenon.

    After first call, this is a no-op, since jpype cannot be reinitialized.
    """
    # cannot initialize Java classes now
    with pytest.raises(EnvironmentError):
        xenon.JavaClass('java.util.Arrays').asList([])
    # Override log_level to get more details on the internals, e.g. 'DEBUG'
    xenon.init()
    # can initialize Java classes now
    xenon.JavaClass('java.util.Arrays').asList([])
