from PyQt5.QtWidgets import QMainWindow
from main_design import Ui_MainWindow


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        # Set up the user interface from Designer.
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.uome_button.clicked.connect(self.issue_uome)
        self.ui.invite_button.clicked.connect(self.invite)
        self.ui.refresh_button.clicked.connect(self.refresh)
        self.ui.pending_button.clicked.connect(self.pending)
        self.ui.waiting_button.clicked.connect(self.waiting)

    def issue_uome(self):
        print("issue UOMe")

    def invite(self):
        print("invite")

    def refresh(self):
        print("refresh")

    def pending(self):
        print("pending")

    def waiting(self):
        print("waiting")
