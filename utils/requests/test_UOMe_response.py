from pytest import raises

from utils.requests.UOMe_response import UOMeResponse
from utils.requests.response import ResponseError


class TestUOMeResponse:

    #
    # Tests for the from_parameters() method
    #

    def test_ValidResponseWithCorrectFormatting_UOMeResponseWithCorrespondingParameters(self):
        parameters = {
            "response": "UOMe",
            "UOMe": "1234"
        }

        response = UOMeResponse.from_parameters(parameters)

        assert response.UOMe == "1234"

    def test_ResponseMissingTheResponseParameter_RaisesResponseError(self):
        parameters = {
            "UOMe": "1234"
        }

        expected_message = "Response was missing some parameters"
        with raises(ResponseError, message=expected_message):
            UOMeResponse.from_parameters(parameters)

    def test_ResponseWithIncorrectMethod_RaisesResponseError(self):
        parameters = {
            "response": "INCORRECT",
            "UOMe": "1234"
        }

        expected_message = "Response method does not match"
        with raises(ResponseError, message=expected_message):
            UOMeResponse.from_parameters(parameters)

    def test_ResponseMethodIsAnInt_RaisesResponseError(self):
        parameters = {
            "response": 1234,
            "UOMe": "1234"
        }

        expected_message = "Parameters are of incorrect type"
        with raises(ResponseError, message=expected_message):
            UOMeResponse.from_parameters(parameters)
