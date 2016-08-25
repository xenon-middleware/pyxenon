import pytest
import xenon
import jpype


@pytest.fixture(scope='session', autouse=True)
def make_init():
    """
    Initialize Xenon.

    After first call, this is a no-op, since jpype cannot be reinitialized.
    """
    # Override log_level to get more details on the internals, e.g. 'DEBUG'
    assert xenon.JavaClass.JClassClass is None
    assert xenon.JavaPackage.JPackageClass is None
    xenon.init()
    assert xenon.JavaClass.JClassClass == jpype.JClass
    assert xenon.JavaPackage.JPackageClass == jpype.JPackage
