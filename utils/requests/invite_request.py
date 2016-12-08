from utils.requests.parameters import identifier, signature
from utils.requests.request import Request
from utils.requests.signer import Signer
from utils.requests.verifier import Verifier


class InviteRequest(Request):
    """
    Invite request sent by a valid user to invite a new user into the group.
    """

    # The class field parameter_types defines the parameters and types of
    # the values of each parameter
    request_type = "INVITE"

    parameter_types = {
        "inviter": str,
        "invitee": str,
        "invitee_email": str
    }

    parameters_to_sign = ["inviter", "invitee", "invitee_email"]
