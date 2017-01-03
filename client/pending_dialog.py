from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QTableWidgetItem

from ui_pending import Ui_PendingDialog


class PendingDialog(QDialog):

    def __init__(self, client):
        super(PendingDialog, self).__init__()
        self.client = client

        # Set up the user interface from Designer.
        self.ui = Ui_PendingDialog()
        self.ui.setupUi(self)

        # Connect buttons to respective slots
        apply_button = self.ui.button_box.button(self.ui.button_box.Apply)
        apply_button.clicked.connect(self.apply)

    def accept(self):
        self.apply()

        # Call the accept method of the QDialog
        super(PendingDialog, self).accept()

    def apply(self):
        if self.ui.tab_widget.currentIndex() == 0:
            # loans tab is active
            self.cancel_uome()
        else:
            # debts tab is active
            self.accept_uome()

    def accept_uome(self):
        remove_rows = []

        for row in range(self.ui.loans_table.rowCount()):
            item = self.ui.loans_table.item(row, 0)
            if item.checkState() == Qt.Checked:
                self.client.accept_UOMe(item.text())
                remove_rows.append(row)

        for i, row in enumerate(remove_rows):
            self.ui.loans_table.removeRow(row - i)

    def cancel_uome(self):
        remove_rows = []

        for row in range(self.ui.debts_table.rowCount()):
            item = self.ui.debts_table.item(row, 0)
            if item.checkState() == Qt.Checked:
                self.client.cancel_UOMe(item.text())
                remove_rows.append(row)

        for i, row in enumerate(remove_rows):
            self.ui.debts_table.removeRow(row - i)

    def refresh(self):
        loans, debts = self.client.pending_UOMes()

        # Update both tables
        self._refresh_table(self.ui.loans_table, loans)
        self._refresh_table(self.ui.debts_table, debts)

    @staticmethod
    def _refresh_table(table, uomes):
        # Fill the loans table with each UOMe
        table.setRowCount(len(uomes))
        for i, uome in enumerate(uomes):
            # Add a check box for each UOMe
            item = QTableWidgetItem(uome.uuid)
            item.setCheckState(Qt.Unchecked)
            table.setItem(i, 0, item)

            table.setItem(i, 1, QTableWidgetItem(uome.borrower))
            table.setItem(i, 2, QTableWidgetItem(str(uome.value)))
            table.setItem(i, 3, QTableWidgetItem(uome.description))

    def select_all(self):
        table = self._current_table()
        for row in range(table.rowCount()):
            table.item(row, 0).setCheckState(Qt.Checked)

    def select_none(self):
        table = self._current_table()
        for row in range(table.rowCount()):
            table.item(row, 0).setCheckState(Qt.Unchecked)

    def _current_table(self):
        if self.ui.tab_widget.currentIndex() == 0:
            # loans tab is active
            return self.ui.loans_table
        else:
            # debts tab is active
            return self.ui.debts_table



