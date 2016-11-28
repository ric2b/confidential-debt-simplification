from pytest import raises

from utils.requests.UOMe_request import UOMeRequest
from utils.requests.request import RequestDecodeError
from utils.requests.test_utils import fake_signer, fake_body


class TestUOMeRequest:

    def test_signed_request_ReturnsCorrectSignedUOMeRequest(self):
        signer = fake_signer()
        request = UOMeRequest.signed_request(
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

    def test_load_request_RequestWithAllParameters_LoadsRequestWithValidParameters(self):
        request = UOMeRequest.load_request(fake_body({
            "borrower": "C1",
            "loaner": "C2",
            "amount": 10,
            "salt": "salt",
            "signature": "C1C210salt",
        }))

        assert request.borrower == b"C1"
        assert request.loaner == b"C2"
        assert request.amount == 10
        assert request.salt == "salt"
        assert request.signature == b"C1C210salt"

    def test_load_request_RequestMissingOneParameter_RaisesRequestDecodeError(self):
        with raises(RequestDecodeError):
            UOMeRequest.load_request(fake_body({
                # missing borrower parameter
                "loaner": "C2",
                "amount": 10,
                "salt": "salt",
                "signature": "C1C210salt",
            }))

    def test_load_request_RequestWithAmountNotAnInt_RaisesRequestDecodeError(self):
        with raises(RequestDecodeError):
            UOMeRequest.load_request(fake_body({
                "borrower": "C1",
                "loaner": "C2",
                "amount": [],  # should be an int but it's a list
                "salt": "salt",
                "signature": "C1C210salt",
            }))
