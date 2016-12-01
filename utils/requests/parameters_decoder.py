import json
from json import JSONDecodeError


class DecodeError(Exception):
    """ Raised when there is an error while decoding parameters """


class ParametersDecoder:
    """
    Single point where the decoding of parameters is implemented. Its current
    implementation is based on JSON.
    """

    @staticmethod
    def load(body: str):
        """
        Takes a string with request/response parameters and  returns a
        dictionary with the parameters names as keys and it  corresponding
        values, well, as the values of the dict.

        The values of the parameters are returned as JSON supported types,
        which means that some base64 encoded values are returned as strings
        and must be converted outside this method.

        This method abstracts the encoding of the parameters. Its current
        implementation decodes from JSON format. It is enough to
        re-implement this method to change to other encoding format.

        :param body: body of a request or response to load from.
        :return: dictionary with the parameters (parameter values support
                 ony JSON supported types)
        """
        try:
            loaded_parameters = json.loads(body)
        except JSONDecodeError as error:
            raise DecodeError(error)

        if not isinstance(loaded_parameters, dict):
            raise DecodeError("Parameters must be encoded with a JSON object")

        return loaded_parameters
