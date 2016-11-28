"""
This module contains multiple functions to handle bytes and to convert
between bytes and other data types.
"""


def from_int(value: int) -> bytes:
    """ Converts an int value into bytes """
    return str(value).encode()
