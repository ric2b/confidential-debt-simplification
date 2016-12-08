import base64

from cryptography import exceptions
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric import rsa

# cryptography suggests this value for
# the public exponent, stating that "65537 should almost always be used"
# However, 65537 is the most used value if we use a lower value with a good
# padding scheme we don't loose any security and gain more performance
# Using e=3 might improve performance by 8x
PUBLIC_EXPONENT = 65537

KEY_SIZE = 2048


class InvalidSignature(Exception):
    """ Raised when a verification of a signature fails. """


def generate_keys() -> (str, str):
    """
    Generates a pair of private and public keys

    :return: 2-tuple with the private and public key in string format.
    """
    key_object = rsa.generate_private_key(
        public_exponent=PUBLIC_EXPONENT,
        key_size=KEY_SIZE,
        backend=default_backend()
    )

    return _key_to_str(key_object), _pubkey_to_str(key_object.public_key())


def load_keys(key_filepath, password=None) -> (str, str):
    """
    Loads the private and public keys from a key file in the PEM format.
    Takes the password to decrypt the key file as an optional argument.

    :param key_filepath: path to the key file in PEM format.
    :param password:     password to decrypt the key file.
    :return: 2-tuple with the private and public key in string format.
    """
    with open(key_filepath, "rb") as key_file:
        key_object = serialization.load_pem_private_key(
            data=key_file.read(),
            password=None if password is None else password.encode(),
            backend=default_backend()
        )

    return _key_to_str(key_object), _pubkey_to_str(key_object.public_key())


def load_pubkey(key_filepath) -> str:
    """
    Loads a public key from a key file in the PEM format.
    Takes the password to decrypt the key file as an optional argument.

    :param key_filepath: path to the key file in PEM format.
    :return: public key in string format.
    """
    with open(key_filepath) as key_file:
        return _pem_to_str(key_file.read(), _PUBLIC_BEGIN_TAG, _PUBLIC_END_TAG)


def dump_key(key: str, key_filepath, password=None):
    """
    Dumps a private key to a key file in the PEM format.
    Takes the password to encrypt the key file as an optional argument.

    :param key:          private key to dump to file.
    :param key_filepath: path to the key file in PEM format.
    :param password:     password to encrypt the key file.
    """
    key_object = _str_to_key(key)

    if password:
        encryption = serialization.BestAvailableEncryption(password.encode())
    else:
        encryption = serialization.NoEncryption()

    pem = key_object.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=encryption
    )

    with open(key_filepath, "wb") as key_file:
        key_file.write(pem)


def dump_pubkey(pubkey: str, key_filepath):
    """
    Dumps a public key to a key file in the PEM format.
    Takes the password to encrypt the key file as an optional argument.

    :param pubkey:       public key to dump to file.
    :param key_filepath: path to the key file in PEM format.
    """
    with open(key_filepath, "wb") as key_file:
        key_file.write(_str_to_pem(pubkey, _PUBLIC_BEGIN_TAG, _PUBLIC_END_TAG))


def sign(key: str, *values: str) -> str:
    """
    Signs a list of values with the given key.

    :param key:     private key used to sign the values.
    :param values:  list of values to sign.
    :return: signature encoded in base 64.
    """
    key_object = _str_to_key(key)  # type: rsa.RSAPrivateKey

    signer = key_object.signer(
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

    signer.update("".join(values).encode())
    signature = signer.finalize()

    return base64.b64encode(signature).decode()


def verify(pubkey: str, signature: str, *values: str):
    """
    Verifies if a signature is valid. Expects the list of values included in
    the signature to be in the same order as they were signed. If the
    verification fails it raises an InvalidSignature exception.

    :param pubkey:      public key used to verify the signature.
    :param signature:   signature to verify encoded in base 64.
    :param values:      values included in the signature.
    :return:
    :raise InvalidSignature: if the signature is invalid.
    """
    # The signature is expected in base 64 and must be decoded
    signature = base64.b64decode(signature.encode())

    pubkey_object = _str_to_pubkey(pubkey)  # type: rsa.RSAPublicKey

    # Padding is done using the recommended PSS scheme and not
    # legacy PKCS1v15
    verifier = pubkey_object.verifier(
        signature,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

    verifier.update("".join(values).encode())

    try:
        verifier.verify()
    except exceptions.InvalidSignature:
        # raise custom invalid signature exception
        # hides the cryptographic library used
        raise InvalidSignature()


#
# Private functions
#

_PRIVATE_BEGIN_TAG = "-----BEGIN RSA PRIVATE KEY-----"
_PRIVATE_END_TAG = "-----END RSA PRIVATE KEY-----"
_PUBLIC_BEGIN_TAG = "-----BEGIN PUBLIC KEY-----"
_PUBLIC_END_TAG = "-----END PUBLIC KEY-----"

_LINE_LENGTH = 64


def _key_to_str(key_object: rsa.RSAPrivateKey) -> str:
    """ Converts a private key object to a string """
    pem = key_object.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )

    key_str = pem.decode()  # type: str
    key_str = key_str[len(_PRIVATE_BEGIN_TAG):]  # remove being tag
    key_str = key_str[:-(len(_PRIVATE_END_TAG) + 1)]  # remove end tag
    key_str = key_str.replace("\n", "")  # remove new lines

    return key_str


def _pubkey_to_str(pubkey_object: rsa.RSAPublicKey) -> str:
    """ Converts a public key object to a string """

    pem = pubkey_object.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    key_str = pem.decode()  # type: str
    key_str = key_str[len(_PUBLIC_BEGIN_TAG):]  # remove being tag
    key_str = key_str[:-(len(_PUBLIC_END_TAG) + 1)]  # remove end tag
    key_str = key_str.replace("\n", "")  # remove new lines

    return key_str


def _str_to_key(key: str) -> rsa.RSAPrivateKey:
    """ Converts a private key in string format to a private key object """

    key_object = serialization.load_pem_private_key(
        data=_str_to_pem(key, _PRIVATE_BEGIN_TAG, _PRIVATE_END_TAG),
        password=None,
        backend=default_backend()
    )

    return key_object


def _str_to_pubkey(pubkey: str) -> rsa.RSAPublicKey:
    """ Converts a public key in string format to a public key object """

    pubkey_object = serialization.load_pem_public_key(
        data=_str_to_pem(pubkey, _PUBLIC_BEGIN_TAG, _PUBLIC_END_TAG),
        backend=default_backend()
    )

    return pubkey_object


def _str_to_pem(key: str, begin_tag, end_tag) -> bytes:
    """ Converts a string key into byte string in PEM format """
    key_size = len(key)
    lines = []
    for i in range(0, key_size, 64):
        lines.append(key[i: i + 64])

    pem_key = "\n".join(lines)
    pem_key = begin_tag + "\n" + pem_key + "\n" + end_tag
    return pem_key.encode()

def _pem_to_str(pem_key: str, begin_tag, end_tag):
    """ Converts a pem key in PEM format to a string key """
    key_str = pem_key
    key_str = key_str[len(begin_tag):]  # remove being tag
    key_str = key_str[:-(len(end_tag) + 1)]  # remove end tag
    key_str = key_str.replace("\n", "")  # remove new lines

    return key_str
