from unittest.mock import MagicMock

import sys
from PyQt5.QtWidgets import QApplication

from pending_dialog import PendingDialog
from uome import UOMe


class TestPendingDialog:

    def test_pending_dialog(self):
        client = MagicMock()
        client.pending_UOMes.return_value = [], [
            UOMe("1", "C1", "C2", 10, "debtC1C2", "sign1", "#1"),
            UOMe("1", "C1", "C3", 10, "debtC1C3", "sign2", "#2"),
        ]

        app = QApplication(sys.argv)

        dialog = PendingDialog(client)
        dialog.show()

        sys.exit(app.exec_())

