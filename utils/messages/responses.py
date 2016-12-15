from utils.messages.message import Message


class RegisterGroup(Message):
    """
    Message sent to the Main server to register a new group and it's signing key
    """

    message_type = 'register-group'

    parameter_types = {
        'group_uuid': str,
        'main_signature': str
    }


class GroupServerJoin(Message):
    """
    Sent to the Group server by a user to join a group in the Group server.
    This can only be done after the user receives his secret code by the e-mail the
    Group server sends after another user invites him.
    """

    message_type = 'join-group'

    parameter_types = {
        'group_uuid': str,
        'user': str,
        'secret_code': str,
        'inviter_signature': str
    }


class MainServerJoin(Message):
    """
    Sent to the Main Server by a user to join a group in the Main server.
    This can only be allowed after the user does a GroupServerJoin, so that the user
    can get his key signed by the group server.
    """

    message_type = 'join-group'

    parameter_types = {
        'group_uuid': str,
        'user': str,
        'user_signature': str,
        'group_server_signature': str
    }


class UserInvite(Message):
    """
    Invite request sent by a valid user to invite a new user into the group.
    """

    message_type = 'invite-user'

    parameter_types = {
        'group_signature': str
    }
