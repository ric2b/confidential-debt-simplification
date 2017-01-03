#
# Configuration parameters
#
import json
import os


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

    CONFIG_PATH = "config.json"
    DEFAULT_APP_DIR = "."
    DEFAULT_PROXY_SERVER_URL = "localhost"

    mandatory_parameters = [
        "group_server_url",
        "proxy_server_url",
        "group_server_pubkey_path",
        "main_server_pubkey_path",
        "user_key_path",
        "user_email",
    ]

    def __init__(self):
        self.app_dir = self.DEFAULT_APP_DIR
        self._parameters = {
            "proxy_server_url": self.DEFAULT_PROXY_SERVER_URL,
            "group_server_pubkey_path": os.path.join(self.app_dir, "group.pem"),
            "main_server_pubkey_path": os.path.join(self.app_dir, "main.pem"),
            "user_key_path": os.path.join(self.app_dir, "user.pem"),
        }

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

    def save(self, config_path=CONFIG_PATH):
        """ Saves the current configurations into a file """
        with open(config_path, 'w') as config_file:
            json.dump(self._parameters, config_file, indent='\t')


config = _Configuration()

