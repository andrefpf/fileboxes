import json


class CustomJsonDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, obj):
        if isinstance(obj, dict) and ("__fileboxes_type__" in obj):
            type_name = obj["__fileboxes_type__"]

            if type_name == "complex":
                return complex(obj["real"], obj["imag"])

        return obj
