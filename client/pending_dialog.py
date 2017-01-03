from PyQt5.QtCore import Qt

from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QPushButton
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
        self.ui.button_box.accepted.connect(self.accept_uome)
        apply_button = self.ui.button_box.button(self.ui.button_box.Apply)
        apply_button.clicked.connect(self.accept_uome)
        self.ui.select_all_button.clicked.connect(self.select_all)
        self.ui.select_none_button.clicked.connect(self.select_none)

        self.refresh()

    def accept_uome(self):
        remove_rows = []

        for row in range(self.ui.table.rowCount()):
            item = self.ui.table.item(row, 0)
            if item.checkState() == Qt.Checked:
                self.client.accept_UOMe(item.text())
                remove_rows.append(row)

        for i, row in enumerate(remove_rows):
            self.ui.table.removeRow(row - i)

    def refresh(self):
        ignored, uomes = self.client.pending_UOMes()

        # Fill the table with each UOMe
        self.ui.table.setRowCount(len(uomes))
        for i, uome in enumerate(uomes):
            # Add a check box for each UOMe
            item = QTableWidgetItem(uome.uuid)
            item.setCheckState(Qt.Unchecked)
            self.ui.table.setItem(i, 0, item)

            self.ui.table.setItem(i, 1, QTableWidgetItem(uome.borrower))
            self.ui.table.setItem(i, 2, QTableWidgetItem(str(uome.value)))
            self.ui.table.setItem(i, 3, QTableWidgetItem(uome.description))

    def select_all(self):
        for row in range(self.ui.table.rowCount()):
            self.ui.table.item(row, 0).setCheckState(Qt.Checked)

    def select_none(self):
        for row in range(self.ui.table.rowCount()):
            self.ui.table.item(row, 0).setCheckState(Qt.Unchecked)



