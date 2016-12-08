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
    pass


def load_keys(key_filepath, password=None) -> (str, str):
    """
    Loads the private and public keys from a key file in the PEM format.
    Takes the password to decrypt the key file as an optional argument.

    :param key_filepath: path to the key file in PEM format.
    :param password:     password to decrypt the key file.
    :return: 2-tuple with the private and public key in string format.
    """
    pass


def sign(key: str, *values: str):
    """
    Signs a list of values with the given key.

    :param key:     private key used to sign the values.
    :param values:  list of values to sign.
    :return: signed values (signature)
    """
    pass


def verify(pubkey: str, signature: str, *values: str):
    """
    Verifies if a signature is valid. Expects the list of values included in
    the signature to be in the same order as they were signed. If the
    verification fails it raises an InvalidSignature exception.

    :param pubkey:      public key used to verify the signature.
    :param signature:   signature to verify.
    :param values:      values included in the signature.
    :return:
    :raise InvalidSignature: if the signature is invalid.
    """
    pass
