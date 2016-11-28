import json
from unittest.mock import Mock

from pytest import fixture
from pytest import raises

from utils.requests.invite_request import InviteRequest
from utils.requests.request import RequestDecodeError
from utils.requests.test_utils import fake_signer, fake_body


class TestInviteRequest:

    def test_signed_request_ReturnsCorrectSignedInviteRequest(self):
        signer = fake_signer()
        request = InviteRequest.signed_request(
            inviter=signer,
            invitee_id=b"C2",
            invitee_email="c2@y.com"
        )

        assert request.inviter == b"C1"
        assert request.invitee == b"C2"
        assert request.invitee_email == "c2@y.com"
        assert request.inviter_signature == b"C1C2c2@y.com"
        assert request.method == "INVITE"

    def test_load_request_RequestWithAllParameters_LoadsRequestWithValidParameters(self):
        request = InviteRequest.load_request(fake_body({
            "inviter": "C1",
            "invitee": "C2",
            "invitee_email": "c2@y.com",
            "inviter_signature": "sign1234",
        }))

        assert request.inviter == b"C1"
        assert request.invitee == b"C2"
        assert request.invitee_email == "c2@y.com"
        assert request.inviter_signature == b"sign1234"

    def test_load_request_RequestMissingOneParameter_RaisesRequestDecodeError(self):
        with raises(RequestDecodeError):
            InviteRequest.load_request(fake_body({
                # missing inviter parameter
                "invitee": "C2",
                "invitee_email": "c2@y.com",
                "inviter_signature": "sign1234",
            }))
