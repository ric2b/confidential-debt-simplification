from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QTableWidget


class CommitButton(QPushButton):

    COLUMN = 0

    def __init__(self, table: QTableWidget, row, *__args):
        super().__init__(*__args)
        self.table = table
        self.row = row

        # noinspection PyUnresolvedReferences
        self.clicked.connect(self.commit)

    def commit(self):
        uome_uuid_column = 1
        uome_uuid = self.table.item(self.row, uome_uuid_column).text()

        self.operate(uome_uuid)

        self.table.removeRow(self.row)

        # update the rows of all other buttons
        for row in range(self.table.rowCount()):
            self.table.cellWidget(row, self.COLUMN).row = row

    def operate(self, uome_uuid):
        """ Subclasses should override this method to accept or cancel """
        pass
