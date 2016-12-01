from utils.requests.parameters import identifier, signature
from utils.requests.request import Request
from utils.requests.signer import Signer


class InviteRequest(Request):
    """
    Invite request sent by a valid user to invite a new user into the group.
    """

    # The class field parameter_types defines the parameters and types of
    # the values of each parameter
    parameters_types = {
        "inviter": identifier,
        "invitee": identifier,
        "invitee_email": str,
        "inviter_signature": signature,
    }

    @staticmethod
    def signed(inviter: Signer, invitee_id: bytes, invitee_email: str):
        """
        Factory method for an Invite request. Use this method to create
        invite requests instead of the default initializer.

        Returns an Invite request signed by the given signer. This method
        abstracts which parameters are signed by the signer.

        :param inviter:       client to send the invite.
        :param invitee_id:    ID of the invited client.
        :param invitee_email: email of the invited client.
        :return: Invite request signed by the inviter.
        """
        parameters_values = {
            "inviter": inviter.id,
            "invitee": invitee_id,
            "invitee_email": invitee_email,
            "inviter_signature": inviter.sign(inviter.id, invitee_id,
                                              invitee_email.encode())
        }

        return InviteRequest(parameters_values)

    @property
    def method(self) -> str:
        return "INVITE"

    @property
    def inviter(self) -> bytes:
        return self._parameters_values['inviter']

    @property
    def invitee(self) -> bytes:
        return self._parameters_values['invitee']

    @property
    def invitee_email(self) -> str:
        return self._parameters_values['invitee_email']

    @property
    def inviter_signature(self) -> bytes:
        return self._parameters_values['inviter_signature']
