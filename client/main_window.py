from PyQt5.QtWidgets import QMainWindow

from invite_dialog import InviteDialog
from pending_dialog import PendingDialog
from ui_main import Ui_MainWindow
from uome_dialog import UOMeDialog
from waiting_dialog import WaitingDialog


class MainWindow(QMainWindow):

    def __init__(self, client):
        super(MainWindow, self).__init__()
        self.client = client

        # Set up the user interface from Designer.
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self._uome_dialog = None
        self._invite_dialog = None
        self._pending_dialog = None
        self._waiting_dialog = None

        self.ui.uome_button.clicked.connect(self.issue_uome)
        self.ui.invite_button.clicked.connect(self.invite)
        self.ui.refresh_button.clicked.connect(self.refresh)
        self.ui.pending_button.clicked.connect(self.pending)
        self.ui.waiting_button.clicked.connect(self.waiting)

    def issue_uome(self):
        if not self._uome_dialog:
            self._uome_dialog = UOMeDialog(self.client)
        self._uome_dialog.show()

    def invite(self):
        if not self._invite_dialog:
            self._invite_dialog = InviteDialog(self.client)
        self._invite_dialog.show()

    def refresh(self):
        balance, transactions = self.client.totals()

        self.ui.balance_value.setText("%0.2f" % (balance / 100.0))
        pattern = "Pay %0.2f to %s" if balance < 0 else "Receive %0.2f from %s"

        self.ui.transactions_list.clear()
        for user, value in transactions.items():
            self.ui.transactions_list.addItem(pattern % (value / 100.0, user))

    def pending(self):
        if not self._pending_dialog:
            self._pending_dialog = PendingDialog(self.client)
        self._pending_dialog.refresh()
        self._pending_dialog.show()

    def waiting(self):
        if not self._waiting_dialog:
            self._waiting_dialog = WaitingDialog(self.client)
        self._waiting_dialog.show()
