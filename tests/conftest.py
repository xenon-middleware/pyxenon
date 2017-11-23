import pytest
import xenon


@pytest.fixture(scope="session")
def xenon_server(request):
    print("============== Starting Xenon-GRPC server ================")
    m = xenon.init(do_not_exit=True, disable_tls=False, log_level='INFO')
    request.addfinalizer(lambda: m.__exit__(None, None, None))


@pytest.fixture
def local_fs(request, xenon_server):
    fs = xenon.FileSystem.create(adaptor='file')
    yield fs
    fs.close()
