class Filebox:
    def __init__(self, path):
        pass

    def write(self, data, arcname: str):
        if isinstance(data, dict | list):
            return self._write_json(data, arcname)
        
        elif isinstance(data, str):
            return self._write_string()
        
        else:
            raise NotImplementedError(f"Data type {type(data)} not implemented.")

    def read(self, arcname: str):
        pass

    def _write_string(self, data: str, arcname: str):
        pass

    def _write_json(self, data: dict | list, arcname: str):
        pass

    def _write_image(self, data, arcname: str):
        pass

    def _read_string(self, arcname: str) -> str:
        pass

    def _read_json(self, arcname: str) -> dict | list:
        pass 

    def _read_image(self, arcname: str):
        pass
