# from io import IOBase, BytesIO
import io
from pathlib import Path
from zipfile import ZipFile


class ZipIO(io.BytesIO):
    def __init__(self, path: str | Path, arcname: str, override: bool = False) -> None:
        super().__init__()

        self.path = Path(path)
        self.arcname = arcname

        if path.exists() and not override:
            with ZipFile(self.path, "r") as zip:
                with zip.open(self.arcname, "r") as file:
                    self.write(file.read())

    def close(self):
        with ZipFile(self.path, "w") as zip:
            with zip.open(self.arcname, "w") as file:
                file.write(self.getvalue())
        super().close()
