"""
Parameters module contains a set of functions to check parameter types and to
convert between support formats
"""


def _bytes_parameter(value) -> bytes:
    """
    Base function to support bytes parameters. The value can be a string or
    a byte string. Expects the input to be in base 64 (independently of
    the format). If the input value is of any other type it raises a TypeError.

    :param value: value as a string or bytes string (encoded in base 64)
    :return: value in bytes format.
    :raise TypeError: if the input value is not a string or bytes string.
    """
    if isinstance(value, str):
        return value.encode()

    if not isinstance(value, bytes):
        raise TypeError("ID parameter requires base64 encoding in "
                        "bytes format")

    return value


def identifier(value) -> bytes:
    """
    Identifier parameters are used for the users' IDs. They can be a string
    or a byte string. Expects the input to be in base 64 (independently of
    the format). If the input value is of any other type it raises a TypeError.

    :param value: value as a string or bytes string (encoded in base 64)
    :return: value in bytes format.
    :raise TypeError: if the input value is not a string or bytes string.
    """
    return _bytes_parameter(value)


def integer(value) -> int:
    try:
        return int(value)
    except ValueError:
        raise TypeError


def signature(value) -> bytes:
    """
    Signature parameters are used for signed string. They can be a string
    or a byte string. Expects the input to be in base 64 (independently of
    the format). If the input value is of any other type it raises a
    TypeError.

    :param value: value as a string or bytes string (encoded in base 64)
    :return: value in bytes format.
    :raise TypeError: if the input value is not a string or bytes string.
    """
    return _bytes_parameter(value)


def entries(values_types: dict):
    """
    Takes a dictionary with parameters and the respective value types.
    Returns the function type for the parameters.

    :param values_types:
    :return:
    """
    return Entries(values_types).parse


class Entries:

    def __init__(self, values_types: dict):
        self.values_types = values_types

    def parse(self, entries: list):

        if not isinstance(entries, list):
            raise TypeError

        parsed_entries = []
        for entry in entries:
            values = {}
            for parameter, param_type in self.values_types.items():
                values[parameter] = param_type(entry[parameter])

            parsed_entries.append(values)

        return parsed_entries
