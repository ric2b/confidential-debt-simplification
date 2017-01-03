from unittest.mock import MagicMock

import sys
from PyQt5.QtWidgets import QApplication

from main_window import MainWindow
from uome import UOMe


class TestMainWindow:

    def test_refresh(self):
        client = MagicMock()
        client.join.return_value = "inviter123", "group123"
        client.totals.return_value = -3000, {"C2": 1000, "C3": 2000}
        client.pending_UOMes.return_value = [], [
            UOMe("1", "C1", "C2", 10, "debtC1C2", "sign1", "#1"),
            UOMe("1", "C1", "C3", 10, "debtC1C3", "sign2", "#2"),
        ]

        app = QApplication(sys.argv)
        window = MainWindow(client)
        window.refresh()
        window.adjustSize()
        window.show()

        app.exec_()
