class Requester:
    """
    A requester is someone that has an ID and is able to sign data. it is
    just an interface which sets the required methods that a request needs
    to be issued.
    """

    def __init__(self, requester_id: str):
        self.requester_id = requester_id

    @property
    def id(self) -> str:
        """ Returns the ID of the requester """
        return self.requester_id

    def sign(self, data: bytes) -> bytes:
        """ Takes data in bytes and returns a signature for it in base 64 """
        pass
