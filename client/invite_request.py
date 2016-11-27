from client.request import Request, RequestDecodeError


class InviteRequest(Request):
    """
    Invite request sent by a valid user to invite a new user into the group.
    An invitation request contains three parameters:
        - inviter
        - invitee
        - invitee email
        - invite signed by the inviter
    """

    def __init__(self, inviter_id, invitee_id, invitee_email, inviter_signature):
        self.inviter_id = inviter_id
        self.invitee_id = invitee_id
        self.invitee_email = invitee_email
        self.inviter_signature = inviter_signature

    @staticmethod
    def load_request(request_body: bytes):
        parameters = Request.body_to_parameters(request_body)

        try:
            return InviteRequest(
                inviter_id=str(parameters['inviter']),
                invitee_id=str(parameters['invitee']),
                invitee_email=str(parameters['invitee_email']),
                inviter_signature=str(parameters['inviter_signature'])
            )

        except KeyError:
            raise RequestDecodeError("Invite request is missing at least one "
                                     "of its required parameters")

    @property
    def method(self) -> str:
        return "INVITE"

    @property
    def parameters(self) -> dict:
        return {
            "inviter": self.inviter_id,
            "invitee": self.invitee_id,
            "invitee_email": self.invitee_email,
            "inviter_signature": self.inviter_signature
        }

