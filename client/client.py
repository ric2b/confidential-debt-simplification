import logging

from cryptography.exceptions import InvalidSignature

from utils.crypto import rsa


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


class Client:
    """ Interface for the client """

    def __init__(self, group_server_url: str,
                 group_server_pubkey: str,
                 main_server_pubkey: str,
                 email: str, key_filepath=None):

        self.group_server_url = group_server_url
        self.group_server_pubkey = group_server_pubkey
        self.main_server_pubkey = main_server_pubkey
        self.email = email

        if key_filepath:
            self.privkey, self.pubkey = rsa.load_keys(key_filepath)
        else:
            self.privkey, self.pubkey = rsa.generate_keys()

        self.proxy_server_address = ""
        self.proxy_server_pubkey = ""

    @property
    def id(self) -> str:
        return self.pubkey

    def invite(self, invitee_id: str, invitee_email: str):
        """
        Invites a new client to the group.

        :param invitee_id: invited client's ID.
        :param invitee_email: invited client's email.
        """
        pass

    def join(self, secret_code: str, inviter_id: str):
        """
        Tries to have the client join to a group.

        :param secret_code: secret code provided by email.
        :param inviter_id: ID of the inviter.
        :raise SecurityError: if the main server signature or the inviter
                              signature do not verify.
        """
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
