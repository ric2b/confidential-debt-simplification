from pytest import raises

from utils.requests.response import DecodeError, Response
from utils.requests.test_utils import fake_body, fake_http_response
from utils.requests.totals_response import TotalsResponse


class TestTotalsResponse:
    #
    # Tests for the from_parameters() method
    #

    def test_ValidResponseWithCorrectFormattingAndOneEntry_TotalsResponseWithEntry(self):
        http_response = fake_http_response(body=fake_body({
            "response": "TOTALS",
            "entries": [
                {
                    "other_user": "C1",
                    "amount": 1000
                }
            ]
        }))

        response = Response.load_response(http_response, TotalsResponse)

        assert response.entries == [
            {
                "other_user": b"C1",
                "amount": 1000
            }
        ]

    def test_ResponseMissingTheResponseParameter_RaisesResponseError(self):
        http_response = fake_http_response(body=fake_body({
            "entries": [
                {
                    "other_user": "C1",
                    "amount": 1000
                }
            ]
        }))

        expected_message = "Response was missing some parameters"
        with raises(DecodeError, message=expected_message):
            Response.load_response(http_response, TotalsResponse)

    def test_ResponseWithIncorrectMethod_RaisesResponseError(self):
        http_response = fake_http_response(body=fake_body({
            "response": "INCORRECT",
            "entries": [
                {
                    "other_user": "C1",
                    "amount": 1000
                }
            ]
        }))

        expected_message = "Response method does not match"
        with raises(DecodeError, message=expected_message):
            Response.load_response(http_response, TotalsResponse)

    def test_ResponseMethodIsAnInt_RaisesResponseError(self):
        http_response = fake_http_response(body=fake_body({
            "response": 1234,
            "entries": [
                {
                    "other_user": "C1",
                    "amount": 1000
                }
            ]
        }))

        expected_message = "Parameters are of incorrect type"
        with raises(DecodeError, message=expected_message):
            Response.load_response(http_response, TotalsResponse)

    def test_ResponseEntriesIsNotAList_RaisesResponseError(self):
        http_response = fake_http_response(body=fake_body({
            "response": "TOTALS",
            "entries": "value"
        }))

        expected_message = "Parameters are of incorrect type"
        with raises(DecodeError, message=expected_message):
            Response.load_response(http_response, TotalsResponse)

    def test_ResponseEntryMissesOneParameter_RaisesResponseError(
            self):
        http_response = fake_http_response(body=fake_body({
            "response": "TOTALS",
            "entries": [
                {
                    # misses other_user
                    "amount": 1000
                }
            ]
        }))

        expected_message = "Parameters are of incorrect type"
        with raises(DecodeError, message=expected_message):
            Response.load_response(http_response, TotalsResponse)

    def test_ResponseEntryIsNotADict_RaisesResponseError(
            self):
        http_response = fake_http_response(body=fake_body({
            "response": "TOTALS",
            "entries": [["entry1"], ["entry2"]]
        }))

        expected_message = "Parameters are of incorrect type"
        with raises(DecodeError, message=expected_message):
            Response.load_response(http_response, TotalsResponse)

    def test_ResponseEntryAmountIsNotAValidInt_RaisesResponseError(
            self):
        http_response = fake_http_response(body=fake_body({
            "response": "TOTALS",
            "entries": [
                {
                    "other_user": "C1",
                    "amount": "AD"
                }
            ]
        }))

        expected_message = "Parameters are of incorrect type"
        with raises(DecodeError, message=expected_message):
            Response.load_response(http_response, TotalsResponse)
