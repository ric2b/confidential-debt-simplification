from pytest import raises

from utils.requests.accept_request import AcceptRequest
from utils.requests.request import RequestDecodeError, Request
from utils.requests.test_utils import fake_signer, fake_body


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

    def test_load_request_RequestMissingOneParameter_RaisesRequestDecodeError(self):
        request_body = fake_body({
            # missing borrower parameter
            "loaner": "C2",
            "amount": 10,
            "salt": "salt",
            "UOMe": "1234",
            "signature": "C2C110salt1234",
        })

        with raises(RequestDecodeError):
            Request.load_request(request_body, AcceptRequest)

    def test_load_request_RequestWithAmountNotAnInt_RaisesRequestDecodeError(self):
        request_body = fake_body({
            "borrower": "C1",
            "loaner": "C2",
            "amount": [],  # should be an int but it's a list
            "salt": "salt",
            "UOMe": "1234",
            "signature": "C2C110salt1234"
        })

        with raises(RequestDecodeError):
            Request.load_request(request_body, AcceptRequest)
