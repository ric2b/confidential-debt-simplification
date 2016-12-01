from utils.requests.request import Request, RequestDecodeError
from utils.requests.signer import Signer


class ConfirmJoinRequest(Request):
    """
    Confirm Join request sent by a new user to confirm is joining a group.
    """

    def __init__(self, user_id: bytes, signed_invite: bytes):
        """
        Initializer should not be directly called, instead use the
        signed_request() method.
        """
        self._parameters = {
            "user": user_id,
            "signature": signed_invite
        }

    @staticmethod
    def signed_request(joiner: Signer, inviter_id: bytes, joiner_email: str):
        """
        Returns a Confirm Join request signed by the given signer. This method
        abstracts which parameters are signed by the signer.

        :param joiner:       client wanting to join.
        :param inviter_id:   ID of the original inviter.
        :param joiner_email: email of the client wanting to join.
        :return: Confirm Join request signed by the joiner.
        """
        return ConfirmJoinRequest(
            user_id=joiner.id,
            signed_invite=joiner.sign(inviter_id, joiner.id, joiner_email.encode())
        )

    @staticmethod
    def load_request(request_body: bytes):
        parameters = Request._read_body(request_body)

        try:
            return ConfirmJoinRequest(
                user_id=str(parameters['user']).encode(),
                signed_invite=str(parameters['signature']).encode()
            )

        except KeyError:
            raise RequestDecodeError("Confirm Join request is missing at least "
                                     "one of its required parameters")

    @property
    def method(self) -> str:
        return "CONFIRM JOIN"

    @property
    def parameters(self) -> dict:
        return self._parameters

    @property
    def user(self) -> bytes:
        return self._parameters['user']

    @property
    def signature(self) -> bytes:
        return self._parameters['signature']

