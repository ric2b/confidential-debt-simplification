import sys

from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QMessageBox

from client_backend import Client
from configuration import config
from ui_login import Ui_LoginDialog
from utils.crypto import rsa


class LoginDialog(QDialog):

    def __init__(self):
        super(LoginDialog, self).__init__()

        # Set up the user interface from Designer.
        self.ui = Ui_LoginDialog()
        self.ui.setupUi(self)

        self.client = None

    def accept(self):

        # Show a warning if one of the inputs is empty
        # Keep the dialog active
        if not self.ui.password_line.text():
            QMessageBox.information(self, "Login Failed",
                                    "Password can not be empty.")

        #
        # Load keys
        #

        try:
            group_server_pubkey = rsa.load_pubkey(
                config.group_server_pubkey_path)

        except FileNotFoundError:
            QMessageBox.information(
                self, "Missing Group Key",
                "Missing group key file.\n"
                "The configuration file says the file should be\n"
                "stored at:\n"
                "%s" % config.group_server_pubkey_path
            )
            sys.exit(1)

        try:
            main_server_pubkey = rsa.load_pubkey(
                config.main_server_pubkey_path)

        except FileNotFoundError:
            QMessageBox.information(
                self, "Missing Main Key",
                "Missing main key file.\n"
                "The configuration file says the file should be\n"
                "stored at:\n"
                "%s" % config.main_server_pubkey_path
            )
            sys.exit(1)

        try:
            user_keys = rsa.load_keys(config.user_key_path,
                                      password=self.ui.password_line.text())

        except FileNotFoundError:
            QMessageBox.information(
                self, "Missing User Key",
                "Missing user key file.\n"
                "The configuration file says the file should be\n"
                "stored at:\n"
                "%s" % config.user_key_path
            )
            sys.exit(1)

        except ValueError:
            QMessageBox.information(
                self, "Incorrect Password",
                "Failed to decrypt keys\n"
                "Password must be incorrect\n"
                "Try again please..."
            )
            return

        #
        # Create the client
        #

        self.client = Client(
            config.group_server_url,
            group_server_pubkey,
            main_server_pubkey,
            config.proxy_server_url,
            config.user_email,
            keys=user_keys
        )

        # Call the accept method of the QDialog
        super(LoginDialog, self).accept()
