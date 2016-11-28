from pytest import raises

from utils.requests.join_response import JoinResponse
from utils.requests.response import ResponseError


class TestJoinResponse:

    #
    # Tests for the from_parameters() method
    #

    def test_ValidResponseWithCorrectFormatting_JoinResponseWithCorrespondingParameters(self):
        parameters = {
            "response": "JOIN",
            "main_server_signature": "1234",
            "inviter_signature": "5678",
            "register_server_signature": "1357",
        }

        response = JoinResponse.from_parameters(parameters)

        assert response.main_server_signature == b"1234"
        assert response.inviter_signature == b"5678"
        assert response.register_server_signature == b"1357"

    def test_ResponseMissingTheResponseParameter_RaisesResponseError(self):
        parameters = {
            "main_server_signature": "1234",
            "inviter_signature": "5678",
            "register_server_signature": "1357",
        }

        expected_message = "Response was missing some parameters"
        with raises(ResponseError, message=expected_message):
            JoinResponse.from_parameters(parameters)

    def test_ResponseWithIncorrectMethod_RaisesResponseError(self):
        parameters = {
            "response": "INCORRECT",
            "main_server_signature": "1234",
            "inviter_signature": "5678",
            "register_server_signature": "1357",
        }

        expected_message = "Response method does not match"
        with raises(ResponseError, message=expected_message):
            JoinResponse.from_parameters(parameters)

    def test_ResponseMethodIsAnInt_RaisesResponseError(self):
        parameters = {
            "response": 1234,
            "main_server_signature": "1234",
            "inviter_signature": "5678",
            "register_server_signature": "1357",
        }

        expected_message = "Parameters are of incorrect type"
        with raises(ResponseError, message=expected_message):
            JoinResponse.from_parameters(parameters)
