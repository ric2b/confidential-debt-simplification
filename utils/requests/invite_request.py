from utils.requests.request import Request, RequestDecodeError
from utils.requests.signer import Signer


class InviteRequest(Request):
    """
    Invite request sent by a valid user to invite a new user into the group.
    """

    def __init__(self, inviter_id: bytes, invitee_id: bytes, invitee_email: str,
                 inviter_signature: bytes):
        """
        Initializer should not be directly called, instead use the
        signed_request() method.
        """
        self._parameters = {
            "inviter": inviter_id,
            "invitee": invitee_id,
            "invitee_email": invitee_email,
            "inviter_signature": inviter_signature
        }

    @staticmethod
    def signed_request(inviter: Signer, invitee_id: bytes, invitee_email: str):
        """
        Returns an Invite request signed by the given signer. This method
        abstracts which parameters are signed by the signer.

        :param inviter:       client to send the invite.
        :param invitee_id:    ID of the invited client.
        :param invitee_email: email of the invited client.
        :return: Invite request signed by the inviter.
        """
        return InviteRequest(
            inviter_id=inviter.id,
            invitee_id=invitee_id,
            invitee_email=invitee_email,
            inviter_signature=inviter.sign(inviter.id, invitee_id,
                                           invitee_email.encode())
        )

    @staticmethod
    def load_request(request_body: bytes):
        parameters = Request._read_body(request_body)
        print(parameters)

        try:
            return InviteRequest(
                inviter_id=str(parameters['inviter']).encode(),
                invitee_id=str(parameters['invitee']).encode(),
                invitee_email=str(parameters['invitee_email']),
                inviter_signature=str(parameters['inviter_signature']).encode()
            )

        except KeyError:
            raise RequestDecodeError("Invite request is missing at least one "
                                     "of its required parameters")

    @property
    def method(self) -> str:
        return "INVITE"

    @property
    def parameters(self) -> dict:
        return self._parameters

    @property
    def inviter(self) -> bytes:
        return self._parameters['inviter']

    @property
    def invitee(self) -> bytes:
        return self._parameters['invitee']

    @property
    def invitee_email(self) -> str:
        return self._parameters['invitee_email']

    @property
    def inviter_signature(self) -> bytes:
        return self._parameters['inviter_signature']
