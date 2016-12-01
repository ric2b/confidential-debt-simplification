import logging

from cryptography.exceptions import InvalidSignature

from utils.crypto import rsa
from utils.requests.ack_response import AckResponse
from utils.requests.confirm_join_request import ConfirmJoinRequest
from utils.requests.connection import Connection
from utils.requests.invite_request import InviteRequest
from utils.requests.join_request import JoinRequest
from utils.requests.join_response import JoinResponse
from utils.requests.signer import Signer


class SecurityError(Exception):
    """
    Raised by the client to indicate an error due to security as
    occurred.
    """

    def __init__(self, message):
        self.message = message


logger = logging.Logger(__name__)
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)


class Client(Signer):
    """ Interface for the client """

    def __init__(self, register_server_url: str,
                 register_server_key: str,
                 main_server_pubkey: str,
                 email: str, key_filepath=None):

        self.register_server_url = register_server_url
        self.register_server_key = register_server_key.encode()
        self.main_server_key = main_server_pubkey.encode()
        self.email = email

        if key_filepath:
            self.privkey, self.pubkey = rsa.load_keys(key_filepath)
        else:
            self.privkey, self.pubkey = rsa.generate_keys()

        self.proxy_server_address = ""
        self.proxy_server_pubkey = ""

    @property
    def id(self) -> bytes:
        """
        Returns the ID of the client. The ID of a client is a base64 string
        representation of its public key.
        """
        return bytes(self.pubkey)

    def sign(self, *data: bytes) -> bytes:
        """
        Takes a some data in bytes format and signs it using the client's
        private key. The returned signature can only be verified. It is not
        possible to decrypt the signature to obtain the signed data.

        :returns: signature for the given data in bytes format.
        """
        return self.privkey.sign(*data)

    def invite(self, invitee_id: str, invitee_email: str):
        """
        Invites a new client to the group.

        :param invitee_id: invited client's ID.
        :param invitee_email: invited client's email.
        """
        with Connection(self.register_server_url) as connection:
            request = InviteRequest.signed(
                inviter=self,
                invitee_id=invitee_id.encode(),
                invitee_email=invitee_email,
            )

            logger.debug("Sending 'invite' request for user id='%s' "
                         "email='%s'" % (invitee_id, invitee_email))
            connection.request(request)
            logger.debug("Finished sending request")

            connection.get_response(AckResponse)
            logger.info("Sent 'invite' to user id='%s' email='%s'" %
                        (invitee_id, invitee_email))

    def join(self, secret_code: str, inviter_id: str):
        """
        Tries to have the client join to a group.

        :param secret_code: secret code provided by email.
        :param inviter_id: ID of teh inviter.
        :raise SecurityError: if the main server signature or the inviter
                              signature do not verify.
        """
        # inviter ID is needed in bytes format
        # we expect a string since the inviter ID argument here comes
        # directly from the user input and that needs to be a string
        inviter_id = inviter_id.encode()

        with Connection(self.register_server_url) as connection:
            request = JoinRequest.signed(
                joiner=self,
                secret_code=secret_code
            )

            logger.debug("Sending 'join' request with code='%s'" % secret_code)
            connection.request(request)
            logger.debug("Finished sending request")

            response = connection.get_response(JoinResponse)  # type: JoinResponse

            # TODO should we keep the connection for the second request or
            # should we close and create a new one
            # Take into account that a TLS connection might take time

            try:
                logger.debug("Verifying the response...")

                response.verify(
                    inviter=inviter_id,
                    invitee=self.id,
                    invitee_email=self.email,
                    main_server_key=self.main_server_key,
                    register_server_key=self.register_server_key
                )

                logger.debug("Response was valid")

            except InvalidSignature:
                logger.warning("Response failed verification")
                raise SecurityError("There was an identify error with the "
                                    "response from the server")

            # TODO store signed invite from inviter
            # TODO store signed invite from request server

            confirm_request = ConfirmJoinRequest.signed(
                joiner=self,
                inviter_id=inviter_id,
                joiner_email=self.email
            )

            logger.debug("Sending 'confirm join'")
            connection.request(confirm_request)
            logger.debug("Finished sending request")

            connection.get_response(AckResponse)
            logger.info("Sent 'confirm join'")

    def issue_UOMe(self, borrower, amount):
        pass

    def pending_UOMes(self):
        pass

    def accept_UOMe(self, UOMe_number):
        pass

    def cancel_UOMe(self, UOMe_number):
        pass

    def totals(self):
        pass
