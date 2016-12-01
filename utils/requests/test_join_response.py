from pytest import raises

from utils.requests.join_response import JoinResponse
from utils.requests.response import DecodeError, Response
from utils.requests.test_utils import fake_body, fake_http_response, \
    fake_verifier


class TestJoinResponse:

    #
    # Tests for the load_response() method
    #

    def test_ValidResponseWithCorrectFormatting_JoinResponseWithCorrespondingParameters(self):
        http_response = fake_http_response(body=fake_body({
            "response": "JOIN",
            "main_server_signature": "1234",
            "inviter_signature": "5678",
            "register_server_signature": "1357",
        }))

        response = Response.load_response(http_response, JoinResponse)

        assert response.main_server_signature == b"1234"
        assert response.inviter_signature == b"5678"
        assert response.register_server_signature == b"1357"

    def test_ResponseMissingTheResponseParameter_RaisesResponseError(self):
        http_response = fake_http_response(body=fake_body({
            "main_server_signature": "1234",
            "inviter_signature": "5678",
            "register_server_signature": "1357",
        }))

        expected_message = "Response was missing some parameters"
        with raises(DecodeError, message=expected_message):
            Response.load_response(http_response, JoinResponse)

    def test_ResponseWithIncorrectMethod_RaisesResponseError(self):
        http_response = fake_http_response(body=fake_body({
            "response": "INCORRECT",
            "main_server_signature": "1234",
            "inviter_signature": "5678",
            "register_server_signature": "1357",
        }))

        expected_message = "Response method does not match"
        with raises(DecodeError, message=expected_message):
            Response.load_response(http_response, JoinResponse)

    def test_ResponseMethodIsAnInt_RaisesResponseError(self):
        http_response = fake_http_response(body=fake_body({
            "response": 1234,
            "main_server_signature": "1234",
            "inviter_signature": "5678",
            "register_server_signature": "1357",
        }))

        expected_message = "Parameters are of incorrect type"
        with raises(DecodeError, message=expected_message):
            Response.load_response(http_response, JoinResponse)
