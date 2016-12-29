from unittest.mock import Mock, MagicMock

from pytest import fixture
from pytest import raises

import client.client as c
import utils.messages.message as m
import utils.messages.message_formats as msg
import utils.crypto.rsa as rsa
from client.client import Client
from utils.messages.connection import ConflictError, ForbiddenError, \
    UnauthorizedError


class TestClient:

    @fixture
    def predictable_signatures(self):
        """
        Forces the signatures to be predictable. A signature is always in the
        format 'key:param1-param2-...' for instance if the key is pC1 and the
        data values to be signed are A and B then the signature is 'pC1-A-B'.

        In order to be able to verify a signature signed with the private key
        using the public key, it must be possible to obtain the private key
        from the public key. To accomplish this, the private key is equal to
        the public key but prefixed by a lower case 'p'.
        """

        def sign(key, *values):
            return "%s:%s" % (key, "-".join(values))

        def verify(pubkey, signature, *values):
            obtained_signature = "p%s:%s" % (pubkey, "-".join(values))

            if obtained_signature != signature:
                raise rsa.InvalidSignature()

        # create a predictable signing method
        m.sign = Mock(side_effect=sign)
        m.verify = Mock(side_effect=verify)

    @fixture
    def client(self):
        return Client(
            group_server_url="http://register.com",
            group_server_pubkey="G",
            main_server_pubkey="M",
            email="c1@email.com",
            keys=("pC1", "C1")
        )

    @fixture
    def mock_connection(self):
        mock_connection = MagicMock()
        mock_connection.__enter__.return_value = mock_connection
        mock_connection.__exit__.return_value = None

        # modify the connect function to return a mock connection instead of
        # a normal connection
        c.connect = Mock(return_value=mock_connection)

        return mock_connection

    def test_invite_UserC2(self, client, mock_connection,
                           predictable_signatures):
        client.invite("C2", "c2@email.com")

        mock_connection.request.assert_called_once_with(
            msg.UserInvite.make_request(
                group_uuid="1",
                inviter="C1",
                invitee="C2",
                invitee_email="c2@email.com",
                inviter_signature="pC1:1-C1-C2-c2@email.com"
            )
        )

    def test_invite_UserC2WhichAlreadyExists_RaisesClientExistsError(
            self, client, mock_connection, predictable_signatures):
        mock_connection.get_response.side_effect = ConflictError()

        with raises(c.ClientExistsError):
            client.invite("C2", "c2@email.com")

    def test_invite_UserC2ButInviterIsNotRegistered_RaisesForbiddenError(
            self, client, mock_connection, predictable_signatures):
        mock_connection.get_response.side_effect = ForbiddenError()

        with raises(c.PermissionDeniedError):
            client.invite("C2", "c2@email.com")

    def test_invite_UserC2ButSignatureWasNotAccepted_RaisesSecurityError(
            self, client, mock_connection, predictable_signatures):
        mock_connection.get_response.side_effect = UnauthorizedError()

        with raises(c.SecurityError):
            client.invite("C2", "c2@email.com")
