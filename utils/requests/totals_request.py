from utils.requests.request import Request, RequestDecodeError
from utils.requests.signer import Signer


class TotalsRequest(Request):
    """
    Totals request is sent by the user to obtain its totals.
    """

    def __init__(self, user_id: bytes, signature: bytes):
        #
        # Parameters in bytes format are stored as a str. However,
        # the respective getter methods return bytes.
        # This prevents problems when serializing to JSON and deserializing
        # since JSON does not support the bytes format.
        #
        self._parameters = {
            "user": user_id,
            "signature": signature
        }

    @staticmethod
    def signed_request(user: Signer):
        """
        Returns a Totals request signed by the given signer. This method
        abstracts which parameters are signed by the signer.

        :param user:    client requesting pending UOMes.
        :return: Totals request signed by the client.
        """
        return TotalsRequest(
            user_id=user.id,
            signature=user.sign(user.id)
        )

    @staticmethod
    def load_request(request_body: bytes):
        parameters = Request._read_body(request_body)

        try:
            return TotalsRequest(
                user_id=str(parameters['user']).encode(),
                signature=str(parameters['signature']).encode()
            )

        except KeyError:
            raise RequestDecodeError("Totals request is missing at least one "
                                     "of its required parameters")

    @property
    def method(self) -> str:
        return "TOTALS"

    @property
    def parameters(self) -> dict:
        return self._parameters

    @property
    def user(self) -> bytes:
        return self._parameters['user']

    @property
    def signature(self) -> bytes:
        return self._parameters['signature']

