from unittest.mock import Mock, MagicMock

from pytest import fixture

import client.client as c
import utils.messages.message as m
from client.client import Client
from utils.messages.message_formats import UserInvite


class TestClient:

    @fixture
    def client(self):
        return Client(
            group_server_url="http://register.com",
            group_server_pubkey="group1234",
            main_server_pubkey="main1234",
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

        def sign(key, *values):
            return "%s:%s" % (key, "-".join(values))

        # create a predictable signing method
        m.sign = Mock(side_effect=sign)

        return mock_connection

    def test_invite_UserC2(self, client, mock_connection):
        client.invite("C2", "c2@email.com")

        mock_connection.request.assert_called_once_with(
            UserInvite.make_request(
                group_uuid="1",
                inviter="C1",
                invitee="C2",
                invitee_email="c2@email.com",
                inviter_signature="pC1:1-C1-C2-c2@email.com"
            )
        )

