from pytest import raises

from utils.crypto.exceptions import InvalidSignature
from utils.requests.cancel_request import CancelRequest
from utils.requests.request import DecodeError, Request
from utils.requests.test_utils import fake_signer, fake_body, fake_verifier


class TestCancelRequest:

    def test_signed_request_ReturnsCorrectSignedCancelRequest(self):
        signer = fake_signer()
        request = CancelRequest.signed(
            borrower=signer,
            UOMe_id="1234",
        )

        assert request.borrower == b"C1"
        assert request.UOMe == "1234"
        assert request.signature == b"C11234"
        assert request.method == "CANCEL"

    def test_verify_ValidSignedRequest_DoesNotRaiseInvalidSignature(self):
        signed_request = CancelRequest.signed(
            borrower=fake_signer(),
            UOMe_id="1234",
        )

        verifier = fake_verifier()
        signed_request.verify(verifier)

    def test_verify_InvalidSignedRequest_RaiseInvalidSignature(self):
        invalid_signed_request = Request.load_request(fake_body({
            "borrower": "C3",
            "UOMe": "1234",
            "signature": "C11234",
        }), CancelRequest)

        verifier = fake_verifier()

        with raises(InvalidSignature):
            invalid_signed_request.verify(verifier)

    def test_load_request_RequestWithAllParameters_LoadsRequestWithValidParameters(self):
        request_body = fake_body({
            "borrower": "C1",
            "UOMe": "1234",
            "signature": "C11234",
        })

        request = Request.load_request(request_body, CancelRequest)

        assert request.borrower == b"C1"
        assert request.UOMe == "1234"
        assert request.signature == b"C11234"

    def test_load_request_RequestMissingOneParameter_RaisesDecodeError(self):
        request_body = fake_body({
            # missing user parameter
            "UOMe": "1234",
            "signature": "C11234",
        })

        with raises(DecodeError):
            Request.load_request(request_body, CancelRequest)
