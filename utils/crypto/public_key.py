import base64

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
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
        """
        Encrypts the given plain text, generating a cypher text in base 64
        format that can only be decrypted by the private key corresponding to
        this public key.

        :param plain_text: text to encrypt in usual bytes format.
        :return: cypher text in base64 format.
        """
        # Padding is done using the recommended OAEP scheme and not
        # legacy PKCS1v15
        cypher_text = self._public_key.encrypt(
            plain_text,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA1()),
                algorithm=hashes.SHA1(),
                label=None
            )
        )

        return base64.b64encode(cypher_text)

    def verify(self, signature: bytes, *data: bytes) -> bool:
        """
        Takes the original data and its signature and verifies if the
        signature is valid for the private key corresponding to this public
        key. Data may be constituted by multiple parts, in that case,
        the data is concatenated before verification.

        :param signature: signed data in base64 format.
        :param data: original data in the usual bytes format.
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

        # data must be concatenated before verifying
        concatenated_data = b"".join(data)
        verifier.update(concatenated_data)

        try:
            verifier.verify()
            # verification succeeded
            return True
        except InvalidSignature:
            # verification failed
            return False

    def dump(self, key_filepath):
        """
        Dumps the key into a file in PEM format.

        :param key_filepath: path to key file to store key on.
        """
        pem = self._public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

        with open(key_filepath, "w") as key_file:
            key_file.writelines(pem.splitlines())
