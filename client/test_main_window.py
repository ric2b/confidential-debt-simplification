from unittest.mock import MagicMock

import sys
from PyQt5.QtWidgets import QApplication

from main_window import MainWindow


class TestMainWindow:

    def test_refresh(self):
        client = MagicMock()
        client.join.return_value = "inviter123", "group123"
        client.totals.return_value = -3000, {"C2": 1000, "C3": 2000}

        app = QApplication(sys.argv)
        window = MainWindow(client)
        window.refresh()
        window.adjustSize()
        window.show()

        app.exec_()
