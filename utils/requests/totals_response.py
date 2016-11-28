from utils.requests.response import ResponseError


class TotalsResponse:
    """
    Totals Response - response to a totals request.
    """

    method = "TOTALS"

    def __init__(self, totals_entries: list):
        self._parameters = {
            "response": self.method,
            "entries": totals_entries
        }

    @staticmethod
    def from_parameters(parameters: dict):
        """
        Expects the following parameters:
            - response type
            - entries

        Each entry has the following parameters:
            - other user ID
            - amount

        :raise ResponseError: if the response is not in the expected format
                              or missing some parameters.
        :return: TotalsResponse object.
        """
        try:
            if parameters["response"] != TotalsResponse.method:
                raise ResponseError("Response method does not match")

            # Note: there is no problem forcing the parameters to be strings
            # and then encoding to bytes. Any JSON type is decoded into a
            # python type that can be correctly converted to a string without
            # generating an exception. Checking if the value is correct is
            # not the responsibility of the response implementation

            # ensure entries parameter is a list
            entries = parameters["entries"]
            if not isinstance(entries, list):
                raise ValueError  # move to ValueError handling

            totals_entries = []
            for entry in entries:
                total_entry = {
                    "other_user": str(entry["other_user"]).encode(),
                    "amount": int(entry["amount"])
                }

                totals_entries.append(total_entry)

            return TotalsResponse(
                totals_entries=totals_entries,
            )

        except KeyError:
            raise ResponseError("Response was missing some parameters")
        except (ValueError, TypeError):
            raise ResponseError("Parameters are of incorrect type")

    @property
    def parameters(self) -> dict:
        """
        Returns a dictionary containing the parameters of the response.

        :return: dictionary with the names and values of the response
                 parameters.
        """
        return self._parameters

    @property
    def entries(self) -> list:
        return self._parameters["entries"]
