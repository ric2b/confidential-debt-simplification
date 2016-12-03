from pytest import raises

from utils.crypto.exceptions import InvalidSignature
from utils.requests.confirm_join_request import ConfirmJoinRequest
from utils.requests.request import DecodeError, Request
from utils.requests.test_utils import fake_signer, fake_body, fake_verifier


class TestConfirmJoinRequest:
    def test_signed_request_ReturnsCorrectSignedConfirmJoinRequest(self):
        signer = fake_signer()
        request = ConfirmJoinRequest.signed(
            joiner=signer,
            inviter_id=b"C2",
            joiner_email="c1@y.com",
        )

        assert request.user == b"C1"
        assert request.signature == b"C2C1c1@y.com"
        assert request.method == "CONFIRM JOIN"

    def test_verify_ValidSignedRequest_DoesNotRaiseInvalidSignature(self):
        signed_request = ConfirmJoinRequest.signed(
            joiner=fake_signer(),
            inviter_id=b"C2",
            joiner_email="c1@y.com",
        )

        verifier = fake_verifier()
        signed_request.verify(verifier, inviter_id=b"C2",
                              joiner_email="c1@y.com")

    def test_verify_InvalidSignedRequest_RaiseInvalidSignature(self):
        invalid_signed_request = Request.load_request(fake_body({
            "user": "C3",
            "signature": "C2C1c1@y.com",
        }), ConfirmJoinRequest)

        verifier = fake_verifier()

        with raises(InvalidSignature):
            invalid_signed_request.verify(verifier, inviter_id=b"C2",
                                          joiner_email="c1@y.com")

    def test_load_request_RequestWithAllParameters_LoadsRequestWithValidParameters(
            self):
        request_body = fake_body({
            "user": "C1",
            "signature": "sign1234",
        })

        request = ConfirmJoinRequest.load_request(request_body,
                                                  ConfirmJoinRequest)

        assert request.user == b"C1"
        assert request.signature == b"sign1234"

    def test_load_request_RequestMissingOneParameter_RaisesDecodeError(self):
        request_body = fake_body({
            # missing user parameter
            "signature": "sign1234",
        })

        with raises(DecodeError):
            ConfirmJoinRequest.load_request(request_body, ConfirmJoinRequest)
