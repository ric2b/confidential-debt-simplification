from pytest import raises

from utils.requests.UOMe_response import UOMeResponse
from utils.requests.response import DecodeError, Response
from utils.requests.test_utils import fake_http_response, fake_body


class TestUOMeResponse:

    #
    # Tests for the from_parameters() method
    #

    def test_ValidResponseWithCorrectFormatting_UOMeResponseWithCorrespondingParameters(self):
        http_response = fake_http_response(body=fake_body({
            "response": "UOMe",
            "UOMe": "1234"
        }))

        response = Response.load_response(http_response, UOMeResponse)

        assert response.UOMe == "1234"

    def test_ResponseMissingTheResponseParameter_RaisesResponseError(self):
        http_response = fake_http_response(body=fake_body({
            "UOMe": "1234"
        }
        ))
        expected_message = "Response was missing some parameters"
        with raises(DecodeError, message=expected_message):
            Response.load_response(http_response, UOMeResponse)

    def test_ResponseWithIncorrectMethod_RaisesResponseError(self):
        http_response = fake_http_response(body=fake_body({
            "response": "INCORRECT",
            "UOMe": "1234"
        }))

        expected_message = "Response method does not match"
        with raises(DecodeError, message=expected_message):
            Response.load_response(http_response, UOMeResponse)

    def test_ResponseMethodIsAnInt_RaisesResponseError(self):
        http_response = fake_http_response(body=fake_body({
            "response": 1234,
            "UOMe": "1234"
        }))

        expected_message = "Parameters are of incorrect type"
        with raises(DecodeError, message=expected_message):
            Response.load_response(http_response, UOMeResponse)
