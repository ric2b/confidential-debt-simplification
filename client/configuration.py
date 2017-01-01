#
# Configuration parameters
#
import json


class MissingParameterError(Exception):
    """
    Raised when a required configuration parameter is missing in the
    configuration file.
    """
    pass


class ParseError(Exception):
    """
    Raised when the format of the file is incorrect an it can not be
    parsed because of it.
    """
    pass


class _Configuration:

    mandatory_parameters = [
        "group_server_url",
        "proxy_server_url",
        "group_server_pubkey_path",
        "main_server_pubkey_path",
        "user_key_path",
        "user_email",
    ]

    def __init__(self):
        self._parameters = {}

    def __getitem__(self, item):
        return self._parameters[item]

    def __setitem__(self, key, value):
        self._parameters[key] = value

    def __contains__(self, item):
        return item in self._parameters

    def load(self, config_path):
        """ Loads configurations from a file """
        with open(config_path) as config_file:
            self._parameters = json.load(config_file)

            # check if the mandatory parameters were all loaded
            for parameter in self.mandatory_parameters:
                if parameter not in self:
                    raise MissingParameterError("Configuration file is missing "
                                                "parameter %s" % parameter)

    def save(self, config_path):
        """ Saves the current configurations into a file """
        with open(config_path, 'w') as config_file:
            json.dump(self._parameters, config_file, indent='\t')


config = _Configuration()

