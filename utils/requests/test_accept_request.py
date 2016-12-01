from pytest import raises

from utils.crypto.exceptions import InvalidSignature
from utils.requests.accept_request import AcceptRequest
from utils.requests.request import DecodeError, Request
from utils.requests.test_utils import fake_signer, fake_body, fake_verifier


class TestAcceptRequest:

    def test_signed_request_ReturnsCorrectSignedAcceptRequest(self):
        signer = fake_signer()
        request = AcceptRequest.signed(
            borrower=signer,
            loaner_id=B"C2",
            amount=10,
            salt="salt",
            UOMe_id="1234"
        )

        assert request.borrower == b"C1"
        assert request.loaner == b"C2"
        assert request.amount == 10
        assert request.salt == "salt"
        assert request.UOMe == "1234"
        assert request.signature == b"C2C110salt1234"
        assert request.method == "ACCEPT"

    def test_verify_ValidSignedRequest_DoesNotRaiseInvalidSignature(self):
        signed_request = AcceptRequest.signed(
            borrower=fake_signer(),
            loaner_id=B"C2",
            amount=10,
            salt="salt",
            UOMe_id="1234"
        )

        verifier = fake_verifier()
        signed_request.verify(verifier)

    def test_verify_InvalidSignedRequest_RaiseInvalidSignature(self):
        invalid_signed_request = Request.load_request(fake_body({
            "borrower": "C2",
            "loaner": "C3",
            "amount": 10,
            "salt": "salt",
            "UOMe": "1234",
            "signature": "C2C110salt1234",
        }), AcceptRequest)

        verifier = fake_verifier()

        with raises(InvalidSignature):
            invalid_signed_request.verify(verifier)

    def test_load_request_RequestWithAllParameters_LoadsRequestWithValidParameters(self):
        request_body = fake_body({
            "borrower": "C1",
            "loaner": "C2",
            "amount": 10,
            "salt": "salt",
            "UOMe": "1234",
            "signature": "C2C110salt1234",
        })

        request = Request.load_request(request_body, AcceptRequest)

        assert request.borrower == b"C1"
        assert request.loaner == b"C2"
        assert request.amount == 10
        assert request.salt == "salt"
        assert request.UOMe == "1234"
        assert request.signature == b"C2C110salt1234"

    def test_load_request_RequestMissingOneParameter_RaisesDecodeError(self):
        request_body = fake_body({
            # missing borrower parameter
            "loaner": "C2",
            "amount": 10,
            "salt": "salt",
            "UOMe": "1234",
            "signature": "C2C110salt1234",
        })

        with raises(DecodeError):
            Request.load_request(request_body, AcceptRequest)

    def test_load_request_RequestWithAmountNotAnInt_RaisesDecodeError(self):
        request_body = fake_body({
            "borrower": "C1",
            "loaner": "C2",
            "amount": [],  # should be an int but it's a list
            "salt": "salt",
            "UOMe": "1234",
            "signature": "C2C110salt1234"
        })

        with raises(DecodeError):
            Request.load_request(request_body, AcceptRequest)
