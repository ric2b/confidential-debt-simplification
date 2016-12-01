from utils.requests.request import Request, RequestDecodeError
from utils.requests.signer import Signer


class CancelRequest(Request):
    """
    Cancel request is sent by a user to accept a certain UOMe.
    """

    def __init__(self, borrower_id: bytes, UOMe_id: str, signature: bytes):
        """
        Initializer should not be directly called, instead use the
        signed_request() method.
        """
        self._parameters = {
            "borrower": borrower_id,
            "UOMe": UOMe_id,
            "signature": signature
        }

    @staticmethod
    def signed_request(borrower: Signer, UOMe_id: str):
        """
        Returns a Cancel request signed by the given signer. This method
        abstracts which parameters are signed by the signer.

        :param borrower:      client requesting pending UOMes.
        :param UOMe_id:     ID of the UOMe to accept.
        :return: Cancel request signed by the client.
        """
        return CancelRequest(
            borrower_id=borrower.id,
            UOMe_id=UOMe_id,
            signature=borrower.sign(borrower.id, UOMe_id.encode())
        )

    @staticmethod
    def load_request(request_body: bytes):
        parameters = Request._read_body(request_body)

        try:
            return CancelRequest(
                borrower_id=str(parameters['borrower']).encode(),
                UOMe_id=str(parameters['UOMe_id']),
                signature=str(parameters['signature']).encode()
            )

        except KeyError:
            raise RequestDecodeError("Cancel request is missing at least one "
                                     "of its required parameters")

    @property
    def method(self) -> str:
        return "CANCEL"

    @property
    def parameters(self) -> dict:
        return self._parameters

    @property
    def borrower(self) -> bytes:
        return self._parameters['borrower']

    @property
    def UOMe(self) -> str:
        return self._parameters['UOMe']

    @property
    def signature(self) -> bytes:
        return self._parameters['signature']

