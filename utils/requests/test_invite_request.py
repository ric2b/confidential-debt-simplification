from pytest import raises

from utils.crypto.rsa import sign, verify, InvalidSignature
from utils.requests.invite_request import InviteRequest
from utils.requests.request import DecodeError, Request
from utils.requests.test_utils import example_key, example_pub_key, fake_body


class TestInviteRequest:

    def test_init_request_ReturnsCorrectInviteRequest(self):
        request = InviteRequest(
            inviter=example_pub_key,
            invitee="C2",
            invitee_email="c2@y.com"
        )

        assert request.inviter == example_pub_key
        assert request.invitee == "C2"
        assert request.invitee_email == "c2@y.com"
        assert request.method == "invite-user"

    def test_load_request_RequestWithAllParameters_LoadsRequestWithValidParameters(self):
        request = InviteRequest.load(fake_body({
            "inviter": "C1",
            "invitee": "C2",
            "invitee_email": "c2@y.com",
        }))

        assert request.inviter == "C1"
        assert request.invitee == "C2"
        assert request.invitee_email == "c2@y.com"

    def test_load_request_RequestMissingOneParameter_RaisesDecodeError(self):
        with raises(DecodeError):
            InviteRequest.load(fake_body({
                # missing inviter parameter
                "invitee": "C2",
                "invitee_email": "c2@y.com",
            }))

    def test_load_request_RequestWrongParameterType_RaisesDecodeError(self):
        with raises(DecodeError):
            InviteRequest.load(fake_body({
                "inviter": 101,  # should be str
                "invitee": "C2",
                "invitee_email": "c2@y.com",
            }))
