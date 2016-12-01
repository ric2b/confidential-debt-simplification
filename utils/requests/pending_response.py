from utils.requests.parameters import entries, identifier, signature, integer
from utils.requests.response import Response


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

    @property
    def parameters(self) -> dict:
        return self._parameters_values

    @property
    def entries(self) -> list:
        return self._parameters_values["entries"]
