import sys
from PyQt5.QtWidgets import QApplication

from configuration import config
from main_window import MainWindow


def main():
    app = QApplication(sys.argv)

    config_path = "client.json"
    config.load(config_path)

    window = MainWindow()
    window.adjustSize()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
