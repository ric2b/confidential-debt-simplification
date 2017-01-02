from unittest.mock import Mock, MagicMock

import pytest
from pytest import raises

from utils.messages.connection import Connection, BadRequestError, \
    UnauthorizedError, ForbiddenError, ConflictError, NotFoundError, \
    UnknownError
from utils.messages.message import Message
from utils.messages.testing_utils import fake_http_response


class FakeMessage(Message):
    """ Fake response used in the test to load responses """

    message_type = 'fake'
    url = "fake-url"
    request_params = {}
    response_params = {}
    signature_formats = {}

    @staticmethod
    def raw():
        """ Returns the raw message encoded in JSON """
        return b"{}"


def fake_http_connection(response_status=200, response_body=b"{}"):
    http_response = fake_http_response(response_status, response_body)
    connection = Mock()
    connection.getresponse = MagicMock(return_value=http_response)

    return connection


class TestConnection:

    @pytest.mark.parametrize("response_status", (200, 201, 202))
    def test_get_response_StatusIs20X_ReturnsExpectedResponse(self, response_status):
        connection = Connection("http://url.com", fake_http_connection(response_status))

        assert isinstance(connection.get_response(FakeMessage), FakeMessage)

    @pytest.mark.parametrize("response_status, exception", (
            (400, BadRequestError),
            (401, UnauthorizedError),
            (403, ForbiddenError),
            (409, ConflictError),
            (404, NotFoundError),
            (444, UnknownError),
    ))
    def test_get_response_StatusIsErrorCode_RaisesExceptionAccordingToCode(
            self, response_status, exception):

        connection = Connection("http://url.com",
                                fake_http_connection(response_status))

        with raises(exception):
            connection.get_response(FakeMessage)

