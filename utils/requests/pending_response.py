from utils import bytesutils
from utils.requests.parameters import entries, identifier, signature, integer
from utils.requests.response import Response
from utils.requests.verifier import Verifier


class PendingResponse(Response):
    """
    Pending Response - response to a pending request.
    """

    method = "PENDING"

    # The class field parameter_types defines the parameters and types of
    # the values of each parameter
    parameters_types = {
        "entries": entries({
            "UOMe": str,
            "loaner": identifier,
            "borrower": identifier,
            "amount": integer,
            "salt": str,
            "loaner_signature": signature
        })
    }

    @staticmethod
    def build(pending_entries: list):
        """
        Factory method for an Pending response. Use this method to create
        Pending responses instead of the default initializer.

        Returns an Pending response signed by the given signer. This method
        abstracts which parameters are signed by the signer.
        """
        parameters_values = {
            "entries": pending_entries
        }

        return PendingResponse(parameters_values)

    def verify(self, verifier: Verifier):
        """
        Verifies if the signatures of each entry in the pending request are
        valid. Does not check if the borrower corresponds to the verifier.
        """
        for entry in self.entries:
            verifier.verify(entry["loaner_signature"],
                            entry["loaner"],
                            entry["borrower"],
                            bytesutils.from_int(entry["amount"]),
                            entry["salt"].encode())

    @property
    def entries(self) -> list:
        return self._parameters_values["entries"]
