import json
from http.client import HTTPResponse
from json import JSONDecodeError

from utils.requests.base64_json_encoder import Base64Encoder


class RequestError(Exception):
    """
    Raised when the response indicates that the corresponding request was
    not successful. This might be due to incorrect format of the request or
    because the request was not accepted by the server due to security issues.
    """
    pass


class ResponseError(Exception):
    """
    Raised to indicate there is an error in the response. This might be a
    format error or the response is not of the expected type.
    """
    pass


class HTTPError(Exception):
    """
    Raises when the response includes an error due to HTTP and not the
    format of the request. An error is considered HTTP if the status code
    of the response is different from 200.
    """
    def __init__(self, status_code: int, message):
        self.status_code = status_code
        self.message = message


class Response:
    """
    Response is an abstraction of a response from a server to a previous
    request. As with the request, a response implementation abstracts the
    actual communication from the response parameters.
    """

    @staticmethod
    def from_HTTP_response(http_response: HTTPResponse, response_impl):
        """
        Takes an HTTP response and generates the appropriate response given
        its implementation. Expects the response content to be in JSON format.

        :param http_response: raw http response.
        :param response_impl: implementation of a Response expected.
        :return: response object of the given implementation
        :raise RequestError: if the server indicates the request was not
                             successful.
        :raise ResponseError: if the response is not in the expected format
                              or missing some parameters.
        :raise HTTPError: if the server sends an unexpected HTTP error.
        """
        return response_impl.from_parameters(
            Response._to_parameters(http_response))

    @staticmethod
    def _to_parameters(http_response: HTTPResponse) -> dict:
        """
        Takes an HTTP response and converts it into a parameters dict.

        :return: parameters dict for the given HTTP response.
        :raise RequestError: if the server indicates the request was not
                             successful.
        :raise ResponseError: if the response is not in the expected format.
        :raise HTTPError: if the server sends an unexpected HTTP error.
        """
        if http_response.status == 200:
            content_type = http_response.getheader('Content-Type')

            if content_type != 'application/json':  # expects only JSON
                raise ResponseError("Responses only support JSON format")

            try:
                raw = http_response.read()
                parameters = json.loads(raw.decode())
            except JSONDecodeError:
                raise ResponseError("Response does not contain valid JSON")

            if not isinstance(parameters, dict):
                raise ResponseError("Expected a JSON object")

        elif http_response.status == 400:  # Bad Request code
            # see the RequestError description to understand its meaning
            raise RequestError()
        else:
            raise HTTPError(http_response.status, http_response.read())

        return parameters

    @staticmethod
    def from_parameters(parameters: dict):
        """
        Takes a dictionary with the parameters from the server's response and
        constructs a response object. All subclasses must implement this
        method.

        :raise ResponseError: if the response is not in the expected format
                              or missing some parameters.
        :return: object of a subclass of response.
        """
        pass

    @property
    def parameters(self) -> dict:
        """
        Returns a dictionary containing the parameters of the response.

        :return: dictionary with the names and values of the response
                 parameters.
        """
        return dict()

    @property
    def body(self) -> str:
        """
        Returns a string containing the body of the response. The body of the
        response is composed by its parameters dictionary serialized to JSON
        format. Subclasses should not override this method and just implement
        the from_parameters static method.

        :return: JSON string containing the parameters of the response.
        """
        return json.dumps(self.parameters, cls=Base64Encoder)
