from django.test import TestCase  # TODO: check out pytest
from django.urls import reverse
from django.core import serializers
from django.conf import settings
import json

from collections import defaultdict

from .models import Group, User, UOMe, UserDebt

from utils.crypto.rsa import generate_keys, sign, verify
from utils.messages import requests, responses

# Create your tests here.

# Good rules-of-thumb include having:
#
# - a separate TestClass for each model or view
# - a separate test method for each set of conditions you want to test
# - test method names that describe their function


class RegisterGroupTests(TestCase):
    def setUp(self):
        self.private_key, self.key = generate_keys()

    # TODO: add proxy/name server address
    def test_register_new_group(self):
        group_name = 'test_name'
        key = self.key

        signature = sign(self.private_key, group_name, key)
        message_data = requests.RegisterGroup(group_name=group_name,
                                              group_key=key,
                                              group_signature=signature)

        raw_response = self.client.post(reverse('main_server_app:register_group'),
                                        {'data': message_data.body})

        print(raw_response.content.decode())
        response = responses.RegisterGroup.load(raw_response.content.decode())

        signature_content = [response.group_uuid, group_name, key]
        verify(settings.PUBLIC_KEY, response.main_signature, *signature_content)


class RegisterUserTests(TestCase):
    def setUp(self):
        group = Group(name='test', key='test')
        group.save()
        self.group = group

    def test_register_new_user_to_existing_group(self):
        signing_key = 'test_signing_key'

        raw_response = self.client.post(reverse('main_server_app:register_user'),
                                        {
                                            'group_uuid': self.group.uuid,
                                            'user_key': signing_key,
                                        })

        assert raw_response.content.decode() == "User '%s' registered" % signing_key


class AddUOMeTests(TestCase):
    def setUp(self):
        group = Group(name='test', key='test')
        group.save()
        borrower = User(group=group, key='signature_key1')
        borrower.save()
        lender = User(group=group, key='signature_key2')
        lender.save()

        self.group, self.borrower, self.lender = group, borrower, lender

    def test_add_first_uome(self):
        raw_response = self.client.post(reverse('main_server_app:add_uome'),
                                        {
                                            'group_uuid': self.group.uuid,
                                            'lender': self.lender.key,
                                            'borrower': self.borrower.key,
                                            'value': 10,
                                            'description': 'test'
                                        })

        assert raw_response.content.decode() == 'UOMe added'


class CancelUOMeTests(TestCase):
    def setUp(self):
        group = Group(name='test', key='test')
        group.save()
        borrower = User(group=group, key='signature_key1')
        borrower.save()
        lender = User(group=group, key='signature_key2')
        lender.save()

        self.group, self.borrower, self.lender = group, borrower, lender

    def test_cancel_unconfirmed_uome(self):
        uome = UOMe(group=self.group, borrower=self.borrower, lender=self.lender,
                    value=10, description="test")
        uome.save()

        assert UOMe.objects.filter(uuid=uome.uuid).first() == uome

        raw_response = self.client.post(reverse('main_server_app:cancel_uome'),
                                        {
                                            'group_uuid': self.group.uuid,
                                            'user_key': self.lender.key,
                                            'uome_uuid': uome.uuid
                                        })

        assert raw_response.content.decode('utf-8') == 'UOMe #%i canceled' % uome.uuid
        assert UOMe.objects.filter(uuid=uome.uuid).first() is None

        # TODO: test for the other cases: uome doesn't exist, the user isn't the issuer of the uome
        # or the uome has already been confirmed


class CheckUnconfirmedUOMesTests(TestCase):
    def setUp(self):
        group = Group(name='test', key='test')
        group.save()
        borrower = User(group=group, key='signature_key1')
        borrower.save()
        lender = User(group=group, key='signature_key2')
        lender.save()

        self.group, self.borrower, self.lender = group, borrower, lender

    def test_one_unconfirmed_uome(self):
        uome = UOMe(group=self.group, borrower=self.borrower, lender=self.lender,
                    value=10, description="test")
        uome.save()

        raw_response = self.client.post(reverse('main_server_app:get_unconfirmed_uomes'),
                                        {'group_uuid': self.group.uuid,
                                         'user_key': self.borrower.key})

        # https://docs.djangoproject.com/en/1.10/topics/serialization/
        response = serializers.deserialize('json', raw_response.content)
        assert [item.object for item in response] == [uome]


class ConfirmUOMeTests(TestCase):
    def setUp(self):
        group = Group(name='test', key='test')
        group.save()
        borrower = User(group=group, key='signature_key1')
        borrower.save()
        lender = User(group=group, key='signature_key2')
        lender.save()

        self.group, self.borrower, self.lender = group, borrower, lender

    def test_confirm_first_uome(self):
        uome = UOMe(group=self.group, borrower=self.borrower, lender=self.lender,
                    value=10, description="test")
        uome.save()
        self.assertIs(uome.confirmed, False)

        raw_response = self.client.post(reverse('main_server_app:confirm_uome'),
                                        {'group_uuid': self.group.uuid,
                                         'uome_uuid': uome.uuid,
                                         'user_key': self.borrower.key})

        # Confirm uome is marked as confirmed
        assert raw_response.content.decode() == 'UOMe confirmed'
        assert UOMe.objects.filter(group=self.group, uuid=uome.uuid).first().confirmed == True

        # Confirm totals
        totals = {}
        for user in User.objects.filter(group=self.group):
            totals[user] = user.balance

        assert totals == {self.borrower: -uome.value, self.lender: uome.value}

        # Confirm simplified debt
        simplified_debt = defaultdict(dict)
        for user_debt in UserDebt.objects.filter(group=self.group):
            simplified_debt[user_debt.borrower][user_debt.lender] = user_debt.value

        assert simplified_debt == {self.borrower: {self.lender: uome.value}}


class CheckTotalsTests(TestCase):
    def setUp(self):
        group = Group(name='test', key='test')
        group.save()
        borrower = User(group=group, key='signature_key1')
        borrower.save()
        lender = User(group=group, key='signature_key2')
        lender.save()

        self.group, self.borrower, self.lender = group, borrower, lender

    def test_check_totals_no_uome(self):
        raw_response = self.client.post(reverse('main_server_app:total_debt'),
                                        {'group_uuid': self.group.uuid,
                                         'user_key': self.borrower.key})

        response = json.loads(raw_response.content.decode())
        assert response['balance'] == 0
        assert response['user_debt'] == {}

    def test_check_totals_one_unconfirmed_uome(self):
        uome = UOMe(group=self.group, borrower=self.borrower, lender=self.lender,
                    value=10, description="test")
        uome.save()

        raw_response = self.client.post(reverse('main_server_app:total_debt'),
                                        {'group_uuid': self.group.uuid,
                                         'user_key': self.borrower.key})

        response = json.loads(str(raw_response.content.decode()))
        assert response['balance'] == 0
        assert response['user_debt'] == {}

    def test_check_totals_one_confirmed_uome(self):
        debt_value = 1000

        UserDebt.objects.create(group=self.group, borrower=self.borrower, lender=self.lender, value=debt_value)

        self.borrower.balance = -debt_value
        self.borrower.save()
        self.lender.balance = debt_value
        self.lender.save()

        raw_response = self.client.post(reverse('main_server_app:total_debt'),
                                        {'group_uuid': self.group.uuid,
                                         'user_key': self.borrower.key})

        response = json.loads(str(raw_response.content.decode()))
        assert response['balance'] == -debt_value
        assert response['user_debt'] == {self.lender.key: debt_value}
