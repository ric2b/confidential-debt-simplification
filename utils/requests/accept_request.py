from utils import bytesutils
from utils.requests.parameters import identifier, signature
from utils.requests.request import Request
from utils.requests.signer import Signer


class AcceptRequest(Request):
    """
    Accept request is sent by a user to accept a certain UOMe.
    """

    # The class field parameter_types defines the parameters and types of
    # the values of each parameter
    parameters_types = {
        "borrower": identifier,
        "loaner": identifier,
        "amount": int,
        "salt": str,
        "UOMe": str,
        "signature": signature,
    }

    @staticmethod
    def signed(borrower: Signer, loaner_id: bytes, amount: int,
               salt: str, UOMe_id: str):
        """
        Factory method for an Accept request. Use this method to create
        invite requests instead of the default initializer.

        Returns an Accept request signed by the given signer. This method
        abstracts which parameters are signed by the signer.

        :param borrower:    client requesting pending UOMes.
        :param loaner_id:   ID of the loaner.
        :param amount:      amount of the UOMe.
        :param salt:        random salt value (must be the same as the original)
        :param UOMe_id:     ID of the UOMe to accept.
        :return: Accept request signed by the client.
        """
        parameters_values = {
            "borrower": borrower.id,
            "loaner": loaner_id,
            "amount": amount,
            "salt": salt,
            "UOMe": UOMe_id,
            "signature": borrower.sign(
                loaner_id, borrower.id, bytesutils.from_int(amount),
                salt.encode(), UOMe_id.encode())
        }

        return AcceptRequest(parameters_values)

    @property
    def method(self) -> str:
        return "ACCEPT"

    @property
    def borrower(self) -> bytes:
        return self._parameters_values['borrower']

    @property
    def loaner(self) -> bytes:
        return self._parameters_values['loaner']

    @property
    def amount(self) -> int:
        return self._parameters_values['amount']

    @property
    def salt(self) -> str:
        return self._parameters_values['salt']

    @property
    def UOMe(self) -> str:
        return self._parameters_values['UOMe']

    @property
    def signature(self) -> bytes:
        return self._parameters_values['signature']
