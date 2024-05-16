from zipfile import ZipFile
import json


class Filebox:
    def __init__(self, path, override=True):
        self.path = path
        self.override = override

    def write(self, arcname: str, data: dict | list | str):
        if isinstance(data, dict | list):
            return self._write_json(arcname, data)
        
        elif isinstance(data, str):
            return self._write_string(arcname, data)
        
        else:
            raise NotImplementedError(f"Data type {type(data)} not implemented.")

    def read(self, arcname: str):
        file_extension = self._get_file_extension(arcname)

        if file_extension == "json":
            return self._read_json(arcname)

        else:
            return self._read_string(arcname)

    def _write_string(self, arcname: str, data: str):
        mode = "w" if self.override else "a"
        self.override = False

        with ZipFile(self.path, mode) as zip:
            zip.writestr(arcname, data)

    def _write_json(self, arcname: str, data: dict | list):
        json_data = json.dumps(data, indent=2)
        self._write_string(arcname, json_data)

    def _write_image(self, arcname: str, data):
        pass

    def _read_string(self, arcname: str) -> str:
        with ZipFile(self.path, "r") as zip:
            data = zip.read(arcname)
        return data

    def _read_json(self, arcname: str) -> dict | list:
        data = self._read_string(arcname)
        return json.loads(data)

    def _read_image(self, arcname: str):
        pass

    def _get_file_extension(self, arcname: str) -> str:
        return "txt"
