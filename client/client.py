from utils.crypto import rsa


class Client:
    """ Interface for the client """

    def __init__(self, email: str, key_filepath=None):
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

    def invite(self, invitee, invitee_email):
        pass

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
