# from io import IOBase, BytesIO
import io
from pathlib import Path
from zipfile import ZipFile


class ZipIO(io.BytesIO):
    def __init__(self, path: str | Path, arcname: str, mode: str = "r") -> None:
        super().__init__()

        self.path = Path(path)
        self.arcname = arcname
        self.mode = mode

        # The data need to be copied from zip on reads and appends
        # In a write case we would just need a
        if self.mode in ["r", "a"]:
            self._copy_data_from_zip()

    def close(self):
        if self.mode in ["w", "a"]:
            self._copy_data_to_zip()
        super().close()

    def delete_if_exists(self):
        if not self.path.exists():
            return

        buffer = dict()
        with ZipFile(self.path, "r") as zip:
            if self.arcname not in zip.namelist():
                return
            for name in zip.namelist():
                if name != self.arcname:
                    buffer[name] = zip.read(name)

        with ZipFile(self.path, "w") as zip:
            for name, data in buffer.items():
                zip.writestr(name, data)

    def _copy_data_from_zip(self):
        with ZipFile(self.path, "r") as zip:
            if self.arcname in zip.namelist():
                with zip.open(self.arcname, "r") as file:
                    self.write(file.read())
                    self.seek(0)

    def _copy_data_to_zip(self):
        self.delete_if_exists()
        with ZipFile(self.path, "a") as zip:
            with zip.open(self.arcname, "w") as file:
                file.write(self.getvalue())
