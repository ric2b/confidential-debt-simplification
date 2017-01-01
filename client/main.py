import sys
from PyQt5.QtWidgets import QApplication

from client import Client
from configuration import config
from main_window import MainWindow
from utils.crypto import rsa


def main():
    app = QApplication(sys.argv)

    config_path = "client.json"
    config.load(config_path)

    group_server_url = config["group_server_url"]
    group_server_pubkey = rsa.load_pubkey(config["group_server_pubkey_path"])
    proxy_server_url = config["proxy_server_url"]
    main_server_pubkey = rsa.load_pubkey(config["main_server_pubkey_path"])
    user_keys = rsa.load_keys(config["user_key_path"])
    user_email = config["user_email"]

    client = Client(group_server_url, group_server_pubkey,
                    main_server_pubkey, proxy_server_url, user_email,
                    keys=user_keys)

    window = MainWindow(client)
    window.adjustSize()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
