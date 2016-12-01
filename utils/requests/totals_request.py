from utils.requests.parameters import identifier, signature
from utils.requests.request import Request, DecodeError
from utils.requests.signer import Signer


class TotalsRequest(Request):
    """
    Totals request is sent by the user to obtain its totals.
    """

    # The class field parameter_types defines the parameters and types of
    # the values of each parameter
    parameters_types = {
        "user": identifier,
        "signature": signature,
    }

    @staticmethod
    def signed(user: Signer):
        """
        Factory method for an Pending request. Use this method to create
        invite requests instead of the default initializer.

        Returns an Pending request signed by the given signer. This method
        abstracts which parameters are signed by the signer.

        :param user:    client requesting pending UOMes.
        :return: Totals request signed by the client.
        """
        parameters_values = {
            "user": user.id,
            "signature": user.sign(user.id)
        }

        return TotalsRequest(parameters_values)

    @property
    def method(self) -> str:
        return "TOTALS"

    @property
    def parameters(self) -> dict:
        return self._parameters_values

    @property
    def user(self) -> bytes:
        return self._parameters_values['user']

    @property
    def signature(self) -> bytes:
        return self._parameters_values['signature']

