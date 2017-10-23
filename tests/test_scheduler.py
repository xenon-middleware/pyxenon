from xenon import Scheduler, FileSystem


def test_get_file_system(xenon_server, tmpdir):
    with Scheduler.create(adaptor='local') as scheduler:
        filesystem = scheduler.get_file_system()
        assert isinstance(filesystem, FileSystem)
        assert filesystem.get_adaptor_name() == 'file'
