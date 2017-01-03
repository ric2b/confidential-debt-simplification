from commit_button import CommitButton


class CancelButton(CommitButton):

    COLUMN = 0

    def __init__(self, client, table, row):
        super().__init__(table, row)
        self.client = client
        self.setText("cancel")

    def operate(self, uome_uuid, other_user, value, description):
        """ Subclasses should override this method to accept or cancel """
        self.client.cancel_UOMe(uome_uuid)
