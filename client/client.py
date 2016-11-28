import logging

from utils.crypto import rsa
from utils.requests.ack_response import AckResponse
from utils.requests.connection import Connection
from utils.requests.invite_request import InviteRequest
from utils.requests.signer import Signer


logger = logging.Logger(__name__)
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)


class Client(Signer):
    """ Interface for the client """

    def __init__(self, server_url: str, email: str, key_filepath=None):
        self.server_url = server_url
        self.email = email

        if key_filepath:
            self.privkey, self.pubkey = rsa.load_keys(key_filepath)
        else:
            self.privkey, self.pubkey = rsa.generate_keys()

        self.proxy_server_address = ""
        self.proxy_server_pubkey = ""
        self.main_server_pubkey = ""

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
        return self.privkey.sign(data)

    def invite(self, invitee_id: str, invitee_email: str):
        """
        Invites a new client to the group.

        :param invitee_id: invited client's ID.
        :param invitee_email: invited client's email.
        """
        with Connection(self.server_url) as connection:
            request = InviteRequest.signed_request(
                inviter=self,
                invitee_id=invitee_id.encode(),
                invitee_email=invitee_email,
            )

            logger.debug("Sending 'invite' request for user id='%s' "
                         "email='%s'" % (invitee_id, invitee_email))
            connection.request(request)
            logger.debug("Finished sending invite")

            # TODO check for errors
            connection.get_response(AckResponse)
            logger.debug("Sent 'invite' to user id='%s' email='%s'" %
                         (invitee_id, invitee_email))

    def join(self, secret_code):
        pass

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
