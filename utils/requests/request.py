import json
from json import JSONDecodeError

from utils.requests.base64_json_encoder import Base64Encoder


class RequestDecodeError(Exception):
    """ Raised to indicate that there was an error while decoding a request. """


class Request:
    """
    << Abstract Class >>

    Request abstracts the complexity of an HTTP request. Hides the actual
    format of the request and provides a clean interface to set the values of
    the parameters required for each type of request.

    A request is always associated with a method. A method is the actual
    operation required from the server. This maps directly into django's view
    model. For instance, when a client want to invite someone it goes to the URL
    proxy-server.com/invite. "invite" is the method of the request.

    Request is only the base class, and does not have a complete
    implementation. Each subclass must provide the implementation for the
    method and parameters getters. Those are use to perform the actual
    request. This class already ensures that the body of the request is
    signed. Therefore, all subclasses should just implement the previously
    mentioned getter methods.
    """

    def __init__(self, parameters_values: dict):
        self._parameters_values = parameters_values

    @staticmethod
    def load_request(request_body: bytes, request_type):
        """
        Loads a request from a JSON string. All subclasses must implement
        this static method.

        :param request_body: body of the request in bytes format.
        :param request_type: request type to be loaded.
        :return: request object.
        :raise RequestDecodeError: if the JSON string is incorrectly formatted or if
                                   it misses any parameter.
        """
        request_items = Request._read_body(request_body)

        try:
            # parse each parameter of the given request type
            # ensure the value of each parameter is encoded in the type
            # format specified by the given request type
            values = {}
            for parameter, param_type in request_type.parameters_types.items():
                values[parameter] = param_type(request_items[parameter])

            # create instance of the given request type
            # assign loaded values to the request
            return Request._create(request_type, values)

        except KeyError:
            raise RequestDecodeError("request is missing at least one "
                                     "of its required parameters")
        except TypeError:
            raise RequestDecodeError("at least one of the parameters of the "
                                     "request is not in the correct type")

    @property
    def method(self) -> str:
        """
        Returns the method of the request. The method should be a string and
        should be the same for all instances of the request implementation.

        :return: request's method
        """
        return ""

    @property
    def parameters(self) -> dict:
        """
        Must return a dictionary containing the parameters of the request.
        For instance, the invite request would require 2 parameters: the
        invitee ID and its email, thereby, the parameters getter should
        return a dictionary with: { 'invitee_ID': ID, 'invitee_email': email }.

        :return: dictionary with the names and values of the request parameters.
        """
        return dict()

    @property
    def body(self) -> str:
        """
        Returns a string containing the body of the request. The body of the
        request is composed by the parameters dictionary of the request
        implementation serialized to JSON format. Subclasses should not
        override this method and just implement the parameters property.

        :return: JSON string containing the parameters of the request.
        """
        return json.dumps(self.parameters, cls=Base64Encoder)

    @staticmethod
    def _create(request_type, parameters_values: dict):
        """
        Creates an instance of the given request type. Assigns teh request
        type with the values from the dictionary parameters_values.

        :param request_type: type of request to create.
        :param parameters_values: dict with the parameter values for the
                                  request.
        """
        return request_type(parameters_values)

    @staticmethod
    def _read_body(request_body: bytes) -> dict:
        """
        Reads a request body in bytes format and returns a dictionary with
        the read parameters. The values of the parameters are returned as
        JSON supported types, which means that some base64 encoded values
        are returned as strings and must be converted outside this method.

        This method abstracts the encoding of the requests. Its current
        implementation decodes from JSON format. It is enough to
        re-implement this method to change to other encoding format.

        :param request_body: request body in bytes format.
        :return: dictionary with the parameters (parameter values support
                 ony JSON supported types)
        """
        # JSON loads method expects a string
        request_body = request_body.decode()

        try:
            loaded_parameters = json.loads(request_body)
        except JSONDecodeError as error:
            raise RequestDecodeError(error)

        if isinstance(loaded_parameters, dict):
            return loaded_parameters
        else:
            raise RequestDecodeError("Parameters must be encoded as "
                                     "JSON objects")
