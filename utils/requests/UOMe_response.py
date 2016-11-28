from utils.requests.response import ResponseError


class UOMeResponse:
    """
    UOMe Response - response to a UOMe request.
    """

    method = "UOMe"

    def __init__(self, UOMe_id: str):
        self._parameters = {
            "response": self.method,
            "UOMe": UOMe_id
        }

    @staticmethod
    def from_parameters(parameters: dict):
        """
        Expects the following parameters:
            - response type
            - UOMe ID

        :raise ResponseError: if the response is not in the expected format
                              or missing some parameters.
        :return: UOMeResponse object.
        """
        try:
            if parameters["response"] != UOMeResponse.method:
                raise ResponseError("Response method does not match")

            # Note: there is no problem forcing the parameters to be strings
            # and then encoding to bytes. Any JSON type is decoded into a
            # python type that can be correctly converted to a string without
            # generating an exception. Checking if the value is correct is
            # not the responsibility of the response implementation

            return UOMeResponse(
                UOMe_id=str(parameters["UOMe"])
            )

        except KeyError:
            raise ResponseError("Response was missing some parameters")
        except ValueError:
            raise ResponseError("Parameters are of incorrect type")

    @property
    def parameters(self) -> dict:
        """
        Returns a dictionary containing the parameters of the response.

        :return: dictionary with the names and values of the response
                 parameters.
        """
        return self._parameters

    @property
    def UOMe(self) -> str:
        return self._parameters["UOMe"]
