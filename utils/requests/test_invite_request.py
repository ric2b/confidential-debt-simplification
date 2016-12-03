from pytest import raises

from utils.crypto.exceptions import InvalidSignature
from utils.requests.invite_request import InviteRequest
from utils.requests.request import DecodeError, Request
from utils.requests.test_utils import fake_signer, fake_body, fake_verifier


class TestInviteRequest:

    def test_signed_request_ReturnsCorrectSignedInviteRequest(self):
        signer = fake_signer()
        request = InviteRequest.signed(
            inviter=signer,
            invitee_id=b"C2",
            invitee_email="c2@y.com"
        )

        assert request.inviter == b"C1"
        assert request.invitee == b"C2"
        assert request.invitee_email == "c2@y.com"
        assert request.inviter_signature == b"C1C2c2@y.com"
        assert request.method == "INVITE"

    def test_verify_ValidSignedRequest_DoesNotRaiseInvalidSignature(self):
        signed_request = InviteRequest.signed(
            inviter=fake_signer(),
            invitee_id=b"C2",
            invitee_email="c2@y.com"
        )

        verifier = fake_verifier()
        signed_request.verify(verifier)

    def test_verify_InvalidSignedRequest_RaiseInvalidSignature(self):
        invalid_signed_request = Request.load_request(fake_body({
            "inviter": "C3",
            "invitee": "C2",
            "invitee_email": "c2@y.com",
            "inviter_signature": "C1C2c2@y.com",
        }), InviteRequest)

        verifier = fake_verifier()

        with raises(InvalidSignature):
            invalid_signed_request.verify(verifier)

    def test_load_request_RequestWithAllParameters_LoadsRequestWithValidParameters(self):
        request = Request.load_request(fake_body({
            "inviter": "C1",
            "invitee": "C2",
            "invitee_email": "c2@y.com",
            "inviter_signature": "sign1234",
        }), InviteRequest)

        assert request.inviter == b"C1"
        assert request.invitee == b"C2"
        assert request.invitee_email == "c2@y.com"
        assert request.inviter_signature == b"sign1234"

    def test_load_request_RequestMissingOneParameter_RaisesDecodeError(self):
        with raises(DecodeError):
            Request.load_request(fake_body({
                # missing inviter parameter
                "invitee": "C2",
                "invitee_email": "c2@y.com",
                "inviter_signature": "sign1234",
            }), InviteRequest)
