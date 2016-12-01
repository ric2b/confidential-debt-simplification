from utils.crypto.public_key import PublicKey


class Verifier:
    """
    A verifier is someone that can verify a signature.
    """

    @staticmethod
    def from_encoded_key(encoded_key):
        return DefaultVerifier(PublicKey.from_bytes(encoded_key))

    def verify(self, signature: bytes, *data: bytes):
        pass


class DefaultVerifier(Verifier):

    def __init__(self, pubkey: PublicKey):
        self.pubkey = pubkey

    def verify(self, signature: bytes, *data: bytes):
        self.pubkey.verify(signature, *data)
