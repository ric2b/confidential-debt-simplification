import pytest

from utils.requests.request import Request, RequestDecodeError


class TestRequest:

    #
    # Tests for the read_body() method
    #
    # The goal is not to test if teh JSON module works correctly
    # What we want to test is if the small logic inside the method besides
    # the loading of the JSON string works
    #

    def test_read_body_ValidJSONWithTwoObjects_DictWithTheTwoParameters(self):
        body = b'{"parameter1": "value1", "parameter2": "value2"}'

        parameters = Request._read_body(body)

        assert parameters == {
            "parameter1": "value1",
            "parameter2": "value2"
        }

    def test_read_body_JSONWithNoObjects_EmptyDict(self):
        body = b'{}'

        parameters = Request._read_body(body)

        assert parameters == {}

    def test_read_body_EmptyString_RaisesRequestDecodeError(self):
        body = b''

        with pytest.raises(RequestDecodeError):
            Request._read_body(body)

    def test_read_body_ValidJSONWithArray_RaisesRequestDecodeError(self):
        body = b'["parameter1", "parameter2"]'

        with pytest.raises(RequestDecodeError):
            Request._read_body(body)
