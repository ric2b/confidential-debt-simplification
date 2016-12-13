import json
from http.client import HTTPResponse
from unittest.mock import Mock, MagicMock

from pytest import fixture

from utils.crypto.rsa import generate_keys, InvalidSignature
from utils.messages.base64_json_encoder import Base64Encoder


example_key, example_pub_key = generate_keys()


def fake_body(parameters: dict) -> str:
    """ Creates a fake request body from a dict with parameters """
    # there is no problem to use JSON directly to convert the parameters since
    # here it is not our goal to test the JSON format but input parameters
    return json.dumps(parameters, cls=Base64Encoder)


def fake_http_response(status=200, body=bytes()) -> HTTPResponse:
    """
    Creates a fake HTTP response.

    :param status:  status code of the response.
    :param body:    body of the response in bytes
    :return: fake http response (mock object)
    """
    http_response = Mock()
    http_response.status = status
    http_response.read = MagicMock(return_value=body)

    # noinspection PyTypeChecker
    return http_response


def fake_signature(*data):
    return "".join(data)


@fixture
def fake_signer():
    """
    Creates a fake signer with some predefined ID and which concatenates all
    data elements as a signature
    """
    signer = Mock()
    signer.sign = Mock(side_effect=fake_signature)
    signer.id = b"C1"
    return signer


@fixture
def fake_verifier():
    """
    Creates a fake verifier to verify fake signatures from the fake signer.
    """

    def fake_verify(signature, *data):
        if signature != fake_signature(*data):
            raise InvalidSignature

    verifier = Mock()
    verifier.verify = Mock(side_effect=fake_verify)
    return verifier

