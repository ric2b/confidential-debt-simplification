from utils.requests.parameters import identifier, signature
from utils.requests.request import Request, DecodeError
from utils.requests.signer import Signer


class CancelRequest(Request):
    """
    Cancel request is sent by a user to accept a certain UOMe.
    """

    # The class field parameter_types defines the parameters and types of
    # the values of each parameter
    parameters_types = {
        "borrower": identifier,
        "UOMe": str,
        "signature": signature,
    }

    @staticmethod
    def signed(borrower: Signer, UOMe_id: str):
        """
        Factory method for an Cancel request. Use this method to create
        invite requests instead of the default initializer.

        Returns an Cancel request signed by the given signer. This method
        abstracts which parameters are signed by the signer.

        :param borrower: client requesting pending UOMes.
        :param UOMe_id:  ID of the UOMe to accept.
        :return: Cancel request signed by the client.
        """
        parameters_values = {
            "borrower": borrower.id,
            "UOMe": UOMe_id,
            "signature": borrower.sign(borrower.id, UOMe_id.encode())
        }

        return CancelRequest(parameters_values)

    @property
    def method(self) -> str:
        return "CANCEL"

    @property
    def parameters(self) -> dict:
        return self._parameters_values

    @property
    def borrower(self) -> bytes:
        return self._parameters_values['borrower']

    @property
    def UOMe(self) -> str:
        return self._parameters_values['UOMe']

    @property
    def signature(self) -> bytes:
        return self._parameters_values['signature']

