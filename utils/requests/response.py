import json
from http.client import HTTPResponse

from utils.requests.base64_json_encoder import Base64Encoder
from utils.requests.parameters_decoder import DecodeError, ParametersDecoder


class RequestError(Exception):
    """
    Raised when the response indicates that the corresponding request was
    not successful. This might be due to incorrect format of the request or
    because the request was not accepted by the server due to security issues.
    """
    pass


class BadRequestError(RequestError):
    """
    Raised when the request was invalid. A request is invalid if the format
    is not correct or it is missing some parameter. This happens when the
    response has the Bad Request code (400).
    """
    pass


class ForbiddenError(RequestError):
    """
    Raised when the request was valid, but the signature was not verified.
    This happens when the response has the Forbidden code (403).
    """
    pass


class HTTPError(Exception):
    """
    Raises when the response includes an error due to HTTP and not the
    format of the request. An error is considered HTTP if the status code
    of the response is not one of the expected codes.
    """
    def __init__(self, status_code: int, message):
        self.status_code = status_code
        self.message = message


class Response:
    """
    << Abstract Class >>

    Response is an abstraction of a HTTP response from a server to a previous
    request. As with the request, a response implementation abstracts the
    actual communication from the response parameters.

    Response is only the base class, and does not have a complete
    implementation. Each subclass must provide the implementation for the
    method and parameters getters. Those are use to perform the actual
    response. This class already ensures that the body of the response is
    signed. Therefore, all subclasses should just implement the previously
    mentioned getter methods.
    """

    # method should be static and immutable for all subclasses
    method = ""

    def __init__(self, parameters_values: dict):
        self._parameters_values = parameters_values
        self._parameters_values["response"] = self.method

    @staticmethod
    def load_response(http_response: HTTPResponse, response_type):
        """
        Takes an HTTP response and generates the appropriate response given
        its implementation. Expects the response content to be in JSON format.

        :param http_response: raw http response.
        :param response_type: implementation of a Response expected.
        :return: response object of the given implementation
        :raise ForbiddenError: if the server indicated the signature was
                               incorrect.
        :raise BadRequestError: if the server indicates the request was in
                                incorrect format or missing some parameters.
        :raise DecodeError: if the response is not in the expected format
                            or missing some parameters.
        :raise HTTPError: if the server sends an unexpected HTTP error.
        """
        Response._check_status_code(http_response)
        response_dict = ParametersDecoder.load(http_response.read().decode())

        try:
            # check if the Response method matches response type method
            if response_dict["response"] != response_type.method:
                raise DecodeError("Response method does not match")

            # parse each parameter of the given request type
            # ensure the value of each parameter is encoded in the type
            # format specified by the given request type
            values = {}
            for parameter, param_type in response_type.parameters_types.items():
                values[parameter] = param_type(response_dict[parameter])

            # create instance of the given request type
            # assign loaded values to the request
            return Response._create(response_type, values)

        except KeyError:
            raise DecodeError("response is missing at least one of its "
                              "required parameters")
        except TypeError:
            raise DecodeError("at least one of the parameters of the "
                              "response is not in the correct type")

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

    @staticmethod
    def _create(response_type, parameters_values: dict):
        """
        Creates an instance of the given response type. Assigns the response
        type with the values from the dictionary parameters_values.

        :param response_type: type of response to create.
        :param parameters_values: dict with the parameter values for the
                                  response.
        """
        return response_type(parameters_values)

    @staticmethod
    def _check_status_code(http_response: HTTPResponse):

        if http_response.status == 200:
            # successful response
            return
        elif http_response.status == 400:
            # bad request
            raise BadRequestError()
        elif http_response.status == 403:
            # request was forbidden - signature verification failed
            raise ForbiddenError()
        else:
            raise HTTPError(http_response.status,
                            http_response.read().decode())
