import json
import os
import imghdr
from zipfile import ZipFile
from fileboxes.custom_json_config import CustomJsonEncoder, CustomJsonDecoder
from treelib import Tree
from collections import defaultdict
from pathlib import Path
from io import BytesIO, StringIO
from PIL import Image
from configparser import ConfigParser, MissingSectionHeaderError


class Filebox:
    def __init__(self, path, override=True):
        self.path = path
        self.override = override

    def write(self, arcname: str, data: dict | list | str | Image.Image):
        if isinstance(data, dict | list):
            return self._write_json(arcname, data)

        elif isinstance(data, Image.Image):
            return self._write_image(arcname, data)

        elif isinstance(data, str):
            return self._write_string(arcname, data)

        elif isinstance(data, ConfigParser):
            return self._write_configparser(arcname, data)

        else:
            raise NotImplementedError(f"Data type {type(data)} not implemented.")

    def read(self, arcname: str):
        file_extension = Path(arcname).suffix

        if not file_extension:
            file_extension = self._get_file_extension(arcname)

        if file_extension == ".json":
            return self._read_json(arcname)
    
        elif file_extension in [".config", ".dat"]:
            return self._read_configparser(arcname)

        elif file_extension in [".png", ".jpeg", ".jpg"]:
            return self._read_image(arcname)

        else:
            return self._read_string(arcname)
            
    def remove(self, arcname: str):
        buffer = dict()
        with ZipFile(self.path, "r") as zip:
            if arcname not in zip.namelist():
                return
            for name in zip.namelist():
                if name != arcname:
                    buffer[name] = zip.read(name)

        with ZipFile(self.path, "w") as zip:
            for name, data in buffer.items():
                zip.writestr(name, data)

    def show_file_structure(self):
        print(self._file_structure_string())

    def _file_structure_string(self):
        with ZipFile(self.path, "r") as zip:
            stack = [Path(i) for i in zip.namelist()]

        # Create a tree from bottom-up
        tree_data = defaultdict(set)
        while len(stack):
            path = stack.pop()
            if path == Path():
                continue
            tree_data[path.parent].add(path)
            stack.append(path.parent)

        # Iterate the tree as top-down
        tree = Tree()
        stack = [Path()]
        tree.create_node(self.path, Path())
        while len(stack):
            path = stack.pop()
            for child in tree_data[path]:
                tree.create_node(child.name, child, parent=path)
                stack.append(child)

        return str(tree)

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        ...

    def _write_string(self, arcname: str, data: str):
        mode = "w" if self.override else "a"
        self.override = False

        if os.path.exists(self.path):
            self.remove(arcname)

        with ZipFile(self.path, mode) as zip:
            zip.writestr(arcname, data)

    def _write_json(self, arcname: str, data: dict | list):
        json_data = json.dumps(data, indent=2, cls=CustomJsonEncoder)
        self._write_string(arcname, json_data)

    def _write_image(self, arcname: str, data: Image.Image):
        image_format = data.format
        image_bytes_io = BytesIO()
        data.save(image_bytes_io, format=image_format)
        image_data = image_bytes_io.getvalue()

        self._write_string(arcname, image_data)

    def _write_configparser(self, arcname: str, data: ConfigParser):
        config_bytes_io = StringIO()
        data.write(config_bytes_io)
        config_data = config_bytes_io.getvalue()
        self._write_string(arcname, config_data)

    def _read_string(self, arcname: str) -> str:
        with ZipFile(self.path, "r") as zip:
            data = zip.read(arcname)
        return data.decode("utf-8")

    def _read_json(self, arcname: str) -> dict | list:
        data = self._read_string(arcname)
        return json.loads(data, cls=CustomJsonDecoder)

    def _read_image(self, arcname: str) -> Image.Image:
        with ZipFile(self.path, "r") as zip:
            image_data = zip.read(arcname)

        image_buffer = BytesIO(image_data)
        return Image.open(image_buffer)

    def _read_configparser(self, arcname: str) -> ConfigParser | None:
        config_string = self._read_string(arcname)
        config = ConfigParser()
        try:
            config.read_string(config_string)
            return config        
        except MissingSectionHeaderError:
            return None

    def _get_image_extension(self, arcname: str) -> str:
        with ZipFile(self.path, "r") as zip:
            file_data= zip.read(arcname)
        file_extension = imghdr.what(None, h=file_data)

        if file_extension:
            return "." + file_extension
        return
    
    def _get_json_extension(self, arcname: str) -> str:
        with ZipFile(self.path, "r") as zip:
            file_data= zip.read(arcname)

        try:
            json.loads(file_data)
            return ".json"
        except json.JSONDecodeError:
            return

    def _get_file_extension(self, arcname: str) -> str:
        file_extension = self._get_image_extension(arcname)

        if file_extension in [".png", ".jpeg"]:
            return file_extension
        
        file_extension = self._get_json_extension(arcname)
        return file_extension
        
        
    