import json
import os
import imghdr
from zipfile import ZipFile
from fileboxes.custom_json_config import CustomJsonEncoder, CustomJsonDecoder
from treelib import Tree
from collections import defaultdict
from pathlib import Path
from io import BytesIO
from PIL import Image



class Filebox:
    def __init__(self, path, override=True):
        self.path = path
        self.override = override

    def write(self, arcname: str, data: dict | list | str):
        if isinstance(data, dict | list):
            return self._write_json(arcname, data)

        elif ".png" in data or ".jpeg" in data:
            return self._write_image(arcname, data)

        elif isinstance(data, str):
            return self._write_string(arcname, data)

        else:
            raise NotImplementedError(f"Data type {type(data)} not implemented.")

    def read(self, arcname: str):
        file_extension = self._get_file_extension(arcname)

        if file_extension == "json":
            return self._read_json(arcname)
    
        elif file_extension in ["png", "jpeg"]:
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

    def _write_image(self, arcname: str, data):
        image_path = data
        if os.path.isfile(image_path):
            with open(image_path, "rb") as image_file:
                image_data = image_file.read()
            
            image_buffer = BytesIO(image_data)
            self._write_string(arcname, image_buffer.getvalue())
            
    def _read_string(self, arcname: str) -> str:
        with ZipFile(self.path, "r") as zip:
            data = zip.read(arcname)
        return data.decode("utf-8")

    def _read_json(self, arcname: str) -> dict | list:
        data = self._read_string(arcname)
        return json.loads(data, cls=CustomJsonDecoder)

    def _read_image(self, arcname: str):
        with ZipFile(self.path, "r") as zip:
            image_data = zip.read(arcname)

            image_buffer = BytesIO(image_data)
            return Image.open(image_buffer)

    def _get_file_extension(self, arcname: str) -> str:
        with ZipFile(self.path, "r") as zip:
            with zip.open(arcname, "r") as file:
                file_data= file.read()
        
        file_extension = imghdr.what(None, h=file_data)

        if file_extension in ["png", "jpeg"]:
            return file_extension
        
        try:
            json.loads(file_data)
            return "json"
        
        except json.JSONDecodeError:
            return