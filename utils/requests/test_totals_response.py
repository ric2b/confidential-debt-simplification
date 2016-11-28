from pytest import raises

from utils.requests.response import ResponseError
from utils.requests.totals_response import TotalsResponse


class TestTotalsResponse:
    #
    # Tests for the from_parameters() method
    #

    def test_ValidResponseWithCorrectFormattingAndOneEntry_TotalsResponseWithEntry(
            self):
        parameters = {
            "response": "TOTALS",
            "entries": [
                {
                    "other_user": "C1",
                    "amount": 1000
                }
            ]
        }

        response = TotalsResponse.from_parameters(parameters)

        assert response.entries == [
            {
                "other_user": b"C1",
                "amount": 1000
            }
        ]

    def test_ResponseMissingTheResponseParameter_RaisesResponseError(self):
        parameters = {
            "entries": [
                {
                    "other_user": "C1",
                    "amount": 1000
                }
            ]
        }

        expected_message = "Response was missing some parameters"
        with raises(ResponseError, message=expected_message):
            TotalsResponse.from_parameters(parameters)

    def test_ResponseWithIncorrectMethod_RaisesResponseError(self):
        parameters = {
            "response": "INCORRECT",
            "entries": [
                {
                    "other_user": "C1",
                    "amount": 1000
                }
            ]
        }

        expected_message = "Response method does not match"
        with raises(ResponseError, message=expected_message):
            TotalsResponse.from_parameters(parameters)

    def test_ResponseMethodIsAnInt_RaisesResponseError(self):
        parameters = {
            "response": 1234,
            "entries": [
                {
                    "other_user": "C1",
                    "amount": 1000
                }
            ]
        }

        expected_message = "Parameters are of incorrect type"
        with raises(ResponseError, message=expected_message):
            TotalsResponse.from_parameters(parameters)

    def test_ResponseEntriesIsNotAList_RaisesResponseError(self):
        parameters = {
            "response": "TOTALS",
            "entries": "value"
        }

        expected_message = "Parameters are of incorrect type"
        with raises(ResponseError, message=expected_message):
            TotalsResponse.from_parameters(parameters)

    def test_ResponseEntryMissesOneParameter_RaisesResponseError(
            self):
        parameters = {
            "response": "TOTALS",
            "entries": [
                {
                    # misses other_user
                    "amount": 1000
                }
            ]
        }

        expected_message = "Parameters are of incorrect type"
        with raises(ResponseError, message=expected_message):
            TotalsResponse.from_parameters(parameters)

    def test_ResponseEntryIsNotADict_RaisesResponseError(
            self):
        parameters = {
            "response": "TOTALS",
            "entries": [["entry1"], ["entry2"]]
        }

        expected_message = "Parameters are of incorrect type"
        with raises(ResponseError, message=expected_message):
            TotalsResponse.from_parameters(parameters)

    def test_ResponseEntryAmountIsNotAValidInt_RaisesResponseError(
            self):
        parameters = {
            "response": "TOTALS",
            "entries": [
                {
                    "other_user": "C1",
                    "amount": "AD"
                }
            ]
        }

        expected_message = "Parameters are of incorrect type"
        with raises(ResponseError, message=expected_message):
            TotalsResponse.from_parameters(parameters)
