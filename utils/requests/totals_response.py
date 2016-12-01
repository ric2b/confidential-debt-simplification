from utils.requests.parameters import entries, identifier, integer
from utils.requests.response import Response


class TotalsResponse(Response):
    """
    Totals Response - response to a totals request.
    """

    method = "TOTALS"

    # The class field parameter_types defines the parameters and types of
    # the values of each parameter
    parameters_types = {
        "entries": entries({
            "other_user": identifier,
            "amount": integer,
        })
    }

    @staticmethod
    def build(pending_entries: list):
        """
        Factory method for an Totals response. Use this method to create
        Totals responses instead of the default initializer.

        Returns an Totals response signed by the given signer. This method
        abstracts which parameters are signed by the signer.
        """
        parameters_values = {
            "entries": pending_entries
        }

        return TotalsResponse(parameters_values)

    @property
    def parameters(self) -> dict:
        """
        Returns a dictionary containing the parameters of the response.

        :return: dictionary with the names and values of the response
                 parameters.
        """
        return self._parameters_values

    @property
    def entries(self) -> list:
        return self._parameters_values["entries"]
