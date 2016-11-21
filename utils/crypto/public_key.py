import base64

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey


class PublicKey:
    """
    Abstraction of a public key. As opposed to private keys, public keys can
    verify a signature.
    """

    def __init__(self, public_key: RSAPublicKey):
        """
        Initializes a public key from an RSAPublicKey object. A public key
        should not be directly instantiated by the user.
        """
        self._public_key = public_key

    def encrypt(self, plain_text: bytes) -> bytes:
        pass

    def verify(self, data: bytes, signature: bytes) -> bool:
        """
        Takes the original data and its signature and verifies if the
        signature is valid for the private key corresponding to this public
        key.

        :param data: original data in the usual bytes format.
        :param signature: signed data in base64 format.
        :return: True if the signature is verified and False if otherwise.
        """
        # The signature is expected in base 64 and must be decoded
        signature = base64.b64decode(signature)

        # Padding is done using the recommended PSS scheme and not
        # legacy PKCS1v15
        verifier = self._public_key.verifier(
            signature,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )

        verifier.update(data)

        try:
            verifier.verify()
            # verification succeeded
            return True
        except InvalidSignature:
            # verification failed
            return False
