import sys
from PyQt5.QtWidgets import QApplication

from main_window import MainWindow


def main():
    app = QApplication(sys.argv)
    window = MainWindow()

    window.adjustSize()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':              # if we're running file directly and not importing it
    main()                              # run the main function
