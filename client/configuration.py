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
        "user_email",
    ]

    def __init__(self):
        self.app_dir = self.DEFAULT_APP_DIR
        self._parameters = {}

    @property
    def group_server_url(self):
        return self._parameters["group_server_url"]

    @group_server_url.setter
    def group_server_url(self, value):
        self._parameters["group_server_url"] = value

    @property
    def proxy_server_url(self):
        try:
            return self._parameters["proxy_server_url"]
        except KeyError:
            return self.DEFAULT_PROXY_SERVER_URL

    @proxy_server_url.setter
    def proxy_server_url(self, value):
        self._parameters["proxy_server_url"] = value

    @property
    def group_server_pubkey_path(self):
        try:
            return self._parameters["group_server_pubkey_path"]
        except KeyError:
            return os.path.join(self.app_dir, "group.pem")

    @group_server_pubkey_path.setter
    def group_server_pubkey_path(self, value):
        self._parameters["group_server_pubkey_path"] = value

    @property
    def main_server_pubkey_path(self):
        try:
            return self._parameters["main_server_pubkey_path"]
        except KeyError:
            return os.path.join(self.app_dir, "main.pem")

    @main_server_pubkey_path.setter
    def main_server_pubkey_path(self, value):
        self._parameters["main_server_pubkey_path"] = value

    @property
    def user_key_path(self):
        try:
            return self._parameters["user_key_path"]
        except KeyError:
            return os.path.join(self.app_dir, "user.pem")

    @user_key_path.setter
    def user_key_path(self, value):
        self._parameters["user_key_path"] = value

    @property
    def user_email(self):
        return self._parameters["user_email"]

    @user_email.setter
    def user_email(self, value):
        self._parameters["user_email"] = value

    def __contains__(self, item):
        return item in self._parameters

    def load(self, config_path=CONFIG_PATH):
        """ Loads configurations from a file """
        with open(config_path) as config_file:
            self._parameters.update(json.load(config_file))

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

