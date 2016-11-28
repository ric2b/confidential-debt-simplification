import json
from unittest.mock import Mock

from pytest import fixture


def fake_body(parameters: dict) -> bytes:
    """ Creates a fake request body from a dict with parameters """
    # there is no problem to use JSON directly to convert the parameters since
    # here it is not our goal to test the JSON format but input parameters
    return json.dumps(parameters).encode()


@fixture
def fake_signer():
    """
    Creates a fake signer with some predefined ID and which concatenates all
    data elements as a signature
    """

    def signature(*data):
        return b"".join(data)

    signer = Mock()
    signer.sign = Mock(side_effect=signature)
    signer.id = b"C1"
    return signer
