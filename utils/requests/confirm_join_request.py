from utils.requests.parameters import identifier, signature
from utils.requests.request import Request, DecodeError
from utils.requests.signer import Signer
from utils.requests.verifier import Verifier


class ConfirmJoinRequest(Request):
    """
    Confirm Join request sent by a new user to confirm is joining a group.
    """

    # The class field parameter_types defines the parameters and types of
    # the values of each parameter
    parameters_types = {
        "user": identifier,
        "signature": signature,
    }

    @staticmethod
    def signed(joiner: Signer, inviter_id: bytes, joiner_email: str):
        """
        Factory method for an Confirm Join request. Use this method to create
        invite requests instead of the default initializer.

        Returns an Confirm Join request signed by the given signer. This method
        abstracts which parameters are signed by the signer.

        :param joiner:       client wanting to join.
        :param inviter_id:   ID of the original inviter.
        :param joiner_email: email of the client wanting to join.
        :return: Confirm Join request signed by the joiner.
        """
        parameters_values = {
            "user": joiner.id,
            "signature": joiner.sign(inviter_id, joiner.id, joiner_email.encode())
        }

        return ConfirmJoinRequest(parameters_values)

    def verify(self, verifier: Verifier, inviter_id: bytes, joiner_email: str):
        """
        Verifies if the signatures in the invite request are valid.

        :param verifier: verifier used to verify the signature.
        """
        verifier.verify(self.signature, inviter_id, self.user,
                        joiner_email.encode())

    @property
    def method(self) -> str:
        return "CONFIRM JOIN"

    @property
    def user(self) -> bytes:
        return self._parameters_values['user']

    @property
    def signature(self) -> bytes:
        return self._parameters_values['signature']

