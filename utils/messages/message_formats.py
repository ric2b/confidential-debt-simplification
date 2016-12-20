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


class IssueUOMe(Message):
    """
    Sent to the Main Server by a user to issue a new, unconfirmed, UOMe.
    """

    request_params = {
        'group_uuid': str,
        'user': str,
        'borrower': str,
        'value': int,
        'description': str,
        'user_signature': str
    }

    response_params = {
        'uome_uuid': str,
        'main_signature': str
    }

    signature_formats = {
        'user': ['group_uuid', 'user', 'borrower', 'value', 'description'],
        'main': ['uome_uuid', 'group_uuid', 'user', 'borrower', 'value', 'description']
    }


class CancelUOMe(Message):
    """
    Sent to the Main Server by a user to cancel a still unconfirmed UOMe issued by him.
    This is mostly meant as a way to clean up old UOMe's that were never accepted.
    After the UOMe is confirmed by the user it cannot be deleted and both users should
    agree on issuing a UOMe in the opposite direction if it was indeed a mistake.
    """

    request_params = {
        'group_uuid': str,
        'user': str,
        'uome_uuid': str,
        'user_signature': str
    }

    response_params = {
        'main_signature': str
    }

    signature_formats = {
        'user': ['group_uuid', 'user', 'uome_uuid'],
        'main': ['group_uuid', 'user', 'uome_uuid']
    }


class PendingUOMes(Message):
    """
    Sent to the Main Server by a user to get all pending UOMe's associated with him.
    """

    request_params = {
        'group_uuid': str,
        'user': str,
        'user_signature': str
    }

    response_params = {
        'uome_list': list,
        'main_signature': str
    }

    signature_formats = {
        'user': ['group_uuid', 'user'],
        'main': ['group_uuid', 'user', 'uome_list'],
        'uome': ['group_uuid', 'user', 'borrower', 'value', 'description']
    }


class AcceptUOMe(Message):
    """
    Sent to the Main Server by a user to accept a pending UOMe's associated with him.
    """

    request_params = {
        'group_uuid': str,
        'lender': str,
        'user': str,
        'value': int,
        'uome_uuid': str,
        'description': str,
        'user_signature': str
    }

    response_params = {
        'main_signature': str
    }

    signature_formats = {
        'user': ['group_uuid', 'lender', 'user', 'value', 'description', 'uome_uuid'],
        'main': ['group_uuid', 'user', 'uome_uuid']
    }


class CheckTotals(Message):
    """
    Sent to the Main Server by a user to get his total debt and the suggested amounts
    he should pay to each person.
    """
    # TODO: From my experience in my group of friends it would also be useful to list
    # the users to whom the user can pay his debt in full, trading global optimality for
    # individual practicality. This of course could reveal more information about
    # all the users in the group. Probably for after the course is done.

    request_params = {
        'group_uuid': str,
        'user': str,
        'user_signature': str
    }

    response_params = {
        'user_balance': int,
        'suggested_transactions': dict,
        'main_signature': str
    }

    signature_formats = {
        'user': ['group_uuid', 'user'],
        'main': ['group_uuid', 'user', 'user_balance', 'suggested_transactions']
    }

    # Sign the JSON string version of 'suggested_transactions'.
