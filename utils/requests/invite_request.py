from utils.requests.message import Message


class InviteRequest(Message):
    """
    Invite request sent by a valid user to invite a new user into the group.
    """

    message_type = 'invite-user'

    parameter_types = {
        'inviter': str,
        'invitee': str,
        'invitee_email': str
    }
