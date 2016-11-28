from utils.requests.signer import Signer
from utils.requests.request import Request, RequestDecodeError


class JoinRequest(Request):
    """
    Join request sent by a new user to join a group.
    """

    def __init__(self, user_id: bytes, secret_code: str, signature: bytes):
        """
        Initializer should not be directly called, instead use the
        signed_request() method.
        """
        self._parameters = {
            "user": user_id,
            "secret_code": secret_code,
            "signature": signature
        }

    @staticmethod
    def signed_request(joiner: Signer, secret_code: str):
        """
        Returns a Join request signed by the given signer. This method
        abstracts which parameters are signed by the signer.

        :param joiner:       client wanting to join.
        :param secret_code:  secret code to authenticate the join.
        :return: Join request signed by the joiner.
        """
        return JoinRequest(
            user_id=joiner.id,
            secret_code=secret_code,
            signature=joiner.sign(joiner.id)
        )

    @staticmethod
    def load_request(request_body: bytes):
        parameters = Request._body_to_parameters(request_body)

        try:
            return JoinRequest(
                user_id=str(parameters['user']).encode(),
                secret_code=str(parameters['secret_code']),
                signature=str(parameters['signature']).encode()
            )

        except KeyError:
            raise RequestDecodeError("Join request is missing at least one "
                                     "of its required parameters")

    @property
    def method(self) -> str:
        return "JOIN"

    @property
    def parameters(self) -> dict:
        return self._parameters

    @property
    def user(self) -> bytes:
        return self._parameters['user']

    @property
    def secret_code(self) -> str:
        return self._parameters['secret_code']

    @property
    def signature(self) -> bytes:
        return self._parameters['signature']

