import json

from utils.requests.base64_json_encoder import Base64Encoder
from utils.requests.parameters_decoder import DecodeError
from utils.crypto.rsa import sign, verify


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

    request_address = None  # type: str
    parameter_types = None  # type: {str: type}
    format_to_sign = None  # type: [str]
    formats_to_verify = None  # type: {str: [str]}

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
        if not (self.__class__.request_address and self.__class__.parameter_types and
                self.__class__.format_to_sign and self.__class__.formats_to_verify):
            raise NotImplementedError('One of the class attributes was not initiated')

        # This will be sub-classed, get the attributes from the sub-class
        parameter_types = self.__class__.parameter_types

        # Check that argument types match the request parameter types (and exist)
        for parameter in parameter_types:
            if not isinstance(given_parameters[parameter], parameter_types[parameter]):
                error_string = "Got type %s for parameter %s but expected type %s"
                raise TypeError(error_string % (type(given_parameters[parameter]),
                                                parameter,
                                                parameter_types[parameter]))
            else:
                # Add the parameter as an object attribute if it's type is correct
                self.__dict__[parameter] = given_parameters[parameter]

        self.__dict__['signature'] = given_parameters.get('signature', None)

    def sign(self, key: str) -> object:
        """
        Signs the request as defined in self.__class__.format_to_sign, using key.
        The resulting signature is added as an object attribute, so it can be
        accessed via request.signature.
        The object is returned so that a request initialization can be done with:
        request = someRequest(**params).sign(key)

        :param key:
        :return self:
        """
        # This will be sub-classed, get the attributes from the sub-class
        format_to_sign = self.__class__.format_to_sign

        # Concatenate in a string the parameters to be signed
        to_be_signed = []
        for parameter_to_sign in format_to_sign:
            to_be_signed.append(self.__dict__[parameter_to_sign])

        # Sign and add the signature as an object attribute
        self.__dict__['signature'] = sign(key, *to_be_signed)

        return self

    def verify(self, **signature_keys: {str: str}):
        """
        Verify all the signatures in self.__class__.formats_to_verify, using the
        keys given in signature_keys.

        If one of the signatures is invalid, InvalidSignature is raised.
        It's not important to know which one failed since the request should fail
        regardless of which one it was. (May be useful for debugging purposes?)

        :param signature_keys: a map of keys used to verify the signatures
        :raises InvalidSignature: if any of the signatures fail to verify
        """
        # This will be sub-classed, get the attributes from the sub-class
        formats_to_verify = self.__class__.formats_to_verify

        for sig_name, sig_format in formats_to_verify.items():
            signature = self.__dict__[sig_name]
            parameters_to_sign = ""
            for parameter in sig_format:
                parameters_to_sign += str(self.__dict__[parameter])

            verify(signature_keys[sig_name], signature, *parameters_to_sign)


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

            # Load the signature as well, if it exists
            signature = request_items.get('signature', None)
            values['signature'] = signature if isinstance(signature, str) else None

            # create instance of the given request type
            return cls(**values)

        except KeyError:
            raise DecodeError("request is missing at least one of its "
                              "required parameters")
        except TypeError:
            raise DecodeError("at least one of the parameters of the "
                              "request is not in the correct type")

    @property
    def method(self) -> str:
        """
        Returns the method of the request. The method should be a string and
        should be the same for all instances of the request implementation.

        :return: request's method
        """
        return self.__class__.request_address

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
        for parameter in self.__class__.parameter_types:
            parameters[parameter] = self.__dict__[parameter]

        return json.dumps(parameters, cls=Base64Encoder)
