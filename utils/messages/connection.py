import http.client as http

from utils.messages.message import Message


class BadRequestError(Exception):
    """ Raised when the response's status code is '400 Bad Request' """
    pass


class UnauthorizedError(Exception):
    """ Raised when the response's status code is '401 Unauthorized' """
    pass


class ForbiddenError(Exception):
    """ Raised when the response's status code is '403 Forbidden' """
    pass


class ConflictError(Exception):
    """ Raised when the response's status code is '409 Conflict' """
    pass


class NotFoundError(Exception):
    """ Raised when the response's status code is '404 Not Found' """
    pass


class UnknownError(Exception):
    """ Raised when the response's status code is not none of the expected """
    pass


# Maps an error status code to the respective exception class
error_exception = {
    400: BadRequestError,
    401: UnauthorizedError,
    403: ForbiddenError,
    409: ConflictError,
    404: NotFoundError,
}


def connect(server_url):
    """ Entry method to connect to a server using an URL """
    return Connection(server_url, http.HTTPConnection(server_url))


class Connection:
    """
    Abstraction of an HTTP or HTTPS connection which supports our own request
    and response API.

    IMPORTANT: To create a connection object do not use its initializer
    directly, instead use the 'connect' factory method.
    Might seem silly, but this separation facilitates testing.
    """

    def __init__(self, server_url, http_connection):
        """
        THIS INITIALIZER SHOULD NOT BE USED - use the 'connect' function instead

        Initializes a connection to the server with the given URL. It takes
        an already established http connection with the corresponding server.
        This connection will be used underneath to send and receive messages.

        :param server_url: URL of the HTTP server to connect to in the format
                           "address:port"
        :param http_connection: established HTTP connection with the server
        """
        self.server_url = server_url
        self._http_connection = http_connection

    def close(self):
        """
        Closes the connection with the server. After calling this the
        connection is no longer useful and can not be used.
        """
        if self._http_connection:
            self._http_connection.close()
            self._http_connection = None

    #
    # Support context management
    #

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    #
    # Public Interface to make requests
    #

    def request(self, request: Message):
        """
        Issues a request. Takes a request object and makes a post request to
        the HTTP server. It accesses the 'method' property of the request to
        generate the URL of the HTTP post request. The body of the HTTP
        request is taken from the 'body' property of the Request object.
        After calling this method, the get_response() method should be called
        to get the server's response.

        :param request: request to be issued.
        """
        self._http_connection.request(
            method='POST',
            url='/' + request.url,
            body=request.dumps()
        )

    def get_response(self, response_type: Message):
        """
        Waits for a response to a request. The expected type of the request
        must be provided. The main job of this method is to take an
        HTTPResponse and load the respective response message object. In case
        of an unsuccessful response from the server an exception is raised
        according to the HTTP error code.

        :param response_type: type for the expected response
        :return: response message from the server.
        """
        http_response = self._http_connection.getresponse()
        status = http_response.status

        if status == 200 or status == 201 or status == 202:
            # request was successful
            body = http_response.read().decode()
            return response_type.load_response(body)

        else:
            try:
                exception = error_exception[status]
            except KeyError:
                # unknown status code
                exception = UnknownError

            error_message = http_response.read()
            raise exception(error_message)
