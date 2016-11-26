import base64

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

from utils.crypto.private_key import PrivateKey
from utils.crypto.public_key import PublicKey


def generate_keys():
    """
    Generates a pair of private and public keys

    :return: 2-tuple with the private and public key in this order.
    """
    raw_private_key = rsa.generate_private_key(
        # do not change this value! cryptography suggests this value for
        # the public exponent, stating that "65537 should almost always be used"
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )

    return PrivateKey(raw_private_key), PublicKey(raw_private_key.public_key())


def load_keys(key_filepath):
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


def verify(encoded_public_key: bytes, data: bytes, signature: bytes):
    """
    Using an encoded public key it verifies if the given signature is valid
    for this data.

    :param encoded_public_key: public key in base64 format.
    :param data: data in the usual bytes format.
    :param signature: signature to check in base64 format.
    :return: True if the signature is valid and False if otherwise.
    """
    # decode public key to the usual bytes format
    encoded_public_key = base64.b64decode(encoded_public_key)

    public_key = serialization.load_pem_private_key(
        encoded_public_key,
        password=None,
        backend=default_backend()
    )

    return PublicKey(public_key).verify(data, signature)
