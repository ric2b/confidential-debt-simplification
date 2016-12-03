from utils import bytesutils
from utils.requests.parameters import identifier, signature
from utils.requests.request import Request
from utils.requests.signer import Signer
from utils.requests.verifier import Verifier


class UOMeRequest(Request):
    """
    UOMe request issued by a user loaning money to another user.
    """

    # The class field parameter_types defines the parameters and types of
    # the values of each parameter
    parameters_types = {
        "loaner": identifier,
        "borrower": identifier,
        "amount": int,
        "salt": str,
        "signature": signature,
    }

    @staticmethod
    def signed(loaner: Signer, borrower_id: bytes, amount: int,
               salt: str):
        """
        Factory method for an UOMe request. Use this method to create
        invite requests instead of the default initializer.

        Returns an UOMe request signed by the given signer. This method
        abstracts which parameters are signed by the signer

        :param loaner:       client who issues the UOMe.
        :param borrower_id:  ID of the borrower.
        :param amount:       amount loaned.
        :param salt:         random salt value.
        :return: UOMe request signed by the loaner.
        """
        parameters_values = {
            "loaner": loaner.id,
            "borrower": borrower_id,
            "amount": amount,
            "salt": salt,
            "signature": loaner.sign(loaner.id, borrower_id,
                                     bytesutils.from_int(amount), salt.encode())
        }

        return UOMeRequest(parameters_values)

    def verify(self, verifier: Verifier):
        """
        Verifies if the signatures in the join request are valid.

        :param verifier: verifier used to verify the signature.
        """
        verifier.verify(self.signature, self.loaner, self.borrower,
                        bytesutils.from_int(self.amount), self.salt.encode())

    @property
    def method(self) -> str:
        return "UOMe"

    @property
    def loaner(self) -> bytes:
        return self._parameters_values['loaner']

    @property
    def borrower(self) -> bytes:
        return self._parameters_values['borrower']

    @property
    def amount(self) -> int:
        return self._parameters_values['amount']

    @property
    def salt(self) -> str:
        return self._parameters_values['salt']

    @property
    def signature(self) -> bytes:
        return self._parameters_values['signature']

