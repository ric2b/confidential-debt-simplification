from utils.requests.parameters import identifier, signature
from utils.requests.request import Request, DecodeError
from utils.requests.signer import Signer
from utils.requests.verifier import Verifier


class PendingRequest(Request):
    """
    Pending request is sent by a user to check its current pending UOMes.
    """

    # The class field parameter_types defines the parameters and types of
    # the values of each parameter
    parameters_types = {
        "user": identifier,
        "signature": signature,
    }

    @staticmethod
    def signed(signer: Signer):
        """
        Factory method for an Pending request. Use this method to create
        invite requests instead of the default initializer.

        Returns an Pending request signed by the given signer. This method
        abstracts which parameters are signed by the signer.

        :param signer: client requesting pending UOMes.
        :return: Pending request signed by the client.
        """
        parameters_values = {
            "user": signer.id,
            "signature": signer.sign(signer.id)
        }

        return PendingRequest(parameters_values)

    def verify(self, verifier: Verifier):
        """
        Verifies if the signatures in the join request are valid.

        :param verifier: verifier used to verify the signature.
        """
        verifier.verify(self.signature, self.user)

    @property
    def method(self) -> str:
        return "PENDING"

    @property
    def user(self) -> bytes:
        return self._parameters_values['user']

    @property
    def signature(self) -> bytes:
        return self._parameters_values['signature']

