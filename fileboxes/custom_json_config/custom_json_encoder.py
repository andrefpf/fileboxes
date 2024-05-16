import json


class CustomJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, complex):
            return {
                "__fileboxes_type__": "complex",
                "real": obj.real,
                "imag": obj.imag,
            }
        return super().default(obj)