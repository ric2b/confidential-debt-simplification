from utils.requests.parameters import identifier, signature
from utils.requests.request import Request
from utils.requests.signer import Signer
from utils.requests.verifier import Verifier


class JoinRequest(Request):
    """
    Join request sent by a new user to join a group.
    """

    # The class field parameter_types defines the parameters and types of
    # the values of each parameter
    parameters_types = {
        "user": identifier,
        "secret_code": str,
        "signature": signature,
    }

    @staticmethod
    def signed(joiner: Signer, secret_code: str):
        """
        Factory method for an Join request. Use this method to create
        invite requests instead of the default initializer.

        Returns an Join request signed by the given signer. This method
        abstracts which parameters are signed by the signer.

        :param joiner:       client wanting to join.
        :param secret_code:  secret code to authenticate the join.
        :return: Join request signed by the joiner.
        """
        parameters_values = {
            "user": joiner.id,
            "secret_code": secret_code,
            "signature": joiner.sign(joiner.id)
        }

        return JoinRequest(parameters_values)

    def verify(self, verifier: Verifier):
        """
        Verifies if the signatures in the join request are valid.

        :param verifier: verifier used to verify the signature.
        """
        verifier.verify(self.signature, self.user)

    @property
    def method(self) -> str:
        return "JOIN"

    @property
    def user(self) -> bytes:
        return self._parameters_values['user']

    @property
    def secret_code(self) -> str:
        return self._parameters_values['secret_code']

    @property
    def signature(self) -> bytes:
        return self._parameters_values['signature']

