from utils.requests.parameters import identifier, signature
from utils.requests.request import Request


class InviteRequest(Request):
    """
    Invite request sent by a valid user to invite a new user into the group.
    """

    # The class field parameter_types defines the parameters and types of
    # the values of each parameter
    request_type = 'INVITE'

    parameter_types = {
        'inviter': str,
        'invitee': str,
        'invitee_email': str
    }

    format_to_sign = ['inviter', 'invitee', 'invitee_email']

    formats_to_verify = {
        "signature": format_to_sign,
    }
