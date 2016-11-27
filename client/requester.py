class Requester:
    """
    A requester is someone that has an ID and is able to sign data. it is
    just an interface which sets the required methods that a request needs
    to be issued.
    """

    @property
    def id(self) -> str:
        """ Returns the ID of the requester """
        return ""

    def sign(self, data: bytes) -> bytes:
        """ Takes data in bytes and returns a signature for it in base 64 """
        pass
