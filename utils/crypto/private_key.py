import base64


from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey


class PrivateKey:
    """
    Abstraction of a private key. Private keys can be used to sign or decrypt
    data. A public key can constructed from  a private key.
    """

    def __init__(self, private_key: RSAPrivateKey):
        """
        Initializes a private key from an RSAPrivateKey object. A private key
        should not be directly instantiated by the user.
        """
        self._private_key = private_key

    def decrypt(self, cypher_text: bytes) -> bytes:
        """
        Decrypts the given cypher text, extracting the plain text in bytes
        format.

        :param cypher_text: cypher text to decrypt in base64 format.
        :return: cypher text in the usual bytes format.
        """
        # The cypher text is expected in base 64 and must be decoded
        cypher_text = base64.b64decode(cypher_text)

        # Padding is done using the recommended OAEP scheme and not
        # legacy PKCS1v15
        plain_text = self._private_key.decrypt(
            cypher_text,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA1()),
                algorithm=hashes.SHA1(),
                label=None
            )
        )

        return plain_text

    def sign(self, *data: bytes) -> bytes:
        """
        Takes a some data in bytes format and signs it. The returned signature
        can only be verified. It is not possible to decrypt the signature to
        obtain the signed data. The signature is returned in base64 format.
        Data may be constituted by multiple parts, in that case, the data is
        concatenated before signing.

        :param data: data to sign in the usual bytes format.
        :returns: signature for the given data in base64 format.
        """
        # Data is hashed using SHA256 and then it is signed
        # Padding is done using the recommended PSS scheme and not
        # legacy PKCS1v15

        # create a signer for the key
        signer = self._private_key.signer(
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )

        signer.update(b"".join(data))
        signature = signer.finalize()

        return base64.b64encode(signature)

    def dump(self, key_filepath):
        """
        Dumps the key into a file in PEM format.

        :param key_filepath: path to key file to store key on.
        """
        # Question: Should the private key be stored encrypted?

        pem = self._private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        )

        with open(key_filepath, "w") as key_file:
            key_file.write(pem.decode())
