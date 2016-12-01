import base64

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

from utils.crypto.private_key import PrivateKey
from utils.crypto.public_key import PublicKey


class InvalidSignature(Exception):
    """ Raised when a verification of a signature fails. """

# cryptography suggests this value for
# the public exponent, stating that "65537 should almost always be used"
# However, 65537 is the most used value if we use a lower value with a good
# padding scheme we don't loose any security and gain more performance
# Using e=3 might improve performance by 8x
PUBLIC_EXPONENT = 65537
KEY_SIZE = 2048

def generate_keys() -> (PrivateKey, PublicKey):
    """
    Generates a pair of private and public keys

    :return: 2-tuple with the private and public key in this order.
    """
    raw_private_key = rsa.generate_private_key(
        public_exponent=PUBLIC_EXPONENT,
        key_size=KEY_SIZE,
        backend=default_backend()
    )

    return PrivateKey(raw_private_key), PublicKey(raw_private_key.public_key())


def load_keys(key_filepath) -> (PrivateKey, PublicKey):
    """
    Loads a pair of private and public keys from a key file in the PEM format.

    :param key_filepath: path to the key file in PEM format.
    :return: 2-tuple with the private and public key in this order.
    """
    with open(key_filepath, "rb") as key_file:
        raw_private_key = serialization.load_pem_private_key(
            data=key_file,
            password=None,
            backend=default_backend()
        )

    return PrivateKey(raw_private_key), PublicKey(raw_private_key.public_key())


def verify(encoded_public_key: bytes, signature: bytes, *data: bytes):
    """
    Using an encoded public key it verifies if the given signature is valid
    for this data. Data may be constituted by multiple parts, in that case,
    the data is concatenated before verification.

    :param encoded_public_key: public key in base64 format.
    :param signature: signature to check in base64 format.
    :param data: data in the usual bytes format.
    :raise InvalidSignature: if verification fails.
    """
    # decode public key to the usual bytes format
    encoded_public_key = base64.b64decode(encoded_public_key)

    public_key = serialization.load_pem_private_key(
        encoded_public_key,
        password=None,
        backend=default_backend()
    )

    return PublicKey(public_key).verify(signature, data)
