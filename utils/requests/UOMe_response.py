from utils.requests.response import Response


class UOMeResponse(Response):
    """
    UOMe Response - response to a UOMe request.
    """

    method = "UOMe"

    # The class field parameter_types defines the parameters and types of
    # the values of each parameter
    parameters_types = {
        "UOMe": str,
    }

    @staticmethod
    def build(UOMe_id: str):
        """
        Factory method for an UOMe response. Use this method to create
        UOMe responses instead of the default initializer.

        Returns an UOMe response signed by the given signer. This method
        abstracts which parameters are signed by the signer.
        """
        parameters_values = {
            "UOMe": UOMe_id,
        }

        return UOMeResponse(parameters_values)

    @property
    def parameters(self) -> dict:
        return self._parameters_values

    @property
    def UOMe(self) -> str:
        return self._parameters_values["UOMe"]
