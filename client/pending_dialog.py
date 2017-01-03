from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QTableWidgetItem

from accept_button import AcceptButton
from cancel_button import CancelButton
from ui_pending import Ui_PendingDialog


class PendingDialog(QDialog):

    def __init__(self, client):
        super(PendingDialog, self).__init__()
        self.client = client

        # Set up the user interface from Designer.
        self.ui = Ui_PendingDialog()
        self.ui.setupUi(self)

    def refresh(self):
        loans, debts = self.client.pending_UOMes()

        # Update both tables
        self._refresh_table(self.ui.loans_table, loans, CancelButton)
        self._refresh_table(self.ui.debts_table, debts, AcceptButton)

    def _refresh_table(self, table, uomes, button_type):
        # Fill the loans table with each UOMe
        table.setRowCount(len(uomes))
        for i, uome in enumerate(uomes):
            # Add a check box for each UOMe
            table.setIndexWidget(table.model().index(i, 0),
                                 button_type(self.client, table, i))

            if table == self.ui.loans_table:
                other_user = uome.borrower
            else:
                other_user = uome.user

            table.setItem(i, 1, QTableWidgetItem(uome.uuid))
            table.setItem(i, 2, QTableWidgetItem(other_user))
            table.setItem(i, 3, QTableWidgetItem("%.2f" % (uome.value / 100.0)))
            table.setItem(i, 4, QTableWidgetItem(uome.description))

    def _current_table(self):
        if self.ui.tab_widget.currentIndex() == 0:
            # loans tab is active
            return self.ui.loans_table
        else:
            # debts tab is active
            return self.ui.debts_table

