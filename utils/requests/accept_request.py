from utils import bytesutils
from utils.requests.request import Request, RequestDecodeError
from utils.requests.signer import Signer


class AcceptRequest(Request):
    """
    Accept request is sent by a user to accept a certain UOMe.
    """

    def __init__(self, borrower_id: bytes, loaner_id: bytes, amount: int,
                 salt: str, UOMe_id: str, signature: bytes):
        """
        Initializer should not be directly called, instead use the
        signed_request() method.
        """
        self._parameters = {
            "borrower": borrower_id,
            "loaner": loaner_id,
            "amount": amount,
            "salt": salt,
            "UOMe": UOMe_id,
            "signature": signature
        }

    @staticmethod
    def signed_request(borrower: Signer, loaner_id: bytes, amount: int,
                       salt: str, UOMe_id: str):
        """
        Returns a Accept request signed by the given signer. This method
        abstracts which parameters are signed by the signer.

        :param borrower:    client requesting pending UOMes.
        :param loaner_id:   ID of the loaner.
        :param amount:      amount of the UOMe.
        :param salt:        random salt value (must be the same as the original)
        :param UOMe_id:     ID of the UOMe to accept.
        :return: Accept request signed by the client.
        """
        return AcceptRequest(
            borrower_id=borrower.id,
            loaner_id=loaner_id,
            amount=amount,
            salt=salt,
            UOMe_id=UOMe_id,
            signature=borrower.sign(loaner_id, borrower.id,
                                    bytesutils.from_int(amount), salt.encode(),
                                    UOMe_id.encode())
        )

    @staticmethod
    def load_request(request_body: bytes):
        parameters = Request._body_to_parameters(request_body)

        try:
            return AcceptRequest(
                borrower_id=str(parameters['borrower']).encode(),
                loaner_id=str(parameters['loaner']).encode(),
                amount=int(parameters['amount']),
                salt=str(parameters['salt']),
                UOMe_id=str(parameters['UOMe_id']),
                signature=str(parameters['signature']).encode()
            )

        except TypeError:
            raise RequestDecodeError("Amount must be an integer value")

        except KeyError:
            raise RequestDecodeError("Accept request is missing at least one "
                                     "of its required parameters")

    @property
    def method(self) -> str:
        return "ACCEPT"

    @property
    def parameters(self) -> dict:
        return self._parameters

    @property
    def borrower(self) -> bytes:
        return self._parameters['borrower']

    @property
    def loaner(self) -> bytes:
        return self._parameters['loaner']

    @property
    def amount(self) -> int:
        return self._parameters['amount']

    @property
    def salt(self) -> str:
        return self._parameters['salt']

    @property
    def UOMe(self) -> str:
        return self._parameters['UOMe']

    @property
    def signature(self) -> bytes:
        return self._parameters['signature']

