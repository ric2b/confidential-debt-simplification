from unittest.mock import Mock, MagicMock

from pytest import fixture
from pytest import raises

import client.client_backend as c
import utils.messages.message as m
import utils.messages.message_formats as msg
import utils.crypto.rsa as rsa
from client.client_backend import Client
from client.uome import UOMe
from utils.messages.connection import ConflictError, ForbiddenError, \
    UnauthorizedError


# noinspection PyUnusedLocal
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
            proxy_server_url="P",
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
                user="C1",
                invitee="C2",
                invitee_email="c2@email.com",
                user_signature="pC1:1-C1-C2-c2@email.com"
            )
        )

    def test_invite_UserC2WhichAlreadyExists_RaisesUserExistsError(
            self, client, mock_connection, predictable_signatures):
        mock_connection.get_response.side_effect = ConflictError()

        with raises(c.UserExistsError):
            client.invite("C2", "c2@email.com")

    def test_invite_UserC2ButInviterIsNotRegistered_RaisesForbiddenError(
            self, client, mock_connection, predictable_signatures):
        mock_connection.get_response.side_effect = ForbiddenError()

        with raises(c.PermissionDeniedError):
            client.invite("C2", "c2@email.com")

    def test_invite_UserC2ButSignatureWasNotAccepted_RaisesAuthenticationError(
            self, client, mock_connection, predictable_signatures):
        mock_connection.get_response.side_effect = UnauthorizedError()

        with raises(c.AuthenticationError):
            client.invite("C2", "c2@email.com")

    def test_join_NewUserC1WithSecretCode123_SendsJoinRequestWithSignedCode123(
            self, client, mock_connection, predictable_signatures):
        mock_connection.get_response.return_value = \
            msg.GroupServerJoin.make_response(
                inviter="C2",
                user="C1",
                user_email="c1@email.com",
                inviter_signature="pC2:1-C2-C1-c1@email.com",
                group_signature="pG:pC2:1-C2-C1-c1@email.com",
            )

        client.join(secret_code="#123", inviter_id="C2")

        mock_connection.request.assert_called_once_with(
            msg.GroupServerJoin.make_request(
                group_uuid="1",
                user="C1",
                secret_code="#123",
                user_signature="pC1:1-C1-#123"
            )
        )

    def test_join_ResponseHasCorrectSignatures_DoesNotRaiseAnyException(
            self, client, mock_connection, predictable_signatures):
        mock_connection.get_response.return_value = \
            msg.GroupServerJoin.make_response(
                inviter="C2",
                user="C1",
                user_email="c1@email.com",
                inviter_signature="pC2:1-C2-C1-c1@email.com",
                group_signature="pG:pC2:1-C2-C1-c1@email.com",
            )

        # assert does not raise anything
        client.join(secret_code="#123", inviter_id="C2")

    def test_join_ResponseHasInvalidInviterSignature_RaisesAuthenticationError(
            self, client, mock_connection, predictable_signatures):
        mock_connection.get_response.return_value = \
            msg.GroupServerJoin.make_response(
                inviter="C2",
                user="C1",
                user_email="c1@email.com",
                # signed by inviter C3 instead of C2
                inviter_signature="pC3:1-C2-C1-c1@email.com",
                group_signature="pG:pC2:1-C2-C1-c1@email.com",
            )

        with raises(c.AuthenticationError):
            client.join(secret_code="#123", inviter_id="C2")

    def test_join_ResponseHasInvalidGroupSignature_RaisesAuthenticationError(
            self, client, mock_connection, predictable_signatures):
        mock_connection.get_response.return_value = \
            msg.GroupServerJoin.make_response(
                inviter="C2",
                user="C1",
                user_email="c1@email.com",
                inviter_signature="pC2:1-C2-C1-c1@email.com",
                # signed with invalid group server key
                group_signature="pG1:pC2:1-C2-C1-c1@email.com",
            )

        with raises(c.AuthenticationError):
            client.join(secret_code="#123", inviter_id="C2")

    def test_join_RequestSignatureWasNotAcceptedByTheServer_RaisesAuthenticationError(
            self, client, mock_connection, predictable_signatures):
        mock_connection.get_response.side_effect = UnauthorizedError()

        with raises(c.AuthenticationError):
            client.join(secret_code="#123", inviter_id="C2")

    def test_join_SecretCodeWasNotAcceptedByTheServer_RaisesPermissionDeniedError(
            self, client, mock_connection, predictable_signatures):
        mock_connection.get_response.side_effect = ForbiddenError()

        with raises(c.PermissionDeniedError):
            client.join(secret_code="#123", inviter_id="C2")

    def test_join_C1IsAlreadyRegistered_RaisesUserExistsError(
            self, client, mock_connection, predictable_signatures):
        mock_connection.get_response.side_effect = ConflictError()

        with raises(c.UserExistsError):
            client.join(secret_code="#123", inviter_id="C2")

    def test_confirm_join_C1ConfirmsJoinBySendingInviteSignedByTheInviterTheGroupServerAnC1(
            self, client, mock_connection, predictable_signatures):

        client.confirm_join(group_signature="pG:pC2:1-C2-C1-c1@email.com")

        mock_connection.request.assert_called_once_with(
            msg.ConfirmJoin.make_request(
                group_uuid="1",
                user="C1",
                user_signature="pC1:1-C1-pG:pC2:1-C2-C1-c1@email.com"
            )
        )

    def test_confirm_join_RequestSignatureWasNotAcceptedByTheServer_RaisesAuthenticationError(
            self, client, mock_connection, predictable_signatures):
        mock_connection.get_response.side_effect = UnauthorizedError()

        with raises(c.AuthenticationError):
            client.confirm_join(group_signature="pG:pC2:1-C2-C1-c1@email.com")

    def test_confirm_join_UserC2ConfirmsJoinForUserC3_RaisesPermissionDeniedError(
            self, client, mock_connection, predictable_signatures):
        mock_connection.get_response.side_effect = ForbiddenError()

        with raises(c.PermissionDeniedError):
            client.confirm_join(group_signature="pG:pC2:1-C2-C1-c1@email.com")

    def test_confirm_join_C1IsAlreadyRegistered_RaisesUserExistsError(
            self, client, mock_connection, predictable_signatures):
        mock_connection.get_response.side_effect = ConflictError()

        with raises(c.UserExistsError):
            client.confirm_join(group_signature="pG:pC2:1-C2-C1-c1@email.com")

    def test_issue_UOMe_WithUserC2WithValue10_SendsUOMeAndSignedUOMe(
            self, client, mock_connection, predictable_signatures):
        mock_connection.get_response.return_value = \
            msg.IssueUOMe.make_response(
                uome_uuid="#1234",
                main_signature="pM:#1234-1-C1-C2-10-debt",
            )

        client.issue_UOMe(borrower="C2", value=10, description="debt")

        mock_connection.request.assert_called_once_with(
            msg.IssueUOMe.make_request(
                group_uuid="1",
                user="C1",
                borrower="C2",
                value=10,
                description="debt",
                user_signature="pC1:1-C1-C2-10-debt"
            )
        )

    def test_issue_UOMe_RequestSignatureWasNotAcceptedByTheServer_RaisesAuthenticationError(
            self, client, mock_connection, predictable_signatures):
        mock_connection.get_response.side_effect = UnauthorizedError()

        with raises(c.AuthenticationError):
            client.issue_UOMe(borrower="C2", value=10, description="debt")

    def test_issue_UOMe_UserDidNotHavePermissionToIssueUOMe_RaisesPermissionDeniedError(
            self, client, mock_connection, predictable_signatures):
        mock_connection.get_response.side_effect = ForbiddenError()

        with raises(c.PermissionDeniedError):
            client.issue_UOMe(borrower="C2", value=10, description="debt")

    def test_issue_UOMe_ResponseHasInvalidSignature_RaisesAuthenticationError(
            self, client, mock_connection, predictable_signatures):
        mock_connection.get_response.return_value = \
            msg.IssueUOMe.make_response(
                uome_uuid="#1234",
                # signed by group server instead of main server
                main_signature="pG:#1234-1-C1-C2-10-debt",
            )

        with raises(c.AuthenticationError):
            client.issue_UOMe(borrower="C2", value=10, description="debt")

    def test_cancel_UOMe_WithValidUOMeID_SendsCorrectRequestAndSignatureVerifies(
            self, client, mock_connection, predictable_signatures):
        mock_connection.get_response.return_value = \
            msg.CancelUOMe.make_response(
                uome_uuid="#1234",
                main_signature="pM:1-C1-#1234",
            )

        client.cancel_UOMe(UOMe_number="#1234")

        mock_connection.request.assert_called_once_with(
            msg.CancelUOMe.make_request(
                group_uuid="1",
                user="C1",
                uome_uuid="#1234",
                user_signature="pC1:1-C1-#1234"
            )
        )

    def test_cancel_UOMe_RequestSignatureWasNotAcceptedByTheServer_RaisesAuthenticationError(
            self, client, mock_connection, predictable_signatures):
        mock_connection.get_response.side_effect = UnauthorizedError()

        with raises(c.AuthenticationError):
            client.cancel_UOMe(UOMe_number="#1234")

    def test_cancel_UOMe_UserDidNotHavePermissionToCancelUOMe_RaisesPermissionDeniedError(
            self, client, mock_connection, predictable_signatures):
        mock_connection.get_response.side_effect = ForbiddenError()

        with raises(c.PermissionDeniedError):
            client.cancel_UOMe(UOMe_number="#1234")

    def test_cancel_UOMe_ResponseHasInvalidSignature_RaisesAuthenticationError(
            self, client, mock_connection, predictable_signatures):
        mock_connection.get_response.return_value = \
            msg.CancelUOMe.make_response(
                uome_uuid="#1234",
                # signed by group server instead of main server
                main_signature="pG:1-C1-#1234",
            )

        with raises(c.AuthenticationError):
            client.cancel_UOMe(UOMe_number="#1234")

    def test_accept_UOMe_WithValidUOMeID_SendsCorrectRequestAndSignatureVerifies(
            self, client, mock_connection, predictable_signatures):
        mock_connection.get_response.return_value = \
            msg.AcceptUOMe.make_response(
                uome_uuid="#1234",
                main_signature="pM:1-C1-#1234",
            )

        client.accept_UOMe(UOMe_number="#1234")

        mock_connection.request.assert_called_once_with(
            msg.AcceptUOMe.make_request(
                group_uuid="1",
                user="C1",
                uome_uuid="#1234",
                user_signature="pC1:1-C1-#1234"
            )
        )

    def test_accept_UOMe_RequestSignatureWasNotAcceptedByTheServer_RaisesAuthenticationError(
            self, client, mock_connection, predictable_signatures):
        mock_connection.get_response.side_effect = UnauthorizedError()

        with raises(c.AuthenticationError):
            client.accept_UOMe(UOMe_number="#1234")

    def test_accept_UOMe_UserDidNotHavePermissionToAcceptUOMe_RaisesPermissionDeniedError(
            self, client, mock_connection, predictable_signatures):
        mock_connection.get_response.side_effect = ForbiddenError()

        with raises(c.PermissionDeniedError):
            client.accept_UOMe(UOMe_number="#1234")

    def test_accept_UOMe_ResponseHasInvalidSignature_RaisesAuthenticationError(
            self, client, mock_connection, predictable_signatures):
        mock_connection.get_response.return_value = \
            msg.AcceptUOMe.make_response(
                uome_uuid="#1234",
                # signed by group server instead of main server
                main_signature="pG:1-C1-#1234",
            )

        with raises(c.AuthenticationError):
            client.accept_UOMe(UOMe_number="#1234")

    def test_pending_UOMes_SendsCorrectRequest(
            self, client, mock_connection, predictable_signatures):

        mock_connection.get_response.return_value = \
            msg.GetPendingUOMes.make_response(
                issued_by_user=[],
                waiting_for_user=[],
                main_signature="ignored"
            )

        client.pending_UOMes()

        mock_connection.request.assert_called_once_with(
            msg.GetPendingUOMes.make_request(
                group_uuid="1",
                user="C1",
                user_signature="pC1:1-C1"
            )
        )

    def test_pending_UOMes_ResponseContainsTwoUOMes_ReturnListWithTheTwoUOMes(
            self, client, mock_connection, predictable_signatures):

        mock_connection.get_response.return_value = \
            msg.GetPendingUOMes.make_response(
                issued_by_user=[
                    ["1", "C1", "C2", 10, "debtC1C2", "sign1", "#1"],
                    ["1", "C1", "C4", 10, "debtC1C4", "sign2", "#2"]
                ],
                waiting_for_user=[
                    ["1", "C3", "C1", 10, "debtC3C1", "sign3", "#3"],
                    ["1", "C5", "C1", 10, "debtC5C1", "sign4", "#4"]
                ],
                main_signature="ignored"
            )

        issued, waiting = client.pending_UOMes()

        assert issued == [
            UOMe("1", "C1", "C2", 10, "debtC1C2", "sign1", "#1"),
            UOMe("1", "C1", "C4", 10, "debtC1C4", "sign2", "#2")
        ]

        assert waiting == [
            UOMe("1", "C3", "C1", 10, "debtC3C1", "sign3", "#3"),
            UOMe("1", "C5", "C1", 10, "debtC5C1", "sign4", "#4")
        ]

    def test_pending_UOMes_RequestSignatureWasNotAcceptedByTheServer_RaisesAuthenticationError(
            self, client, mock_connection, predictable_signatures):
        mock_connection.get_response.side_effect = UnauthorizedError()

        with raises(c.AuthenticationError):
            client.pending_UOMes()

    def test_totals_SendsCorrectRequest(
            self, client, mock_connection, predictable_signatures):

        mock_connection.get_response.return_value = \
            msg.CheckTotals.make_response(
                user_balance=0,
                suggested_transactions={},
                main_signature="ignored"
            )

        client.totals()

        mock_connection.request.assert_called_once_with(
            msg.CheckTotals.make_request(
                group_uuid="1",
                user="C1",
                user_signature="pC1:1-C1"
            )
        )

    def test_totals_ResponseBalanceIs10AndUserMayPay5ToC2And5ToC3_ReturnedBalanceIs10(
            self, client, mock_connection, predictable_signatures):

        mock_connection.get_response.return_value = \
            msg.CheckTotals.make_response(
                user_balance=10,
                suggested_transactions={"C2": 5, "C3": 5},
                main_signature="ignored"
            )

        balance, transactions = client.totals()

        assert balance == 10

    def test_totals_ResponseBalanceIs10AndUserMayPay5ToC2And5ToC3_ReturnedTransactionAre5ToC2And5ToC3(
            self, client, mock_connection, predictable_signatures):

        mock_connection.get_response.return_value = \
            msg.CheckTotals.make_response(
                user_balance=10,
                suggested_transactions={"C2": 5, "C3": 5},
                main_signature="ignored"
            )

        balance, transactions = client.totals()

        assert transactions == {"C2": 5, "C3": 5}

    def test_totals_RequestSignatureWasNotAcceptedByTheServer_RaisesAuthenticationError(
            self, client, mock_connection, predictable_signatures):
        mock_connection.get_response.side_effect = UnauthorizedError()

        with raises(c.AuthenticationError):
            client.totals()

    def test_totals_UserDidNotHavePermissionToCheckTotals_RaisesPermissionDeniedError(
            self, client, mock_connection, predictable_signatures):
        mock_connection.get_response.side_effect = ForbiddenError()

        with raises(c.PermissionDeniedError):
            client.totals()
