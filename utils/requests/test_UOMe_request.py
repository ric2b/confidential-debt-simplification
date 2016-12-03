from pytest import raises

from utils.crypto.exceptions import InvalidSignature
from utils.requests.UOMe_request import UOMeRequest
from utils.requests.request import DecodeError, Request
from utils.requests.test_utils import fake_signer, fake_body, fake_verifier


class TestUOMeRequest:

    def test_signed_request_ReturnsCorrectSignedUOMeRequest(self):
        signer = fake_signer()
        request = UOMeRequest.signed(
            loaner=signer,
            borrower_id=B"C2",
            amount=10,
            salt="salt"
        )

        assert request.loaner == b"C1"
        assert request.borrower == b"C2"
        assert request.amount == 10
        assert request.salt == "salt"
        assert request.signature == b"C1C210salt"
        assert request.method == "UOMe"

    def test_verify_ValidSignedRequest_DoesNotRaiseInvalidSignature(self):
        signed_request = UOMeRequest.signed(
            loaner=fake_signer(),
            borrower_id=B"C2",
            amount=10,
            salt="salt"
        )

        verifier = fake_verifier()
        signed_request.verify(verifier)

    def test_verify_InvalidSignedRequest_RaiseInvalidSignature(self):
        invalid_signed_request = Request.load_request(fake_body({
            "borrower": "C3",
            "loaner": "C2",
            "amount": 10,
            "salt": "salt",
            "signature": "C1C210salt",
        }), UOMeRequest)

        verifier = fake_verifier()

        with raises(InvalidSignature):
            invalid_signed_request.verify(verifier)

    def test_load_request_RequestWithAllParameters_LoadsRequestWithValidParameters(self):
        request_body = fake_body({
            "borrower": "C1",
            "loaner": "C2",
            "amount": 10,
            "salt": "salt",
            "signature": "C1C210salt",
        })

        request = Request.load_request(request_body, UOMeRequest)

        assert request.borrower == b"C1"
        assert request.loaner == b"C2"
        assert request.amount == 10
        assert request.salt == "salt"
        assert request.signature == b"C1C210salt"

    def test_load_request_RequestMissingOneParameter_RaisesDecodeError(self):
        request_body = fake_body({
            # missing borrower parameter
            "loaner": "C2",
            "amount": 10,
            "salt": "salt",
            "signature": "C1C210salt",
        })

        with raises(DecodeError):
            Request.load_request(request_body, UOMeRequest)

    def test_load_request_RequestWithAmountNotAnInt_RaisesDecodeError(self):
        request_body = fake_body({
            "borrower": "C1",
            "loaner": "C2",
            "amount": [],  # should be an int but it's a list
            "salt": "salt",
            "signature": "C1C210salt",
        })

        with raises(DecodeError):
            Request.load_request(request_body, UOMeRequest)
