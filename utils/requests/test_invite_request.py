from pytest import raises

from utils.crypto.exceptions import InvalidSignature
from utils.requests.invite_request import InviteRequest
from utils.requests.request import DecodeError, Request
from utils.requests.test_utils import fake_signer, fake_body, fake_verifier


class TestInviteRequest:

    def test_signed_request_ReturnsCorrectSignedInviteRequest(self):
        signer = fake_signer()
        request = InviteRequest(
            signer,
            inviter_id=signer.id,
            invitee_id=b"C2",
            invitee_email="c2@y.com"
        )

        assert request.inviter_id == b"C1"
        assert request.invitee_id == b"C2"
        assert request.invitee_email == "c2@y.com"
        assert request.signature == b"C1C2c2@y.com"
        assert request.method == "INVITE"

    def test_verify_ValidSignedRequest_DoesNotRaiseInvalidSignature(self):
        signer = fake_signer()
        signed_request = InviteRequest(
            signer,
            inviter_id=signer.id,
            invitee_id=b"C2",
            invitee_email="c2@y.com"
        )

        verifier = fake_verifier()
        signed_request.verify(verifier)

    def test_verify_InvalidSignedRequest_RaiseInvalidSignature(self):
        invalid_signed_request = InviteRequest.load_request(fake_body({
            "inviter_id": "C3",
            "invitee_id": "C2",
            "invitee_email": "c2@y.com",
            "signature": "C1C2c2@y.com",
        }), InviteRequest)

        verifier = fake_verifier()

        with raises(InvalidSignature):
            invalid_signed_request.verify(verifier)

    def test_load_request_RequestWithAllParameters_LoadsRequestWithValidParameters(self):
        request = InviteRequest.load_request(fake_body({
            "inviter": "C1",
            "invitee": "C2",
            "invitee_email": "c2@y.com",
            "inviter_signature": "sign1234",
        }), InviteRequest)

        assert request.inviter == "C1"
        assert request.invitee == "C2"
        assert request.invitee_email == "c2@y.com"
        assert request.signature == b"sign1234"

    def test_load_request_RequestMissingOneParameter_RaisesDecodeError(self):
        with raises(DecodeError):
            InviteRequest.load_request(fake_body({
                # missing inviter parameter
                "invitee": "C2",
                "invitee_email": "c2@y.com",
                "inviter_signature": "sign1234",
            }), InviteRequest)
