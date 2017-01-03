import os
import sys

from PyQt5.QtWidgets import QApplication

from configuration import config
from login_dialog import LoginDialog
from main_window import MainWindow
from register_dialog import RegisterDialog


def main():
    app = QApplication(sys.argv)

    if os.path.exists(config.CONFIG_PATH):
        # User is already registered

        config.load()

        dialog = LoginDialog()

        if dialog.exec() != 1:
            print("Error: failed to login user\n"
                  "Will exit the program!", file=sys.stderr)
            sys.exit(1)

        # Get registered client
        client = dialog.client

    else:
        # User needs to register first

        # Present the user with the register dialog
        dialog = RegisterDialog()

        if dialog.exec() != 1:
            print("Error: failed to register user\n"
                  "Will exit the program!", file=sys.stderr)
            sys.exit(1)

        # Get registered client
        client = dialog.client

    window = MainWindow(client)
    window.refresh()
    window.adjustSize()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
