from utils.messages.message import Message


class RegisterGroup(Message):
    """
    Message sent to the Main server to register a new group and it's signing key
    """

    request_params = {
        'group_name': str,
        'group_key': str,
        'group_signature': str
    }

    response_params = {
        'group_uuid': str,
        'main_signature': str
    }

    signature_formats = {
        'group': ['group_name', 'group_key'],
        'main': ['group_uuid', 'group_name', 'group_key']
    }


class UserInvite(Message):
    """
    Invite request sent by a valid user to invite a new user into the group.
    """

    request_params = {
        'group_uuid': str,
        'inviter': str,
        'invitee': str,
        'invitee_email': str,
        'inviter_signature': str
    }

    response_params = {
        'group_signature': str
    }

    signature_formats = {
        'inviter': ['group_uuid', 'inviter', 'invitee', 'invitee_email'],
        'group': ['group_uuid', 'inviter', 'invitee', 'invitee_email']
    }


class GroupServerJoin(Message):
    """
    Sent to the Group server by a user to join a group in the Group server.
    This can only be done after the user receives his secret code by the e-mail the
    Group server sends after another user invites him.
    """

    request_params = {
        'group_uuid': str,
        'user': str,
        'secret_code': str,
        'user_signature': str
    }

    response_params = {
        'inviter': str,
        'user': str,
        'user_email': str,
        'inviter_signature': str,
        'group_signature': str
    }

    signature_formats = {
        'user': ['group_uuid', 'user', 'secret_code'],
        'invite': ['group_uuid', 'inviter', 'user', 'user_email'],
        'group': ['inviter_signature']
    }


class MainServerJoin(Message):
    """
    Sent to the Main Server by a user to join a group in the Main server.
    This can only be allowed after the user does a GroupServerJoin, so that the user
    can get his key signed by the group server.
    """

    request_params = {
        'group_uuid': str,
        'user': str,
        'user_signature': str,
        'group_signature': str
    }

    response_params = {
        'group_uuid': str,
        'user': str,
        'main_signature': str
    }

    signature_formats = {
        'user': ['group_uuid', 'user'],
        'group': ['group_uuid', 'user'],
        'main': ['group_uuid', 'user']
    }
