import json

from client.requester import Requester


class Request:
    """
    Request abstracts the complexity of an HTTP request. Hides the actual
    format of the request and provides a clean interface to set the values of
    the parameters required for each type of request.

    A request is always associated with a method. A method is the actual
    operation required from the server. This maps directly into django's view
    model. For instance, when a client want to invite someone it goes to the URL
    proxy-server.com/invite. "invite" is the method of the request.

    A request is always associated with a requester that signs the request.
    All request's bodies must be signed by the requester.

    Request is only the base class, and does not have a complete
    implementation. Each subclass must provide the implementation for the
    method and parameters getters. Those are use to perform the actual
    request. This class already ensures that the body of the request is
    signed. Therefore, all subclasses should just implement the previously
    mentioned getter methods.
    """

    def __init__(self, requester: Requester):
        """
        Initializes a request, associating it with the requester.

        :param requester: requester making th request.
        """
        self.requester = requester

    @property
    def method(self) -> str:
        """
        Returns the method of the request. The method should be a string and
        should be the same for all instances of the request implementation.

        :return: request's method
        """
        return ""

    @property
    def parameters(self) -> dict:
        """
        Must return a dictionary containing the parameters of the request.
        For instance, the invite request would require 2 parameters: the
        invitee ID and its email, thereby, the parameters getter should
        return a dictionary with: { 'invitee_ID': ID, 'invitee_email': email }.

        :return: dictionary with the names and values of the request parameters.
        """
        return dict()

    @property
    def body(self) -> str:
        """
        Returns a string containing the body of the request. The body of the
        request is composed by the parameters dictionary of the request
        implementation serialized to JSON format. Subclasses should not
        override this method and just implement the parameters property.

        :return: JSON string containing the parameters of the request.
        """
        return json.dumps(self.parameters).encode()
