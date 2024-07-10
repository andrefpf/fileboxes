import json
from pprint import pprint


class CustomJsonEncoder(json.JSONEncoder):
    def key_handler(self, key):
        """
        Handle custom dict keys not usually suported by JSON.
        """

        if isinstance(key, tuple):
            return str(key)

        if isinstance(key, complex):
            return f"{key.real} + {key.imag}j"

        return key

    def value_handler(self, obj):
        """
        Handles custom object values not usually suported by JSON.
        """
        if isinstance(obj, complex):
            return {
                "__fileboxes_type__": "complex",
                "real": obj.real,
                "imag": obj.imag,
            }

        return obj

    # Everything bellow this comment is black magic.
    # Be carefull 🧙.

    def encode(self, obj) -> str:
        obj = self._recursive_key_handler(obj)
        return super().encode(obj)

    def default(self, obj):
        new_obj = self.value_handler(obj)
        if new_obj is not obj:
            return new_obj
        return super().default(obj)

    def _recursive_key_handler(self, obj):
        """
        This functions iterates recursivelly every list and dict
        to handle invalid dict keys.

        If you want to write custom key handlers checkout the
        "key handler" function.
        """

        if isinstance(obj, list):
            new_list = [self._recursive_key_handler(v) for v in obj]
            return new_list

        elif isinstance(obj, dict):
            new_dict = dict()
            key_info = dict()

            for k, v in obj.items():
                new_key = self.key_handler(k)
                new_dict[new_key] = self._recursive_key_handler(v)

                if type(k) != type(new_key):
                    key_info[new_key] = k

            if key_info:
                new_dict["__fileboxes_key_info__"] = key_info

            return new_dict

        else:
            return obj
