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

    def test_verify_ValidSignedRequest_DoesNotRaiseInvalidSignature(self):
        signed_request = InviteRequest(
            inviter=example_pub_key,
            invitee="C2",
            invitee_email="c2@y.com"
        ).sign(example_key)

        signed_request.verify(signature=example_pub_key)

    def test_verify_InvalidSignedRequest_RaiseInvalidSignature(self):
        invalid_signed_request = InviteRequest.load(fake_body({
            "inviter": "C3",
            "invitee": "C2",
            "invitee_email": "c2@y.com",
            "signature": "C1C2c2@y.com",
        }))

        with raises(InvalidSignature):
            invalid_signed_request.verify(signature=example_pub_key)

    def test_load_request_RequestWithAllParameters_LoadsRequestWithValidParameters(self):
        request = InviteRequest.load(fake_body({
            "inviter": "C1",
            "invitee": "C2",
            "invitee_email": "c2@y.com",
            "signature": "sign1234",
        }))

        assert request.inviter == "C1"
        assert request.invitee == "C2"
        assert request.invitee_email == "c2@y.com"
        assert request.signature == "sign1234"

    def test_load_request_RequestMissingOneParameter_RaisesDecodeError(self):
        with raises(DecodeError):
            InviteRequest.load(fake_body({
                # missing inviter parameter
                "invitee": "C2",
                "invitee_email": "c2@y.com",
                "signature": "sign1234",
            }))

    def test_load_request_RequestWrongParameterType_RaisesDecodeError(self):
        with raises(DecodeError):
            InviteRequest.load(fake_body({
                "inviter": 101,  # should be str
                "invitee": "C2",
                "invitee_email": "c2@y.com",
                "signature": "sign1234",
            }))
