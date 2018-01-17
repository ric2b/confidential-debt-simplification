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
        # TODO store signature
        # TODO store the UOMe-ID

        borrower = self.ui.borrower_lineedit.text()
        value = int(self.ui.amount_spinbox.value() * 100)
        description = self.ui.description_lineedit.text()

        uome_uuid, main_signature = self.client.issue_UOMe(borrower, value,
                                                           description)

        self.client.confirm_UOMe(uome_uuid, borrower, value, description)

