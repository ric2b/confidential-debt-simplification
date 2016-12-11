from utils.requests.request import Request


class InviteRequest(Request):
    """
    Invite request sent by a valid user to invite a new user into the group.
    """

    request_address = 'invite-user'

    parameter_types = {
        'inviter': str,
        'invitee': str,
        'invitee_email': str
    }
