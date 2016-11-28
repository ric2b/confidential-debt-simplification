from unittest.mock import MagicMock, Mock

from pytest import raises

from utils.requests.response import Response, HTTPError, ResponseError, \
    RequestError


def fake_http_response(status=200, headers=None, body=bytes()):
    """
    Creates a fake HTTP response.

    :param status:  status code of the response.
    :param headers: dict with the header keys and values.
    :param body:    body of the response in bytes
    :return: fake http response (mock object)
    """
    if headers is None:
        headers = {}

    http_response = Mock()
    http_response.status = status

    def side_effect(header):
        return headers.get(header)

    http_response.getheader = Mock(side_effect=side_effect)
    http_response.read = MagicMock(return_value=body)

    return http_response


# noinspection PyTypeChecker,PyPep8Naming
class TestResponse_ToParameters:

    #
    # Tests for the _to_parameters() method
    #

    def test_200ResponseWithJsonHeaderAndOneParameter_DictWithTheReceivedParameter(self):
        response = fake_http_response(
            status=200,
            headers={'Content-Type': 'application/json'},
            body=b'{"parameter": "value"}'
        )

        parameters = Response._to_parameters(response)

        assert parameters == {
            "parameter": "value"
        }

    def test_404Response_Raises404HTTPError(self):
        response = fake_http_response(
            status=404,
            headers={},
            body=b'Not found'
        )

        with raises(HTTPError, status_code=404):
            Response._to_parameters(response)

    def test_200ResponseMissingContentType_RaisesResponseError(self):
        response = fake_http_response(
            status=200,
            headers={},
            body=b'{"parameter": "value"}'
        )

        with raises(ResponseError):
            Response._to_parameters(response)

    def test_200ResponseWithInvalidContentType_RaisesResponseError(self):
        response = fake_http_response(
            status=200,
            headers={'Content-Type': 'text/html'},
            body=b'{"parameter": "value"}'
        )

        with raises(ResponseError):
            Response._to_parameters(response)

    def test_200ResponseWithInvalidJSONFormat_RaisesResponseError(self):
        response = fake_http_response(
            status=200,
            headers={'Content-Type': 'application/json'},
            body=b'parameter'
        )

        with raises(ResponseError):
            Response._to_parameters(response)

    def test_200ResponseWithoutJSONObject_RaisesResponseError(self):
        response = fake_http_response(
            status=200,
            headers={'Content-Type': 'application/json'},
            body=b'["parameter", "value"]'
        )

        with raises(ResponseError):
            Response._to_parameters(response)

    def test_400Response_RaisesRequestError(self):
        response = fake_http_response(
            status=400,
            headers={},
            body=b'Bad Request'
        )

        with raises(RequestError):
            Response._to_parameters(response)
