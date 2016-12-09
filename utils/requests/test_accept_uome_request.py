from pytest import raises

from utils.crypto.rsa import InvalidSignature
from utils.requests.accept_uome_request import AcceptUOMeRequest
from utils.requests.request import DecodeError, Request
from utils.requests.test_utils import example_key, example_pub_key, fake_body


class TestAcceptUOMeRequest:

    def test_signed_request_ReturnsCorrectSignedAcceptRequest(self):
        request = AcceptUOMeRequest(
            group_uuid="G1",
            user=example_key,
            loaner="C1",
            amount=10,
            UOMe_id=1234
        ).sign(example_key)

        assert request.group_uuid == "G1"
        assert request.user == example_key
        assert request.loaner == "C1"
        assert request.amount == 10
        assert request.UOMe_id == 1234
        assert request.method == "accept-uome"

        request.verify(signature=example_pub_key)

    def test_verify_ValidSignedRequest_DoesNotRaiseInvalidSignature(self):
        signed_request = AcceptUOMeRequest(
            group_uuid="G1",
            user=example_key,
            loaner="C1",
            amount=10,
            salt="salt",
            UOMe_id=1234
        ).sign(example_key)

        signed_request.verify(signature=example_pub_key)

    def test_verify_InvalidSignedRequest_RaiseInvalidSignature(self):
        invalid_signed_request = AcceptUOMeRequest.load(fake_body({
            "group_uuid": "G1",
            "user": "C2",
            "loaner": "C3",
            "amount": 10,
            "UOMe_id": 1234,
            "signature": "C2C110salt1234",
        }))

        with raises(InvalidSignature):
            invalid_signed_request.verify(signature=example_pub_key)

    def test_load_request_RequestWithAllParameters_LoadsRequestWithValidParameters(self):
        request_body = fake_body({
            "group_uuid": "G1",
            "user": "C2",
            "loaner": "C1",
            "amount": 10,
            "UOMe_id": 1234,
            "signature": "C2C110salt1234",
        })

        request = AcceptUOMeRequest.load(request_body)

        assert request.user == "C2"
        assert request.loaner == "C1"
        assert request.amount == 10
        assert request.UOMe_id == 1234
        assert request.signature == "C2C110salt1234"

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
            AcceptUOMeRequest.load(request_body)

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
            AcceptUOMeRequest.load(request_body)
