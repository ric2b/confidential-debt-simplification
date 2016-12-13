import json

from utils.messages.base64_json_encoder import Base64Encoder


class TestBase64Encoder:

    def test_EncodingByteStringABC_JSONStringABC(self):
        assert json.dumps(b"ABC", cls=Base64Encoder) == '"ABC"'
