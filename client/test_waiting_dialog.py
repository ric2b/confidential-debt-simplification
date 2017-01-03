import sys
from unittest.mock import MagicMock

from PyQt5.QtWidgets import QApplication

from uome import UOMe
from waiting_dialog import WaitingDialog


class TestWaitingDialog:

    def test_waiting_dialog(self):
        client = MagicMock()
        client.pending_UOMes.return_value = [
            UOMe("1", "C2", "C1", 10, "debtC1C2", "sign1", "#1"),
            UOMe("1", "C3", "C1", 10, "debtC1C3", "sign2", "#2"),
            UOMe("1", "C4", "C1", 10, "debtC1C4", "sign3", "#3"),
            UOMe("1", "C5", "C1", 10, "debtC1C5", "sign4", "#4"),
        ], []

        app = QApplication(sys.argv)

        dialog = WaitingDialog(client)
        dialog.show()

        sys.exit(app.exec_())

