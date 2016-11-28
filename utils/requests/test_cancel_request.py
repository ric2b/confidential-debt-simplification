from pytest import raises

from utils.requests.cancel_request import CancelRequest
from utils.requests.request import RequestDecodeError
from utils.requests.test_utils import fake_signer, fake_body


class TestCancelRequest:

    def test_signed_request_ReturnsCorrectSignedCancelRequest(self):
        signer = fake_signer()
        request = CancelRequest.signed_request(
            borrower=signer,
            UOMe_id="1234",
        )

        assert request.borrower == b"C1"
        assert request.UOMe == "1234"
        assert request.signature == b"C11234"
        assert request.method == "CANCEL"

    def test_load_request_RequestWithAllParameters_LoadsRequestWithValidParameters(self):
        request = CancelRequest.load_request(fake_body({
            "borrower": "C1",
            "UOMe_id": "1234",
            "signature": "C11234",
        }))

        assert request.borrower == b"C1"
        assert request.UOMe == "1234"
        assert request.signature == b"C11234"

    def test_load_request_RequestMissingOneParameter_RaisesRequestDecodeError(self):
        with raises(RequestDecodeError):
            CancelRequest.load_request(fake_body({
                # missing user parameter
                "UOMe_id": "1234",
                "signature": "C11234",
            }))
