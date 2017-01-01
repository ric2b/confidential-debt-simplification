from PyQt5.QtWidgets import QMainWindow
from main_design import Ui_MainWindow
from uome_dialog import UOMeDialog


class MainWindow(QMainWindow):

    def __init__(self, client):
        super(MainWindow, self).__init__()
        self.client = client

        # Set up the user interface from Designer.
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self._uome_dialog = None

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
        print("invite")

    def refresh(self):
        print("refresh")

    def pending(self):
        print("pending")

    def waiting(self):
        print("waiting")
