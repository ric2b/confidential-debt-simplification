import json

from utils.crypto.rsa import sign, verify


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

    message_type = None  # type: str: Only used for Message objects, not Message classes
    request_params = None  # type: {str: type}
    response_params = None  # type: {str: type}
    signature_formats = None  # type: {str: [str]}

    @classmethod
    def _check_class(cls):
        """
        Verify that the sub-class correctly implemented the abstract
        parameters of the Message class.
        """
        if not (cls.request_params and cls.response_params and cls.signature_formats):
            raise NotImplementedError('One or more class attributes were not initiated')

        if not (isinstance(cls.request_params, dict)
                and isinstance(cls.response_params, dict)
                and isinstance(cls.signature_formats, dict)):
            raise TypeError('One or more class attributes are of the wrong type')

        return  # So PyCharm stops complaining that this is an abstract method...

    @classmethod
    def _get_parameters_for_message_type(cls, message_type):
        # use the correct parameter_types for the message type
        if message_type == 'request':
            return cls.request_params
        elif message_type == 'response':
            return cls.response_params
        else:
            raise TypeError('received an unsupported message-type: %s' % message_type)

    def __init__(self, message_type, **given_parameters: {str: object}):
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

        # verify that the sub-class is implemented correctly and choose parameters
        self._check_class()
        parameter_types = self._get_parameters_for_message_type(message_type)
        self.message_type = message_type

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
    def make_request(cls, **given_parameters: {str: object}):
        return cls('request', **given_parameters)

    @classmethod
    def make_response(cls, **given_parameters: {str: object}):
        return cls('response', **given_parameters)

    @classmethod
    def load(cls, message_type, request_body: str):
        """
        Loads a request from a JSON string. All subclasses must implement
        this static method.

        :param message_type: the type of message, a request or a response
        :param request_body: body of the request in bytes format.
        :return: request object.
        :raise DecodeError: if the JSON string is incorrectly formatted or if
                                   it misses any parameter.
        """

        # verify that the sub-class is implemented correctly and choose parameters
        cls._check_class()
        parameter_types = cls._get_parameters_for_message_type(message_type)

        request_items = json.loads(request_body)

        try:
            # parse each parameter of the given request type
            # ensure the value of each parameter is encoded in the type
            # format specified by the given request type
            values = {}
            for parameter, param_type in parameter_types.items():
                # TODO: This is a temporary hack because I don't have an Identifier Type
                if not isinstance(request_items[parameter], param_type):
                    error_string = "Got type %s for parameter %s but expected type %s"
                    raise TypeError(error_string % (type(request_items[parameter]),
                                                    parameter,
                                                    param_type))
                else:
                    values[parameter] = request_items[parameter]

            # create instance of the given message type
            return cls(message_type, **values)

        except KeyError:
            raise DecodeError("message is missing at least one of its "
                              "required parameters")
        except TypeError:
            raise DecodeError("at least one of the parameters of the "
                              "message is not in the correct type")

    @classmethod
    def load_request(cls, message_body: str):
        return cls.load('request', message_body)

    @classmethod
    def load_response(cls, message_body: str):
        return cls.load('response', message_body)

    def dumps(self) -> str:
        """
        Returns a string containing the body of the message. The body of the
        message is composed by the parameters dictionary of the message
        implementation serialized to JSON format. Subclasses should not
        override this method and just implement the parameters property.

        :return: JSON string containing the parameters of the message.
        """
        parameters = {}
        for parameter in self._get_parameters_for_message_type(self.message_type):
            parameters[parameter] = getattr(self, parameter)

        return json.dumps(parameters)

    @classmethod
    def _order_signature_parameters(cls, signature_name, **parameters):
        # raises KeyError if the signature_name isn't found in the Message sub-class
        signature_format = cls.signature_formats[signature_name]

        # make a list with all the parameters in the correct order
        signature_values = []
        for parameter_name in signature_format:
            # TODO: check types, maybe?
            try:
                parameter = parameters[parameter_name]
                signature_values.append(str(parameter))
            except KeyError:
                error_msg = "missing parameter '%s' required for '%s' signature"
                raise AttributeError(error_msg % (parameter_name, signature_name))

        return signature_values

    @classmethod
    def sign(cls, key, signature_name, **parameters):
        """
        Signs a single signature described in the class attribute "signatures_formats".
        The signature to sign is chosen with "signature_name".
        The values can be given in any order but they must be gives as keyword arguments
        that match the names of the parameters present in the signature format.

        :param key:
        :param signature_name:
        :param parameters:

        :raises KeyError: signature_name is not the name of a signature for this class
        :raises AttributeError: at least one signature parameter was not given
        :raises TypeError: --Currently not implemented--
        """
        signature_values = cls._order_signature_parameters(signature_name, **parameters)

        return sign(key, *signature_values)

    @classmethod
    def verify(cls, key, signature_name, signature, **parameters):
        """
        Verifies a single signature described in the class attribute "signatures_formats".
        The signature to verify is chosen with "signature_name".
        The values can be given in any order but they must be gives as keyword arguments
        that match the names of the parameters present in the signature format.

        :param key:
        :param signature_name:
        :param signature:
        :param parameters:

        :raises KeyError: signature_name is not the name of a signature for this class
        :raises AttributeError: at least one signature parameter was not given
        :raises TypeError: --Currently not implemented--
        :raises InvalidSignature: the signature is invalid, either wrong key or wrong data
        """
        signature_values = cls._order_signature_parameters(signature_name, **parameters)

        verify(key, signature, *signature_values)