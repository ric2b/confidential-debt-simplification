from http.client import HTTPResponse
from unittest.mock import MagicMock, Mock

from pytest import raises

from utils.requests.response import Response, HTTPError, BadRequestError, \
    ForbiddenError
from utils.requests.test_utils import fake_http_response


class TestResponse:

    #
    # Tests for the check_status_code() method
    #

    def test_check_status_code_Code200ForOK_DoesNotRaiseAnything(self):
        http_response = fake_http_response(status=200, body=b"")

        Response._check_status_code(http_response)

    def test_check_status_code_Code400ForBadRequest_RaisesBadRequestError(self):
        http_response = fake_http_response(status=400, body=b"")

        with raises(BadRequestError):
            Response._check_status_code(http_response)

    def test_check_status_code_Code403ForForbidden_RaisesForbiddenRequestError(self):
        http_response = fake_http_response(status=403, body=b"")

        with raises(ForbiddenError):
            Response._check_status_code(http_response)

    def test_check_status_code_UnexpectedCode_RaisesHTTPError(self):
        http_response = fake_http_response(status=500, body=b"some content")

        with raises(HTTPError, message="some content"):
            Response._check_status_code(http_response)
