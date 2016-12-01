from pytest import raises

from utils.crypto.exceptions import InvalidSignature
from utils.requests.pending_request import PendingRequest
from utils.requests.request import DecodeError, Request
from utils.requests.test_utils import fake_signer, fake_body, fake_verifier


class TestPendingRequest:

    def test_signed_request_ReturnsCorrectSignedPendingRequest(self):
        signer = fake_signer()
        request = PendingRequest.signed(signer)

        assert request.user == b"C1"
        assert request.signature == b"C1"
        assert request.method == "PENDING"

    def test_verify_ValidSignedRequest_DoesNotRaiseInvalidSignature(self):
        signed_request = PendingRequest.signed(fake_signer())

        verifier = fake_verifier()
        signed_request.verify(verifier)

    def test_verify_InvalidSignedRequest_RaiseInvalidSignature(self):
        invalid_signed_request = Request.load_request(fake_body({
            "user": "C3",
            "signature": "C1",
        }), PendingRequest)

        verifier = fake_verifier()

        with raises(InvalidSignature):
            invalid_signed_request.verify(verifier)

    def test_load_request_RequestWithAllParameters_LoadsRequestWithValidParameters(self):
        request_body = fake_body({
            "user": "C1",
            "signature": "C1",
        })

        request = Request.load_request(request_body, PendingRequest)

        assert request.user == b"C1"
        assert request.signature == b"C1"

    def test_load_request_RequestMissingOneParameter_RaisesDecodeError(self):
        request_body = fake_body({
            # missing user parameter
            "signature": "C1",
        })

        with raises(DecodeError):
            Request.load_request(request_body, PendingRequest)
