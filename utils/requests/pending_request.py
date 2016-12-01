from utils.requests.request import Request, RequestDecodeError
from utils.requests.signer import Signer


class PendingRequest(Request):
    """
    Pending request is sent by a user to check its current pending UOMes.
    """

    def __init__(self, user_id: bytes, signature: bytes):
        """
        Initializer should not be directly called, instead use the
        signed_request() method.
        """
        self._parameters = {
            "user": user_id,
            "signature": signature
        }

    @staticmethod
    def signed_request(signer: Signer):
        """
        Returns a Pending request signed by the given signer. This method
        abstracts which parameters are signed by the signer.

        :param signer: client requesting pending UOMes.
        :return: Pending request signed by the client.
        """
        return PendingRequest(
            user_id=signer.id,
            signature=signer.sign(signer.id)
        )

    @staticmethod
    def load_request(request_body: bytes):
        parameters = Request._read_body(request_body)

        try:
            return PendingRequest(
                user_id=str(parameters['user']).encode(),
                signature=str(parameters['signature']).encode()
            )

        except KeyError:
            raise RequestDecodeError("Pending request is missing at least one "
                                     "of its required parameters")

    @property
    def method(self) -> str:
        return "PENDING"

    @property
    def parameters(self) -> dict:
        return self._parameters

    @property
    def user(self) -> bytes:
        return self._parameters['user']

    @property
    def signature(self) -> bytes:
        return self._parameters['signature']

