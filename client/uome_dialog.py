from PyQt5.QtWidgets import QDialog
from ui_uome import Ui_UOMeDialog


class UOMeDialog(QDialog):

    def __init__(self, client):
        super(UOMeDialog, self).__init__()
        self.client = client

        # Set up the user interface from Designer.
        self.ui = Ui_UOMeDialog()
        self.ui.setupUi(self)

        self.ui.button_box.accepted.connect(self.issue_uome)

    def issue_uome(self):
        self.client.issue_UOMe(
            borrower=self.ui.borrower_lineedit.text(),
            value=int(self.ui.amount_spinbox.value() * 100),
            description=self.ui.description_lineedit.text()
        )

