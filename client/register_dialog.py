import os

import sys
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QMessageBox

from client_backend import Client
from client_backend import ProtocolError
from configuration import config
from ui_register import Ui_RegisterDialog
from utils.crypto import rsa


class RegisterDialog(QDialog):

    def __init__(self):
        super(RegisterDialog, self).__init__()

        # Set up the user interface from Designer.
        self.ui = Ui_RegisterDialog()
        self.ui.setupUi(self)

        try:
            # Load the main server public key
            main_server_pubkey_path = config.main_server_pubkey_path
            self._main_server_pubkey = rsa.load_pubkey(main_server_pubkey_path)

        except FileNotFoundError:
            QMessageBox.warning(
                self, "Missing Main Public Key",
                "Missing 'main.pem' file in the app directory\n"
                "Please ask the support team for this file."
            )
            sys.exit(1)

        # Generate keys for client
        self._key, self._pubkey = rsa.generate_keys()
        self.ui.id_line.setText(self._pubkey)

        self.client = None

    def accept(self):

        # Show a warning if one of the inputs is empty
        # Keep the dialog active
        if not self.ui.email_line.text() or \
                not self.ui.inviter_line.text() or \
                not self.ui.group_line.text() or \
                not self.ui.group_key_line.text() or \
                not self.ui.secret_line.text() or \
                not self.ui.password_line.text():
            QMessageBox.information(self, "Register Failed",
                                    "Please fill empty values")

        client = Client(
            group_server_url=self.ui.group_line.text(),
            group_server_pubkey=self.ui.group_key_line.text(),
            main_server_pubkey=self._main_server_pubkey,
            proxy_server_url=config.proxy_server_url,
            email=self.ui.email_line.text(),
            keys=(self._key, self._pubkey)
        )

        try:
            inviter_signature, group_signature = client.join(
                secret_code=self.ui.secret_line.text(),
                inviter_id=self.ui.inviter_line.text()
            )

            self.client = client

        except ProtocolError as error:
            QMessageBox.warning(self, "Register Failed", str(error))
            sys.exit(1)

        #
        # Store the two signatures obtained during registration
        #

        signature_path = os.path.join(config.app_dir, "inviter_signature.txt")
        with open(signature_path, "w") as signature_file:
            signature_file.write(inviter_signature + "\n")

        signature_path = os.path.join(config.app_dir, "group_signature.txt")
        with open(signature_path, "w") as signature_file:
            signature_file.write(group_signature + "\n")

        # Store the group server public key
        rsa.dump_pubkey(
            pubkey=self.ui.group_key_line.text(),
            key_filepath=config.group_server_pubkey_path
        )

        # Store the user's keys
        rsa.dump_key(
            key=self._key,
            key_filepath=config.user_key_path,
            password=self.ui.password_line.text()
        )

        # Create the config file for this user
        config.group_server_url = self.ui.group_line.text()
        config.user_email = self.ui.email_line.text()
        config.save()

        # Call the accept method of the QDialog
        super(RegisterDialog, self).accept()
