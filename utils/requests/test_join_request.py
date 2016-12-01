from pytest import raises

from utils.requests.join_request import JoinRequest
from utils.requests.request import Request
from utils.requests.test_utils import fake_signer, fake_body


class TestJoinRequest:

    def test_signed_request_ReturnsCorrectSignedJoinRequest(self):
        signer = fake_signer()
        request = JoinRequest.signed(
            joiner=signer,
            secret_code="$€cR€t",
        )

        assert request.user == b"C1"
        assert request.secret_code == "$€cR€t"
        assert request.signature == b"C1"
        assert request.method == "JOIN"

    def test_load_request_RequestWithAllParameters_LoadsRequestWithValidParameters(self):
        request_body = fake_body({
            "user": "C1",
            "secret_code": "$€cR€t",
            "signature": "sign1234",
        })

        request = Request.load_request(request_body, JoinRequest)

        assert request.user == b"C1"
        assert request.secret_code == "$€cR€t"
        assert request.signature == b"sign1234"

    def test_load_request_RequestMissingOneParameter_RaisesDecodeError(self):
        request_body = fake_body({
            # missing user parameter
            "secret_code": "$€cR€t",
            "signature": "sign1234",
        })

        with raises(DecodeError):
            Request.load_request(request_body, JoinRequest)
