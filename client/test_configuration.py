from pytest import fixture
from pytest import raises

from configuration import config, MissingParameterError


class TestConfiguration:

    @fixture
    def tmp_file(self, tmpdir):
        return tmpdir.join("config.conf")

    def test_load_FileWithAllParameters_LoadedParametersMatchFile(
            self, tmp_file):
        tmp_file.write("""{
            "group_server_url": "group.com",
            "proxy_server_url": "proxy.com",
            "group_server_pubkey_path": "group/key",
            "main_server_pubkey_path": "main/key",
            "user_key_path": "user/key",
            "user_email": "user@email.com"
        }""")

        config.load(str(tmp_file))

        assert config["group_server_url"] == "group.com"
        assert config["proxy_server_url"] == "proxy.com"
        assert config["group_server_pubkey_path"] == "group/key"
        assert config["main_server_pubkey_path"] == "main/key"
        assert config["user_key_path"] == "user/key"
        assert config["user_email"] == "user@email.com"

    def test_load_FileMissesGroupServerUrl_RaisesMissingParameterError(
            self, tmp_file):

        tmp_file.write("""{
            "proxy_server_url": "proxy.com",
            "group_server_pubkey_path": "group/key",
            "main_server_pubkey_path": "main/key",
            "user_key_path": "user/key",
            "user_email": "user@email.com"
        }""")

        with raises(MissingParameterError):
            config.load(str(tmp_file))
