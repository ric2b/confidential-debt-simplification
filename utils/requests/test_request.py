import pytest

from utils.requests.request import Request, RequestDecodeError


class TestRequest:

    #
    # Tests for the body_to_parameters() method
    #
    # The goal is not to test if teh JSON module works correctly
    # What we want to test is if the small logic inside the method besides
    # the loading of the JSON string works
    #

    def test_body_to_parameters_ValidJSONWithTwoObjects_DictWithTheTwoParameters(self):
        body = b'{"parameter1": "value1", "parameter2": "value2"}'

        parameters = Request._body_to_parameters(body)

        assert parameters == {
            "parameter1": "value1",
            "parameter2": "value2"
        }

    def test_body_to_parameters_JSONWithNoObjects_EmptyDict(self):
        body = b'{}'

        parameters = Request._body_to_parameters(body)

        assert parameters == {}

    def test_body_to_parameters_EmptyString_RaisesRequestDecodeError(self):
        body = b''

        with pytest.raises(RequestDecodeError):
            Request._body_to_parameters(body)

    def test_body_to_parameters_ValidJSONWithArray_RaisesRequestDecodeError(self):
        body = b'["parameter1", "parameter2"]'

        with pytest.raises(RequestDecodeError):
            Request._body_to_parameters(body)
