from utils.requests.response import ResponseError


class JoinResponse:
    """
    Join Response - response to a join request.
    """

    method = "JOIN"

    def __init__(self, main_server_signature: bytes,
                 inviter_signature: bytes, register_server_signature: bytes):
        self._parameters = {
            "response": self.method,
            "main_server_signature": main_server_signature,
            "inviter_signature": inviter_signature,
            "register_server_signature": register_server_signature
        }

    @staticmethod
    def from_parameters(parameters: dict):
        """
        Expects the following parameters:
            - response type
            - user ID signed by the main server
            - invite signed by the inviter
            - invite signed by the register server

        :raise ResponseError: if the response is not in the expected format
                              or missing some parameters.
        :return: JoinResponse object.
        """
        try:
            if parameters["response"] != JoinResponse.method:
                raise ResponseError("Response method does not match")

            # Note: there is no problem forcing the parameters to be strings
            # and then encoding to bytes. Any JSON type is decoded into a
            # python type that can be correctly converted to a string without
            # generating an exception. Checking if the value is correct is
            # not the responsibility of the response implementation

            return JoinResponse(
                main_server_signature=str(
                    parameters["main_server_signature"]).encode(),
                inviter_signature=str(parameters["inviter_signature"]).encode(),
                register_server_signature=str(
                    parameters["register_server_signature"]).encode()
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
    def main_server_signature(self) -> bytes:
        return self._parameters["main_server_signature"]

    @property
    def inviter_signature(self) -> bytes:
        return self._parameters["inviter_signature"]

    @property
    def register_server_signature(self) -> bytes:
        return self._parameters["register_server_signature"]
