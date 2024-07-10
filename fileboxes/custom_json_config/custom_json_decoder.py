import json


class CustomJsonDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, obj):
        """
        Every object enters this function during the decoding.
        """
        obj = self._handle_custom_keys(obj)
        obj = self._handle_custom_values(obj)
        return obj

    def _handle_custom_keys(self, obj: dict):
        if not self._has_custom_key(obj):
            return obj

        key_info = obj.pop("__fileboxes_key_info__")
        new_obj = dict()

        for k, v in obj.items():
            new_key = self._recover_key(k, key_info)
            new_obj[new_key] = v

        return new_obj

    def _handle_custom_values(self, obj: dict):
        if not self._has_custom_value(obj):
            return obj

        type_name = obj.get("__fileboxes_type__")

        if type_name == "complex":
            return complex(obj["real"], obj["imag"])
        else:
            return obj

    def _recover_key(self, key: str, key_info: dict):
        new_key = key_info.get(key, key)
        if isinstance(new_key, list):
            new_key = tuple(new_key)
        return new_key

    def _has_custom_key(self, obj) -> bool:
        return isinstance(obj, dict) and ("__fileboxes_key_info__" in obj)

    def _has_custom_value(self, obj) -> bool:
        return isinstance(obj, dict) and ("__fileboxes_type__" in obj)
