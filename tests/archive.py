import tarfile
import io


class Archive(object):
    """Easy interface to `tarfile`.

    We use buffered `tar` files to communicate with Docker
    containers. This class provides an easy way to create
    `tar` buffers on the fly, or read from them.

    Methods in this class can be chained JS style."""
    def __init__(self, mode, data=None):
        self.file = io.BytesIO(data)
        self.tar = tarfile.open(mode=mode, fileobj=self.file)

    def add_text_file(self, filename: str, text: str, encoding='utf-8'):
        """Add the contents of `text` to a new entry in the `tar`
        file.

        :return:
            self
        """
        b = text.encode(encoding)
        f = io.BytesIO(b)
        info = tarfile.TarInfo(filename)
        info.size = len(b)
        info.type = tarfile.REGTYPE

        self.tar.addfile(info, fileobj=f)
        return self

    def get_text_file(self, filename: str, encoding='utf-8') -> str:
        """Read the contents of a file in the archive.

        :return:
            contents of file in string.
        """
        return self.tar.extractfile(filename).read().decode(encoding)

    def close(self):
        self.tar.close()
        return self

    @property
    def buffer(self):
        return self.file.getvalue()
