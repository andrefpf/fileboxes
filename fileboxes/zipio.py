# from io import IOBase, BytesIO
import io
from pathlib import Path
from zipfile import ZipFile


class ZipIO(io.IOBase):
    def __init__(self, path: str | Path, arcname: str, mode: str = "r") -> None:
        self.path = path
        self.arcname = arcname
        self.mode = mode
        self._zip = ZipFile(path, mode)
        self._file = self._zip.open(arcname, mode)

    def close(self):
        super().close()
        self._file.close()
        self._zip.close()
    
    def write(self, buffer: str | bytes) -> int:
        if isinstance(buffer, str):
            buffer = buffer.encode()
        return self._file.write(buffer)

    def read(self, size: int | None = None):
        return self._file.read(size)

    def readline(self) -> None:
        return self._file.readline()

    def flush(self) -> None:
        return self._file.flush()
    
    def readable(self) -> None:
        return self._file.readable()
    
    def writable(self) -> bool:
        return self._file.writable()
    
    def seekable(self) -> None:
        return self._file.seekable()
    
    def seek(self, offset, whence=0) -> None:
        return
    
    def tell(self) -> int:
        return 0

    def truncate(self, size: int | None = ...) -> int:
        return 0
