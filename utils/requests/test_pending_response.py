from pytest import raises

from utils.requests.pending_response import PendingResponse
from utils.requests.response import ResponseError


class TestPendingResponse:
    #
    # Tests for the from_parameters() method
    #

    def test_ValidResponseWithCorrectFormattingAndOneEntry_PendingResponseWithEntry(
            self):
        parameters = {
            "response": "PENDING",
            "entries": [
                {
                    "id": "#1234",
                    "loaner": "C1",
                    "borrower": "C2",
                    "amount": 1000,
                    "salt": "1234",
                    "loaner_signature": "df4r2"
                }
            ]
        }

        response = PendingResponse.from_parameters(parameters)

        assert response.entries == [
            {
                "id": "#1234",
                "loaner": b"C1",
                "borrower": b"C2",
                "amount": 1000,
                "salt": "1234",
                "loaner_signature": b"df4r2"
            }
        ]

    def test_ResponseMissingTheResponseParameter_RaisesResponseError(self):
        parameters = {
            "entries": [
                {
                    "id": "#1234",
                    "loaner": "C1",
                    "borrower": "C2",
                    "amount": 1000,
                    "salt": "1234",
                    "loaner_signature": "df4r2"
                }
            ]
        }

        expected_message = "Response was missing some parameters"
        with raises(ResponseError, message=expected_message):
            PendingResponse.from_parameters(parameters)

    def test_ResponseWithIncorrectMethod_RaisesResponseError(self):
        parameters = {
            "response": "INCORRECT",
            "entries": [
                {
                    "id": "#1234",
                    "loaner": "C1",
                    "borrower": "C2",
                    "amount": 1000,
                    "salt": "1234",
                    "loaner_signature": "df4r2"
                }
            ]
        }

        expected_message = "Response method does not match"
        with raises(ResponseError, message=expected_message):
            PendingResponse.from_parameters(parameters)

    def test_ResponseMethodIsAnInt_RaisesResponseError(self):
        parameters = {
            "response": 1234,
            "entries": [
                {
                    "id": "#1234",
                    "loaner": "C1",
                    "borrower": "C2",
                    "amount": 1000,
                    "salt": "1234",
                    "loaner_signature": "df4r2"
                }
            ]
        }

        expected_message = "Parameters are of incorrect type"
        with raises(ResponseError, message=expected_message):
            PendingResponse.from_parameters(parameters)

    def test_ResponseEntriesIsNotAList_RaisesResponseError(self):
        parameters = {
            "response": "PENDING",
            "entries": "value"
        }

        expected_message = "Parameters are of incorrect type"
        with raises(ResponseError, message=expected_message):
            PendingResponse.from_parameters(parameters)

    def test_ResponseEntryMissesOneParameter_RaisesResponseError(
            self):
        parameters = {
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
        }

        expected_message = "Parameters are of incorrect type"
        with raises(ResponseError, message=expected_message):
            PendingResponse.from_parameters(parameters)

    def test_ResponseEntryIsNotADict_RaisesResponseError(
            self):
        parameters = {
            "response": "PENDING",
            "entries": [["entry1"], ["entry2"]]
        }

        expected_message = "Parameters are of incorrect type"
        with raises(ResponseError, message=expected_message):
            PendingResponse.from_parameters(parameters)

    def test_ResponseEntryAmountIsNotAValidInt_RaisesResponseError(
            self):
        parameters = {
            "response": "PENDING",
            "entries": [
                {
                    "id": "1234",
                    "loaner": "C1",
                    "borrower": "C2",
                    "amount": "AD",
                    "salt": "1234",
                    "loaner_signature": "df4r2"
                }
            ]
        }

        expected_message = "Parameters are of incorrect type"
        with raises(ResponseError, message=expected_message):
            PendingResponse.from_parameters(parameters)
