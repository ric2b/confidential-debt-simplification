from pytest import raises

from utils.requests.pending_response import PendingResponse
from utils.requests.response import DecodeError, Response
from utils.requests.test_utils import fake_body, fake_http_response


class TestPendingResponse:
    #
    # Tests for the from_parameters() method
    #

    def test_ValidResponseWithCorrectFormattingAndOneEntry_PendingResponseWithEntry(self):
        http_response = fake_http_response(body=fake_body({
            "response": "PENDING",
            "entries": [
                {
                    "UOMe": "#1234",
                    "loaner": "C1",
                    "borrower": "C2",
                    "amount": 1000,
                    "salt": "1234",
                    "loaner_signature": "df4r2"
                }
            ]
        }))

        response = Response.load_response(http_response, PendingResponse)

        assert response.entries == [
            {
                "UOMe": "#1234",
                "loaner": b"C1",
                "borrower": b"C2",
                "amount": 1000,
                "salt": "1234",
                "loaner_signature": b"df4r2"
            }
        ]

    def test_ResponseMissingTheResponseParameter_RaisesResponseError(self):
        http_response = fake_http_response(body=fake_body({
            "entries": [
                {
                    "UOMe": "#1234",
                    "loaner": "C1",
                    "borrower": "C2",
                    "amount": 1000,
                    "salt": "1234",
                    "loaner_signature": "df4r2"
                }
            ]
        }))

        expected_message = "Response was missing some parameters"
        with raises(DecodeError, message=expected_message):
            Response.load_response(http_response, PendingResponse)

    def test_ResponseWithIncorrectMethod_RaisesResponseError(self):
        http_response = fake_http_response(body=fake_body({
            "response": "INCORRECT",
            "entries": [
                {
                    "UOMe": "#1234",
                    "loaner": "C1",
                    "borrower": "C2",
                    "amount": 1000,
                    "salt": "1234",
                    "loaner_signature": "df4r2"
                }
            ]
        }))

        expected_message = "Response method does not match"
        with raises(DecodeError, message=expected_message):
            Response.load_response(http_response, PendingResponse)

    def test_ResponseMethodIsAnInt_RaisesResponseError(self):
        http_response = fake_http_response(body=fake_body({
            "response": 1234,
            "entries": [
                {
                    "UOMe": "#1234",
                    "loaner": "C1",
                    "borrower": "C2",
                    "amount": 1000,
                    "salt": "1234",
                    "loaner_signature": "df4r2"
                }
            ]
        }))

        expected_message = "Parameters are of incorrect type"
        with raises(DecodeError, message=expected_message):
            Response.load_response(http_response, PendingResponse)

    def test_ResponseEntriesIsNotAList_RaisesResponseError(self):
        http_response = fake_http_response(body=fake_body({
            "response": "PENDING",
            "entries": "value"
        }))

        expected_message = "Parameters are of incorrect type"
        with raises(DecodeError, message=expected_message):
            Response.load_response(http_response, PendingResponse)

    def test_ResponseEntryMissesOneParameter_RaisesResponseError(
            self):
        http_response = fake_http_response(body=fake_body({
            "response": "PENDING",
            "entries": [
                {
                    # misses the ID
                    "loaner": "C1",
                    "borrower": "C2",
                    "amount": 1000,
                    "salt": "1234",
                    "loaner_signature": "df4r2"
                }
            ]
        }))

        expected_message = "Parameters are of incorrect type"
        with raises(DecodeError, message=expected_message):
            Response.load_response(http_response, PendingResponse)

    def test_ResponseEntryIsNotADict_RaisesResponseError(
            self):
        http_response = fake_http_response(body=fake_body({
            "response": "PENDING",
            "entries": [["entry1"], ["entry2"]]
        }))

        expected_message = "Parameters are of incorrect type"
        with raises(DecodeError, message=expected_message):
            Response.load_response(http_response, PendingResponse)

    def test_ResponseEntryAmountIsNotAValidInt_RaisesResponseError(
            self):
        http_response = fake_http_response(body=fake_body({
            "response": "PENDING",
            "entries": [
                {
                    "UOMe": "1234",
                    "loaner": "C1",
                    "borrower": "C2",
                    "amount": "AD",
                    "salt": "1234",
                    "loaner_signature": "df4r2"
                }
            ]
        }))

        expected_message = "Parameters are of incorrect type"
        with raises(DecodeError, message=expected_message):
            Response.load_response(http_response, PendingResponse)
