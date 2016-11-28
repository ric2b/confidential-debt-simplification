from pytest import raises

from utils.requests.confirm_join_request import ConfirmJoinRequest
from utils.requests.request import RequestDecodeError
from utils.requests.test_utils import fake_signer, fake_body


class TestConfirmJoinRequest:

    def test_signed_request_ReturnsCorrectSignedConfirmJoinRequest(self):
        signer = fake_signer()
        request = ConfirmJoinRequest.signed_request(
            joiner=signer,
            inviter_id=b"C2",
            joiner_email="c1@y.com",
        )

        assert request.user == b"C1"
        assert request.signature == b"C2C1c1@y.com"
        assert request.method == "CONFIRM JOIN"

    def test_load_request_RequestWithAllParameters_LoadsRequestWithValidParameters(self):
        request = ConfirmJoinRequest.load_request(fake_body({
            "user": "C1",
            "signature": "sign1234",
        }))

        assert request.user == b"C1"
        assert request.signature == b"sign1234"

    def test_load_request_RequestMissingOneParameter_RaisesRequestDecodeError(self):
        with raises(RequestDecodeError):
            ConfirmJoinRequest.load_request(fake_body({
                # missing user parameter
                "signature": "sign1234",
            }))
