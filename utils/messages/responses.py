from utils.messages.message import Message


class RegisterGroup(Message):
    """
    Message sent to the Main server to register a new group and it's signing key
    """

    message_type = 'register-group'

    parameter_types = {
        'group_uuid': str,
        'group_name': str,
        'group_key': str,
        'main_signature': str
    }


class UserInvite(Message):
    """
    Invite request sent by a valid user to invite a new user into the group.
    """

    message_type = 'invite-user'

    parameter_types = {
        'group_signature': str
    }
