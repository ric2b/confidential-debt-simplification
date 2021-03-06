import logging

import utils.messages.message_formats as msg
import uome
from utils.crypto import rsa
from utils.messages.connection import connect, ConflictError, ForbiddenError, \
    UnauthorizedError, NotFoundError


class ProtocolError(Exception):
    """ Raised when an error anticipated in the protocol """

    def __init__(self, message):
        self.message = message


class UserExistsError(ProtocolError):
    """ Raised when trying to add a client that already exists """
    pass


class PermissionDeniedError(ProtocolError):
    """
    Raised when a client does not have permission to execute some
    operation.
    """
    pass


class AuthenticationError(ProtocolError):
    """ Raised when the client fails to authenticate with the server """
    pass


class UOMeNotFoundError(ProtocolError):
    """ Raised when trying to access an UOMe-ID that does not exist """
    pass


logger = logging.Logger(__name__)
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)


class Client:
    """ Interface for the client """

    # default group ID
    GROUP_ID = "1"  # FIXME add support for multiple groups

    def __init__(self, group_server_url: str,
                 group_server_pubkey: str,
                 main_server_pubkey: str,
                 proxy_server_url: str,
                 email: str, key_path=None, keys=None):

        self.group_server_url = group_server_url
        self.group_server_pubkey = group_server_pubkey
        self.main_server_pubkey = main_server_pubkey
        self.proxy_server_url = proxy_server_url
        self.email = email

        if key_path:
            self.key, self.pubkey = rsa.load_keys(key_path)
        elif keys:
            self.key, self.pubkey = keys
        else:
            self.key, self.pubkey = rsa.generate_keys()

    @property
    def id(self) -> str:
        return self.pubkey

    def invite(self, invitee_id: str, invitee_email: str):
        """
        Invites a new user to the group.

        :param invitee_id: invited user's ID.
        :param invitee_email: invited user's email.
        :raise ClientExistsError: if invitee is already registered
        """
        # parameters that are common to the request and user signature
        parameters = {
            'invitee': invitee_id,
            'invitee_email': invitee_email
        }

        request = self._make_request(
            request_type=msg.UserInvite,
            request_params=parameters,
            signature_params=parameters
        )

        with connect(self.group_server_url) as connection:
            connection.request(request)

            try:
                # response can be ignored since it is only an acknowledgement
                connection.get_response(msg.UserInvite)

            except ConflictError:
                raise UserExistsError("Invited client is already registered")
            except ForbiddenError:
                raise PermissionDeniedError("Inviter is not registered")
            except UnauthorizedError:
                raise AuthenticationError("Signature verification failed")

    def join(self, secret_code: str, inviter_id: str):
        """
        Tries to have the client join a group.

        :param secret_code: secret code provided by email.
        :param inviter_id: ID of the inviter.
        """
        # parameters that are common to the request and user signature
        parameters = {'secret_code': secret_code}

        request = self._make_request(
            request_type=msg.GroupServerJoin,
            request_params=parameters,
            signature_params=parameters
        )

        with connect(self.group_server_url) as connection:
            connection.request(request)

            try:
                response = connection.get_response(msg.GroupServerJoin)

            except ConflictError:
                raise UserExistsError("User is already registered")
            except ForbiddenError:
                raise PermissionDeniedError("Secret code was not accepted")
            except UnauthorizedError:
                raise AuthenticationError("Signature verification failed")

            try:
                msg.GroupServerJoin.verify(
                    key=inviter_id,
                    signature_name='invite',
                    signature=response.inviter_signature,
                    group_uuid=self.GROUP_ID,
                    inviter=inviter_id,
                    user=self.id,
                    user_email=self.email,
                )

            except rsa.InvalidSignature:
                raise AuthenticationError("Inviter signature is invalid")

            try:
                msg.GroupServerJoin.verify(
                    key=self.group_server_pubkey,
                    signature_name='group',
                    signature=response.group_signature,
                    group_uuid=self.GROUP_ID,
                    inviter_signature=response.inviter_signature,
                )

            except rsa.InvalidSignature:
                raise AuthenticationError("Group server signature is invalid")

            return response.inviter_signature, response.group_signature

    def confirm_join(self, group_signature):
        """
        Sends a confirm join to the group server. This completes the joining
        process. It assumes that both the inviter and group signatures have
        already been verified. DO NOT CALL THIS METHOD WITH NON-VERIFIED
        SIGNATURES!

        :param group_signature: invite signed by the group server
        """
        request = self._make_request(
            request_type=msg.ConfirmJoin,
            signature_params={'group_server_signature': group_signature}
        )

        with connect(self.group_server_url) as connection:
            connection.request(request)

            try:
                # response can be ignored since it is only an acknowledgement
                connection.get_response(msg.ConfirmJoin)

            except ConflictError:
                raise UserExistsError("User is already confirmed")
            except ForbiddenError:
                raise PermissionDeniedError("User can not confirm join of "
                                            "another user")
            except UnauthorizedError:
                raise AuthenticationError("Signature verification failed")

    def issue_UOMe(self, borrower: str, value: int, description: str):
        # parameters that are common to the request and user signature
        parameters = {
            'borrower': borrower,
            'value': value,
            'description': description
        }

        request = self._make_request(
            request_type=msg.IssueUOMe,
            request_params=parameters,
            signature_params=parameters
        )

        with connect(self.proxy_server_url) as connection:
            connection.request(request)

            try:
                response = connection.get_response(msg.IssueUOMe)

            except ForbiddenError:
                raise PermissionDeniedError("User can not issue UOMes")
            except UnauthorizedError:
                raise AuthenticationError("Signature verification failed")

            try:
                msg.IssueUOMe.verify(
                    key=self.main_server_pubkey,
                    signature_name='main',
                    signature=response.main_signature,
                    uome_uuid=response.uome_uuid,
                    group_uuid=self.GROUP_ID,
                    user=self.id,
                    borrower=borrower,
                    value=str(value),
                    description=description,
                )

            except rsa.InvalidSignature:
                raise AuthenticationError("Main server signature is invalid")

            return response.uome_uuid, response.main_signature

    def confirm_UOMe(self, uome_uuid, borrower, value, description):

        request = self._make_request(
            request_type=msg.ConfirmUOMe,
            request_params={'uome_uuid': uome_uuid},
            signature_params={
                'uome_uuid': uome_uuid,
                'borrower': borrower,
                'value': value,
                'description': description,
            }
        )

        with connect(self.proxy_server_url) as connection:
            connection.request(request)

            # response can be ignored since it is only an acknowledgement
            connection.get_response(msg.ConfirmUOMe)

    def pending_UOMes(self):
        request = self._make_request(request_type=msg.GetPendingUOMes)

        with connect(self.proxy_server_url) as connection:
            connection.request(request)

            try:
                response = connection.get_response(msg.GetPendingUOMes)

            except UnauthorizedError:
                raise AuthenticationError("Signature verification failed")

            issued_by_user = list(map(uome.from_list, response.issued_by_user))
            waiting_for_user = list(map(uome.from_list, response.waiting_for_user))

            return issued_by_user, waiting_for_user

    def accept_UOMe(self, uome_uuid, loaner: str, value: int, description: str):
        # parameters that are common to the request and user signature

        request = self._make_request(
            request_type=msg.AcceptUOMe,
            request_params={'uome_uuid': uome_uuid},
            signature_params={
                'uome_uuid': uome_uuid,
                'issuer': loaner,
                'value': value,
                'description': description
            }
        )

        with connect(self.proxy_server_url) as connection:
            connection.request(request)

            try:
                response = connection.get_response(msg.AcceptUOMe)

            except NotFoundError:
                raise UOMeNotFoundError("There is not a UOMe with that ID")
            except ForbiddenError:
                raise PermissionDeniedError("User can not accept the UOMe")
            except UnauthorizedError:
                raise AuthenticationError("Signature verification failed")

            try:
                msg.AcceptUOMe.verify(
                    key=self.main_server_pubkey,
                    signature_name='main',
                    signature=response.main_signature,
                    group_uuid=self.GROUP_ID,
                    user=self.id,
                    uome_uuid=uome_uuid,
                )

                # TODO store signature
                # TODO store the UOMe-ID

            except rsa.InvalidSignature:
                raise AuthenticationError("Main server signature is invalid")

    def cancel_UOMe(self, UOMe_number):
        # parameters that are common to the request and user signature
        parameters = {'uome_uuid': UOMe_number}

        request = self._make_request(
            request_type=msg.CancelUOMe,
            request_params=parameters,
            signature_params=parameters
        )

        with connect(self.proxy_server_url) as connection:
            connection.request(request)

            try:
                response = connection.get_response(msg.CancelUOMe)

            except NotFoundError:
                raise UOMeNotFoundError("There is not a UOMe with that ID")
            except ForbiddenError:
                raise PermissionDeniedError("User can not cancel the UOMe")
            except UnauthorizedError:
                raise AuthenticationError("Signature verification failed")

            try:
                msg.CancelUOMe.verify(
                    key=self.main_server_pubkey,
                    signature_name='main',
                    signature=response.main_signature,
                    group_uuid=self.GROUP_ID,
                    user=self.id,
                    uome_uuid=UOMe_number,
                )

                # TODO store signature
                # TODO store the UOMe-ID

            except rsa.InvalidSignature:
                raise AuthenticationError("Main server signature is invalid")

    def totals(self):
        request = self._make_request(request_type=msg.CheckTotals)

        with connect(self.proxy_server_url) as connection:
            connection.request(request)

            try:
                response = connection.get_response(msg.CheckTotals)

            except ForbiddenError:
                raise PermissionDeniedError("User can not check totals")
            except UnauthorizedError:
                raise AuthenticationError("Signature verification failed")

            return response.user_balance, response.suggested_transactions

    def _make_request(self, request_type, request_params=None,
                      signature_params=None):

        if request_params is None:
            request_params = {}
        if signature_params is None:
            signature_params = {}

        signature_params['group_uuid'] = self.GROUP_ID
        signature_params['user'] = self.id

        request_params['group_uuid'] = self.GROUP_ID
        request_params['user'] = self.id
        request_params['user_signature'] = request_type.sign(
            key=self.key,
            signature_name='user',
            **signature_params
        )

        return request_type.make_request(**request_params)
