from utils.requests.response import Response


class AckResponse(Response):
    """
    Ack Response - Is a special response to indicate everything went ok with 
    the request. It has no parameters.
    """

    method = "ACK"

    # The class field parameter_types defines the parameters and types of
    # the values of each parameter
    parameters_types = {}

    @staticmethod
    def build():
        return AckResponse({})

    @property
    def parameters(self) -> dict:
        """ Returns empty dict """
        return {}
