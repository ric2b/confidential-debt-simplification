import json
from json import JSONDecodeError

from utils.requests.base64_json_encoder import Base64Encoder
from utils.requests.parameters_decoder import ParametersDecoder, DecodeError
from utils.requests.signer import Signer
from utils.requests.verifier import Verifier


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

    request_type = None
    parameter_types = None
    parameters_to_sign = None

    def __init__(self, **kwargs):
        # This will be sub-classed, we want to get the attributes from those sub-classes
        parameter_types = self.__class__.parameter_types
        self.__dict__['signature'] = None

        # Check that the types of the arguments match the request parameters, and that they exist
        for parameter in parameter_types:
            if not isinstance(kwargs[parameter], parameter_types[parameter]):
                error_string = "Got type %s for parameter %s but expected type %s"
                raise TypeError(error_string % (type(kwargs[parameter]),
                                                parameter,
                                                parameter_types[parameter]))
            else:
                # If the parameter type is correct, add it as an object attribute
                self.__dict__[parameter] = kwargs[parameter]

        print(kwargs)
        print(self.__dict__)

    def sign(self, signer: Signer):
        # This will be sub-classed, we want to get the attributes from those sub-classes
        signed_parameters = self.__class__.parameters_to_sign

        # Figure out what parameters need to be signed and concatenate them in a bytes string
        to_be_signed = b""
        for parameter_to_sign in signed_parameters:
            parameter = self.__dict__[parameter_to_sign]
            parameter_bytes = parameter if isinstance(parameter, bytes) else parameter.encode()
            to_be_signed += parameter_bytes

        # Create the signature for the request
        self.__dict__['signature'] = signer.sign(to_be_signed)

        return self

    def verify(self, verifier: Verifier):
        # This will be sub-classed, we want to get the attributes from those sub-classes
        parameters_to_sign = self.__class__.parameters_to_sign

        signed_parameters = []
        for parameter in parameters_to_sign:
            parameter_value = self.__dict__[parameter]
            bytes_value = parameter_value if isinstance(parameter_value, bytes) else parameter_value.encode()
            signed_parameters.append(bytes_value)

        verifier.verify(self.signature, *signed_parameters)

        self.extra_verifications()

    def extra_verifications(self):
        pass

    @classmethod
    def load_request(cls, request_body: bytes):
        """
        Loads a request from a JSON string. All subclasses must implement
        this static method.

        :param request_body: body of the request in bytes format.
        :param request_type: request type to be loaded.
        :return: request object.
        :raise DecodeError: if the JSON string is incorrectly formatted or if
                                   it misses any parameter.
        """
        request_items = ParametersDecoder.load(request_body.decode())

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
            values['signature'] = request_items.get('signature', None)

            # create instance of the given request type
            # assign loaded values to the request
            return Request._create(cls, values)

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
        return self.__class__.request_type

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

    @staticmethod
    def _create(request_type, parameters_values: dict):
        """
        Creates an instance of the given request type. Assigns the request
        type with the values from the dictionary parameters_values.

        :param request_type: type of request to create.
        :param parameters_values: dict with the parameter values for the
                                  request.
        """
        request = request_type(**parameters_values)
        request.__dict__['signature'] = parameters_values['signature']
        return request
