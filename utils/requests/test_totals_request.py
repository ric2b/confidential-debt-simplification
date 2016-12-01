from pytest import raises

from utils.requests.request import RequestDecodeError, Request
from utils.requests.test_utils import fake_signer, fake_body
from utils.requests.totals_request import TotalsRequest


class TestTotalsRequest:

    def test_signed_request_ReturnsCorrectSignedTotalsRequest(self):
        signer = fake_signer()
        request = TotalsRequest.signed(signer)

        assert request.user == b"C1"
        assert request.signature == b"C1"
        assert request.method == "TOTALS"

    def test_load_request_RequestWithAllParameters_LoadsRequestWithValidParameters(self):
        request_body = fake_body({
            "user": "C1",
            "signature": "C1",
        })

        request = Request.load_request(request_body, TotalsRequest)

        assert request.user == b"C1"
        assert request.signature == b"C1"

    def test_load_request_RequestMissingOneParameter_RaisesRequestDecodeError(self):
        request_body = fake_body({
            # missing user parameter
            "signature": "C1",
        })

        with raises(RequestDecodeError):
            Request.load_request(request_body, TotalsRequest)
