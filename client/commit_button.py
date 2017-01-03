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
        other_user_column = 2
        value_column = 3
        description_column = 4

        uome_uuid = self.table.item(self.row, uome_uuid_column).text()
        other_user = self.table.item(self.row, other_user_column).text()
        value = self.table.item(self.row, value_column).text()
        value = int(float(value) * 100)
        description = self.table.item(self.row, description_column).text()

        self.operate(uome_uuid, other_user, value, description)

        self.table.removeRow(self.row)

        # update the rows of all other buttons
        for row in range(self.table.rowCount()):
            self.table.cellWidget(row, self.COLUMN).row = row

    def operate(self, uome_uuid, other_user, value, description):
        """ Subclasses should override this method to accept or cancel """
        pass
