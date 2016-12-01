from utils import bytesutils
from utils.requests.request import Request, RequestDecodeError
from utils.requests.signer import Signer


class UOMeRequest(Request):
    """
    UOMe request issued by a user loaning money to another user.
    """

    def __init__(self, loaner_id: bytes, borrower_id: bytes, amount: int,
                 salt: str, signature: bytes):
        """
        Initializer should not be directly called, instead use the
        signed_request() method.
        """
        self._parameters = {
            "loaner": loaner_id,
            "borrower": borrower_id,
            "amount": amount,
            "salt": salt,
            "signature": signature
        }

    @staticmethod
    def signed_request(loaner: Signer, borrower_id: bytes, amount: int,
                       salt: str):
        """
        Returns a UOMe request signed by the given signer. This method
        abstracts which parameters are signed by the signer.

        :param loaner:       client who issues the UOMe.
        :param borrower_id:  ID of the borrower.
        :param amount:       amount loaned.
        :param salt:         random salt value.
        :return: UOMe request signed by the loaner.
        """
        return UOMeRequest(
            loaner_id=loaner.id,
            borrower_id=borrower_id,
            amount=amount,
            salt=salt,
            signature=loaner.sign(loaner.id, borrower_id,
                                  bytesutils.from_int(amount), salt.encode())
        )

    @staticmethod
    def load_request(request_body: bytes):
        parameters = Request._read_body(request_body)

        try:
            return UOMeRequest(
                loaner_id=str(parameters['loaner']).encode(),
                borrower_id=str(parameters['borrower']).encode(),
                amount=int(parameters['amount']),
                salt=str(parameters['salt']),
                signature=str(parameters['signature']).encode()
            )

        except TypeError:
            raise RequestDecodeError("Amount must be an integer value")

        except KeyError:
            raise RequestDecodeError("UOMe request is missing at least one "
                                     "of its required parameters")

    @property
    def method(self) -> str:
        return "UOMe"

    @property
    def parameters(self) -> dict:
        return self._parameters

    @property
    def loaner(self) -> bytes:
        return self._parameters['loaner']

    @property
    def borrower(self) -> bytes:
        return self._parameters['borrower']

    @property
    def amount(self) -> int:
        return self._parameters['amount']

    @property
    def salt(self) -> str:
        return self._parameters['salt']

    @property
    def signature(self) -> bytes:
        return self._parameters['signature']

