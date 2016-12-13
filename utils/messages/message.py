import json

from utils.messages.base64_json_encoder import Base64Encoder


class DecodeError(Exception):
    """ Raised when there is an error while decoding parameters """


class Message:
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

    message_type = None  # type: str
    parameter_types = None  # type: {str: type}

    def __init__(self, **given_parameters: {str: object}):
        """
        Initializes a someRequest object from the someRequest class attributes.
        In particular, the following are added as object attributes:
        - request_type
        - parameter_types

        It also sets the object.signature to Null if a signature isn't given.
        This is done because a request can be created before being signed with
        the sign(key) method.

        :param given_parameters:
        """

        # check that the attributes were assigned.
        if not (self.message_type and self.parameter_types):
            raise NotImplementedError('One of the class attributes was not initiated')

        if not(isinstance(self.message_type, str) and
                isinstance(self.parameter_types, dict)):
            raise TypeError('One of the class attributes is of the wrong type')

        # This will be sub-classed, get the attributes from the sub-class
        parameter_types = self.parameter_types

        # Check that argument types match the request parameter types (and exist)
        for parameter in parameter_types:
            if not isinstance(given_parameters[parameter], parameter_types[parameter]):
                error_string = "Got type %s for parameter %s but expected type %s"
                raise TypeError(error_string % (type(given_parameters[parameter]),
                                                parameter,
                                                parameter_types[parameter]))
            else:
                # Add the parameter as an object attribute if it's type is correct
                setattr(self, parameter, given_parameters[parameter])


    @classmethod
    def load(cls, request_body: bytes):
        """
        Loads a request from a JSON string. All subclasses must implement
        this static method.

        :param request_body: body of the request in bytes format.
        :param request_type: request type to be loaded.
        :return: request object.
        :raise DecodeError: if the JSON string is incorrectly formatted or if
                                   it misses any parameter.
        """
        request_items = json.loads(request_body.decode())

        try:
            # parse each parameter of the given request type
            # ensure the value of each parameter is encoded in the type
            # format specified by the given request type
            values = {}
            for parameter, param_type in cls.parameter_types.items():
                # TODO: This is a temporary hack because I don't have an Identifier Type
                if not isinstance(request_items[parameter], param_type):
                    error_string = "Got type %s for parameter %s but expected type %s"
                    raise TypeError(error_string % (type(request_items[parameter]),
                                                    parameter,
                                                    param_type))
                else:
                    values[parameter] = request_items[parameter]

            # create instance of the given request type
            return cls(**values)

        except KeyError:
            raise DecodeError("request is missing at least one of its "
                              "required parameters")
        except TypeError:
            raise DecodeError("at least one of the parameters of the "
                              "request is not in the correct type")

    @property
    def body(self) -> str:
        """
        Returns a string containing the body of the request. The body of the
        request is composed by the parameters dictionary of the request
        implementation serialized to JSON format. Subclasses should not
        override this method and just implement the parameters property.

        :return: JSON string containing the parameters of the request.
        """
        parameters = {}
        for parameter in self.parameter_types:
            parameters[parameter] = getattr(self, parameter)

        return json.dumps(parameters, cls=Base64Encoder)

    def dump(self) -> bytes:
        """
        Encode the body into UTF-8 for network transport

        :return: JSON bytes string containing the parameters of the request.
        """
        return self.body.encode()
