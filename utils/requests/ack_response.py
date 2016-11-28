class AckResponse:
    """
    Ack Response - Is a special response to indicate everything went ok with 
    the request. It has no parameters.
    """

    method = "ACK"

    @staticmethod
    def from_parameters(parameters: dict):
        """
        It has no parameters, therefore, it just returns an AckResponse object.

        :return: AckResponse object.
        """
        return AckResponse()

    @property
    def parameters(self) -> dict:
        """ Returns empty dict """
        return {}
