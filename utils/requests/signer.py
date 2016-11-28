class Signer:
    """
    << Interface >>
    A signer is simply someone with an ID that is able to sign
    data bytes.
    """

    @property
    def id(self) -> bytes:
        """ Returns the ID of the signer """
        return b""

    def sign(self, *data: bytes) -> bytes:
        """
        Method called when requesting something to be signed by the signer.

        :param data: list with data elements to sign in bytes format.
        :return: signature for the given data in base 64.
        """
        pass
