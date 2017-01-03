from django.test import TestCase  # TODO: check out pytest
from django.urls import reverse
from django.core import serializers
from django.conf import settings
import json
from uuid import uuid4

from collections import defaultdict

from .models import Group, User, UOMe, UserDebt

from utils.crypto.rsa import generate_keys, sign, verify
from utils.crypto import example_keys
from utils.messages import message_formats as msg
from utils.messages.uome_tools import UOMeTools


# Create your tests here.

# Good rules-of-thumb include having:
#
# - a separate TestClass for each model or view
# - a separate test method for each set of conditions you want to test
# - test method names that describe their function
# TODO: check this out, looks cool: https://docs.djangoproject.com/en/1.10/ref/validators/

class RegisterGroupTests(TestCase):
    # TODO: add proxy/name server address?
    def test_correct_inputs(self):
        group_name = 'test_name'
        key = example_keys.G1_pub

        signature = sign(example_keys.G1_priv, group_name, key)
        message_data = msg.RegisterGroup.make_request(group_name=group_name,
                                                      group_key=key,
                                                      group_signature=signature)

        raw_response = self.client.post(reverse('main_server_app:register_group'),
                                        {'data': message_data.dumps()})

        response = msg.RegisterGroup.load_response(raw_response.content.decode())

        assert raw_response.status_code == 201

        signature_content = [response.group_uuid, group_name, key]
        verify(settings.PUBLIC_KEY, response.main_signature, *signature_content)

    def test_invalid_message(self):
        group_name = 'test_name'
        key = example_keys.G1_pub

        signature = sign(example_keys.G1_priv, group_name)
        message_data = msg.RegisterGroup.make_request(group_name=group_name,
                                                      group_key=key,
                                                      group_signature=signature)

        message_data.group_key = 42

        raw_response = self.client.post(reverse('main_server_app:register_group'),
                                        {'data': message_data.dumps()})

        assert raw_response.status_code == 400

    def test_invalid_signature(self):
        group_name = 'test_name'
        key = example_keys.G1_pub

        signature = sign(example_keys.G1_priv, group_name)
        message_data = msg.RegisterGroup.make_request(group_name=group_name,
                                                      group_key=key,
                                                      group_signature=signature)

        raw_response = self.client.post(reverse('main_server_app:register_group'),
                                        {'data': message_data.dumps()})

        assert raw_response.status_code == 401


class JoinGroupTests(TestCase):
    def setUp(self):
        self.message_class = msg.MainServerJoin
        self.private_key, self.key = generate_keys()
        self.group = Group.objects.create(name='test', key=example_keys.G1_pub)

    def test_new_user_invalid_group_uuid(self):
        user_priv, user_pub = example_keys.C1_priv, example_keys.C1_pub

        group_sig = self.message_class.sign(example_keys.G2_priv, 'group', user=user_pub,
                                            group_uuid='random_uuid')

        request = self.message_class.make_request(group_uuid='random_uuid',
                                                  user=user_pub,
                                                  group_signature=group_sig)

        raw_response = self.client.post(reverse('main_server_app:join-group'),
                                        {'data': request.dumps()})

        assert raw_response.status_code == 400

    def test_new_user_non_existent_group(self):
        user_priv, user_pub = example_keys.C1_priv, example_keys.C1_pub

        group_uuid = str(uuid4())

        group_sig = self.message_class.sign(example_keys.G2_priv, 'group', user=user_pub,
                                            group_uuid=group_uuid)

        request = self.message_class.make_request(group_uuid=group_uuid,
                                                  user=user_pub,
                                                  group_signature=group_sig)

        raw_response = self.client.post(reverse('main_server_app:join-group'),
                                        {'data': request.dumps()})

        assert raw_response.status_code == 400

    def test_new_user_to_existing_group(self):
        user_priv, user_pub = example_keys.C1_priv, example_keys.C1_pub

        group_sig = self.message_class.sign(example_keys.G1_priv, 'group', user=user_pub,
                                            group_uuid=self.group.uuid)

        request = self.message_class.make_request(group_uuid=str(self.group.uuid),
                                                  user=user_pub,
                                                  group_signature=group_sig)

        raw_response = self.client.post(reverse('main_server_app:join-group'),
                                        {'data': request.dumps()})

        assert raw_response.status_code == 201

        response = self.message_class.load_response(raw_response.content.decode())
        assert response.group_uuid == str(self.group.uuid)
        assert response.user == user_pub

        self.message_class.verify(settings.PUBLIC_KEY, 'main', response.main_signature,
                                  group_uuid=self.group.uuid,
                                  user=user_pub)


class IssueUOMeTests(TestCase):
    def setUp(self):
        self.message_class = msg.IssueUOMe
        self.private_key, self.key = example_keys.C1_priv, example_keys.C1_pub
        self.group = Group.objects.create(name='test', key=example_keys.G1_pub)
        self.user = User.objects.create(group=self.group, key=self.key)
        self.borrower = User.objects.create(group=self.group, key=example_keys.C2_pub)

    def test_add_first_uome(self):
        signature = self.message_class.sign(self.private_key, 'user',
                                            group_uuid=str(self.group.uuid),
                                            user=self.user.key)

        request = self.message_class.make_request(group_uuid=str(self.group.uuid),
                                                  user=self.user.key,
                                                  borrower=self.borrower.key,
                                                  value=1000,
                                                  description='my description',
                                                  user_signature=signature)

        raw_response = self.client.post(reverse('main_server_app:issue_uome'),
                                        {'data': request.dumps()})

        assert raw_response.status_code == 201

        response = self.message_class.load_response(raw_response.content.decode())

        self.message_class.verify(settings.PUBLIC_KEY, 'main', response.main_signature,
                                  uome_uuid=response.uome_uuid,
                                  group_uuid=str(self.group.uuid),
                                  user=self.user.key,
                                  borrower=self.borrower.key,
                                  value=1000,
                                  description='my description')

        uome = UOMe.objects.get(pk=response.uome_uuid)
        assert uome.issuer_signature == ''


class ConfirmUOMeTests(TestCase):
    def setUp(self):
        self.message_class = msg.ConfirmUOMe
        self.private_key, self.key = example_keys.C1_priv, example_keys.C1_pub
        self.group = Group.objects.create(name='test', key=example_keys.G1_pub)
        self.user = User.objects.create(group=self.group, key=self.key)
        self.borrower = User.objects.create(group=self.group, key=example_keys.C2_pub)

    def test_confirm_first_uome(self):
        uome = UOMe.objects.create(group=self.group, lender=self.user,
                                   borrower=self.borrower,
                                   value=10,
                                   description='test')

        issuer_signature = UOMeTools.sign(self.private_key,
                                          group_uuid=str(self.group.uuid),
                                          issuer=self.user.key,
                                          borrower=self.borrower.key,
                                          value=10,
                                          description='test',
                                          uome_uuid=str(uome.uuid))

        request = self.message_class.make_request(group_uuid=str(self.group.uuid),
                                                  user=self.user.key,
                                                  uome_uuid=str(uome.uuid),
                                                  user_signature=issuer_signature)

        raw_response = self.client.post(reverse('main_server_app:confirm_uome'),
                                        {'data': request.dumps()})

        assert raw_response.status_code == 200

        response = self.message_class.load_response(raw_response.content.decode())

        assert response.group_uuid == str(self.group.uuid)
        assert response.user == self.user.key

        uome = UOMe.objects.get(pk=uome.uuid)
        assert uome.issuer_signature == issuer_signature


class CancelUOMeTests(TestCase):
    def setUp(self):
        self.message_class = msg.CancelUOMe
        self.private_key, self.key = example_keys.C1_priv, example_keys.C1_pub
        self.group = Group.objects.create(name='test', key=example_keys.G1_pub)
        self.user = User.objects.create(group=self.group, key=self.key)
        self.borrower = User.objects.create(group=self.group, key=example_keys.C2_pub)

    def test_cancel_unconfirmed_uome(self):
        uome = UOMe.objects.create(group=self.group, lender=self.user,
                                   borrower=self.borrower,
                                   value=10,
                                   description='test')

        issuer_signature = UOMeTools.sign(self.private_key,
                                          group_uuid=str(self.group.uuid),
                                          issuer=self.user.key,
                                          borrower=self.borrower.key,
                                          value=10,
                                          description='test',
                                          uome_uuid=str(uome.uuid))

        uome.issuer_signature = issuer_signature
        uome.save()

        signature = self.message_class.sign(self.private_key, 'user',
                                            group_uuid=str(self.group.uuid),
                                            user=self.user.key,
                                            uome_uuid=str(uome.uuid))

        request = self.message_class.make_request(group_uuid=str(self.group.uuid),
                                                  user=self.user.key,
                                                  uome_uuid=str(uome.uuid),
                                                  user_signature=signature)

        raw_response = self.client.post(reverse('main_server_app:cancel_uome'),
                                        {'data': request.dumps()})

        assert raw_response.status_code == 200

        response = self.message_class.load_response(raw_response.content.decode())
        self.message_class.verify(settings.PUBLIC_KEY, 'main', response.main_signature,
                                  group_uuid=str(self.group.uuid),
                                  user=self.user.key,
                                  uome_uuid=str(uome.uuid))

        assert UOMe.objects.filter(uuid=uome.uuid).first() is None

        # TODO: test for the other cases: uome doesn't exist, the user isn't the
        # issuer of the uome or the uome has already been confirmed


class GetPendingUOMesTests(TestCase):
    def setUp(self):
        self.message_class = msg.GetPendingUOMes
        self.private_key, self.key = example_keys.C1_priv, example_keys.C1_pub
        self.group = Group.objects.create(name='test', key=example_keys.G1_pub)
        self.user = User.objects.create(group=self.group, key=self.key)
        self.other_user = User.objects.create(group=self.group, key=example_keys.C2_pub)

    def test_one_by_user_uome_and_one_for_user_uome(self):

        uome_by_user = UOMe.objects.create(group=self.group, lender=self.user,
                                           borrower=self.other_user, value=30,
                                           description="by user")

        by_user_sig = UOMeTools.sign(self.private_key,
                                     group_uuid=str(self.group.uuid),
                                     issuer=self.user.key,
                                     borrower=self.other_user.key,
                                     value=30,
                                     description="by user",
                                     uome_uuid=str(uome_by_user.uuid))

        uome_by_user.issuer_signature = by_user_sig
        uome_by_user.save()

        uome_for_user = UOMe.objects.create(group=self.group, lender=self.other_user,
                                            borrower=self.user, value=20,
                                            description="for user")

        for_user_sig = UOMeTools.sign(example_keys.C2_priv,
                                      group_uuid=str(self.group.uuid),
                                      issuer=self.other_user.key,
                                      borrower=self.user.key,
                                      value=20,
                                      description="for user",
                                      uome_uuid=str(uome_for_user.uuid))

        uome_for_user.issuer_signature = for_user_sig
        uome_for_user.save()

        assert uome_by_user.borrower_signature == ''
        assert uome_by_user.issuer_signature != ''

        assert uome_for_user.borrower_signature == ''
        assert uome_for_user.issuer_signature != ''

        signature = self.message_class.sign(self.private_key, 'user',
                                            group_uuid=str(self.group.uuid),
                                            user=self.user.key)

        request = self.message_class.make_request(group_uuid=str(self.group.uuid),
                                                  user=self.user.key,
                                                  user_signature=signature)

        raw_response = self.client.post(reverse('main_server_app:get_pending_uomes'),
                                        {'data': request.dumps()})

        assert raw_response.status_code == 200

        response = self.message_class.load_response(raw_response.content.decode())

        response.verify(settings.PUBLIC_KEY, 'main', response.main_signature,
                        group_uuid=str(self.group.uuid),
                        user=self.user.key,
                        issued_by_user=json.dumps([uome_by_user.to_array_unconfirmed()]),
                        waiting_for_user=json.dumps(
                            [uome_for_user.to_array_unconfirmed()]))

        for uome in response.issued_by_user:
            UOMeTools.verify(uome[1], uome[5],
                             group_uuid=uome[0],
                             issuer=uome[1],
                             borrower=uome[2],
                             value=uome[3],
                             description=uome[4],
                             uome_uuid=uome[6])

        for uome in response.waiting_for_user:
            UOMeTools.verify(uome[1], uome[5],
                             group_uuid=uome[0],
                             issuer=uome[1],
                             borrower=uome[2],
                             value=uome[3],
                             description=uome[4],
                             uome_uuid=uome[6])


class AcceptTests(TestCase):
    def setUp(self):
        self.message_class = msg.AcceptUOMe
        self.private_key, self.key = example_keys.C1_priv, example_keys.C1_pub
        self.group = Group.objects.create(name='test', key=example_keys.G1_pub)
        self.user = User.objects.create(group=self.group, key=self.key)
        self.lender = User.objects.create(group=self.group, key=example_keys.C2_pub)

    def test_confirm_first_uome(self):

        uome = UOMe.objects.create(group=self.group,
                                   lender=self.lender,
                                   borrower=self.user,
                                   value=10,
                                   description='test')

        issuer_signature = UOMeTools.sign(example_keys.C2_priv,
                                          group_uuid=str(self.group.uuid),
                                          issuer=self.lender.key,
                                          borrower=self.user.key,
                                          value=10,
                                          description='test',
                                          uome_uuid=str(uome.uuid))

        uome.issuer_signature = issuer_signature
        uome.save()

        assert uome.borrower_signature == ''

        signature = UOMeTools.sign(self.private_key,
                                   group_uuid=str(self.group.uuid),
                                   issuer=self.lender.key,
                                   borrower=self.user.key,
                                   value=10,
                                   description='test',
                                   uome_uuid=str(uome.uuid))

        request = self.message_class.make_request(group_uuid=str(self.group.uuid),
                                                  user=self.user.key,
                                                  uome_uuid=str(uome.uuid),
                                                  user_signature=signature)

        raw_response = self.client.post(reverse('main_server_app:accept_uome'),
                                        {'data': request.dumps()})

        assert raw_response.status_code == 200

        uome = UOMe.objects.filter(group=self.group, uuid=uome.uuid).first()
        assert uome.borrower_signature == signature

        response = self.message_class.load_response(raw_response.content.decode())

        self.message_class.verify(settings.PUBLIC_KEY, 'main', response.main_signature,
                                  group_uuid=str(self.group.uuid), user=self.user.key,
                                  uome_uuid=str(uome.uuid))

        # Confirm totals
        totals = {}
        for user in User.objects.filter(group=self.group):
            totals[user] = user.balance

        assert totals == {self.user: -uome.value, self.lender: uome.value}

        # Confirm simplified debt
        simplified_debt = defaultdict(dict)
        for user_debt in UserDebt.objects.filter(group=self.group):
            simplified_debt[user_debt.borrower][user_debt.lender] = user_debt.value

        assert simplified_debt == {self.user: {self.lender: uome.value}}


class GetTotalsTests(TestCase):
    def setUp(self):
        self.message_class = msg.CheckTotals
        self.private_key, self.key = example_keys.C1_priv, example_keys.C1_pub
        self.group = Group.objects.create(name='test', key=example_keys.G1_pub)
        self.user1 = User.objects.create(group=self.group, key=example_keys.C1_pub)
        self.user2 = User.objects.create(group=self.group, key=example_keys.C2_pub)
        self.user3 = User.objects.create(group=self.group, key=example_keys.C3_pub)

    def test_get_totals_no_uome(self):
        signature = self.message_class.sign(self.private_key, 'user',
                                            group_uuid=str(self.group.uuid),
                                            user=self.user1.key
                                            )

        request = self.message_class.make_request(group_uuid=str(self.group.uuid),
                                                  user=self.user1.key,
                                                  user_signature=signature)

        raw_response = self.client.post(reverse('main_server_app:get_totals'),
                                        {'data': request.dumps()})

        assert raw_response.status_code == 200
        response = self.message_class.load_response(raw_response.content.decode())

        assert response.user_balance == 0
        assert response.suggested_transactions == {}

    def test_get_totals_one_unconfirmed_uome(self):
        UOMe.objects.create(group=self.group, lender=self.user2, borrower=self.user1,
                            value=10, description="test", issuer_signature='meh')

        signature = self.message_class.sign(self.private_key, 'user',
                                            group_uuid=str(self.group.uuid),
                                            user=self.user1.key
                                            )

        request = self.message_class.make_request(group_uuid=str(self.group.uuid),
                                                  user=self.user1.key,
                                                  user_signature=signature)

        raw_response = self.client.post(reverse('main_server_app:get_totals'),
                                        {'data': request.dumps()})

        assert raw_response.status_code == 200
        response = self.message_class.load_response(raw_response.content.decode())

        assert response.user_balance == 0
        assert response.suggested_transactions == {}

    def test_get_totals_one_confirmed_uome(self):
        uome = UserDebt.objects.create(group=self.group, lender=self.user1,
                                       borrower=self.user2, value=1000)

        self.user1.balance = +uome.value
        self.user1.save()
        self.user2.balance = -uome.value
        self.user2.save()

        signature = self.message_class.sign(example_keys.C2_priv, 'user',
                                            group_uuid=str(self.group.uuid),
                                            user=self.user2.key
                                            )

        request = self.message_class.make_request(group_uuid=str(self.group.uuid),
                                                  user=self.user2.key,
                                                  user_signature=signature)

        raw_response = self.client.post(reverse('main_server_app:get_totals'),
                                        {'data': request.dumps()})

        assert raw_response.status_code == 200
        response = self.message_class.load_response(raw_response.content.decode())

        assert response.user_balance == -uome.value
        assert response.suggested_transactions == {self.user1.key: uome.value}
