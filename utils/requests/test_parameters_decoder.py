from pytest import raises

from utils.requests.parameters_decoder import ParametersDecoder, DecodeError


class TestParametersDecoder:

    #
    # The goal is not to test if the JSON module works correctly
    # What we want to test is if the small logic inside the load method besides
    # the loading of the JSON string works
    #

    def test_load_ValidJSONWithTwoObjects_DictWithTheTwoParameters(self):
        body = '{"parameter1": "value1", "parameter2": "value2"}'

        parameters = ParametersDecoder.load(body)

        assert parameters == {
            "parameter1": "value1",
            "parameter2": "value2"
        }

    def test_load_JSONWithNoObjects_EmptyDict(self):
        body = '{}'

        parameters = ParametersDecoder.load(body)

        assert parameters == {}

    def test_load_EmptyString_RaisesDecodeError(self):
        body = ''

        with raises(DecodeError):
            ParametersDecoder.load(body)

    def test_load_ValidJSONWithArray_RaisesDecodeError(self):
        body = '["parameter1", "parameter2"]'

        with raises(DecodeError):
            ParametersDecoder.load(body)
