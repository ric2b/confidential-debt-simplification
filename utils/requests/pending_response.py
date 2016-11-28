from utils.requests.response import ResponseError


class PendingResponse:
    """
    Pending Response - response to a pending request.
    """

    method = "PENDING"

    def __init__(self, pending_entries: list):
        self._parameters = {
            "response": self.method,
            "entries": pending_entries
        }

    @staticmethod
    def from_parameters(parameters: dict):
        """
        Expects the following parameters:
            - response type
            - entries

        Each entry has the following parameters:
            - UOMe ID
            - loaner ID
            - borrower ID
            - amount
            - salt
            - UOMe signed by the loaner

        :raise ResponseError: if the response is not in the expected format
                              or missing some parameters.
        :return: PendingResponse object.
        """
        try:
            if parameters["response"] != PendingResponse.method:
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

            pending_entries = []
            for entry in entries:
                pending_UOMe = {
                    "id": str(entry["id"]),
                    "loaner": str(entry["loaner"]).encode(),
                    "borrower": str(entry["borrower"]).encode(),
                    "amount": int(entry["amount"]),
                    "salt": entry["salt"],
                    "loaner_signature": str(entry["loaner_signature"]).encode()
                }

                pending_entries.append(pending_UOMe)

            return PendingResponse(
                pending_entries=pending_entries,
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
