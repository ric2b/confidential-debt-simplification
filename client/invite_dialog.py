from PyQt5.QtWidgets import QDialog
from ui_invite import Ui_InviteDialog


class InviteDialog(QDialog):

    def __init__(self, client):
        super(InviteDialog, self).__init__()
        self.client = client

        # Set up the user interface from Designer.
        self.ui = Ui_InviteDialog()
        self.ui.setupUi(self)

        self.ui.button_box.accepted.connect(self.invite)

    def invite(self):
        self.client.invite(
            invitee_id=self.ui.id_lineedit.text(),
            invitee_email=self.ui.email_lineedit.text()
        )

