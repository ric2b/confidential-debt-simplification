import json
from json import JSONEncoder


class Base64Encoder(JSONEncoder):
    """
    Encoder that adds support for base64.
    Basically all data in bytes is considered to be in base64 and is encoded
    as a JSON string.
    """

    def default(self, obj):
        if isinstance(obj, bytes):
            return obj.decode()

        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)
