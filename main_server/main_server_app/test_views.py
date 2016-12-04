from django.test import TestCase  # TODO: check out pytest
from django.urls import reverse
from django.core import serializers
import json
import pytest
from collections import defaultdict

from .models import Group, User, UOMe, UserDebt
# Create your tests here.

#Good rules-of-thumb include having:
#
# - a separate TestClass for each model or view
# - a separate test method for each set of conditions you want to test
# - test method names that describe their function


class AddUOMeTests(TestCase):
    def setUp(self):
        group = Group(name='test', owner='test')
        group.save()
        borrower = User(group=group, user_id='signature_key1', encryption_key='encryption_key1')
        borrower.save()
        lender = User(group=group, user_id='signature_key2', encryption_key='encryption_key2')
        lender.save()

        self.group, self.borrower, self.lender = group, borrower, lender


    def test_add_first_uome(self):
        raw_response = self.client.post(reverse('main_server_app:add_uome'), 
                                                {
                                                'group_uuid': self.group.uuid, 
                                                'user_id':self.lender.user_id,
                                                'borrower':self.borrower.user_id,
                                                'value': 10,
                                                'description': 'test'
                                                })

        assert raw_response.content.decode('utf-8') == 'UOMe added'


class CancelUOMeTests(TestCase):
    def setUp(self):
        group = Group(name='test', owner='test')
        group.save()
        borrower = User(group=group, user_id='signature_key1', encryption_key='encryption_key1')
        borrower.save()
        lender = User(group=group, user_id='signature_key2', encryption_key='encryption_key2')
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
                                                'user_id': self.lender.user_id,
                                                'uome_uuid': uome.uuid                                                
                                                })

        assert raw_response.content.decode('utf-8') == 'UOMe #%i canceled' % uome.uuid
        assert UOMe.objects.filter(uuid=uome.uuid).first() == None

    # TODO: test for the other cases: uome doesn't exist, the user isn't the issuer of the uome
    # or the uome has already been confirmed


class CheckUnconfirmedUOMesTests(TestCase):
    def setUp(self):
        group = Group(name='test', owner='test')
        group.save()
        borrower = User(group=group, user_id='signature_key1', encryption_key='encryption_key1')
        borrower.save()
        lender = User(group=group, user_id='signature_key2', encryption_key='encryption_key2')
        lender.save()

        self.group, self.borrower, self.lender = group, borrower, lender


    def test_one_unconfirmed_uome(self):
        uome = UOMe(group=self.group, borrower=self.borrower, lender=self.lender,
                    value=10, description="test")
        uome.save()

        raw_response = self.client.post(reverse('main_server_app:get_unconfirmed_uomes'), 
                                                {'group_uuid': self.group.uuid, 
                                                 'user_id':self.borrower.user_id})

        # https://docs.djangoproject.com/en/1.10/topics/serialization/
        response = serializers.deserialize('json', raw_response.content)
        assert [item.object for item in response] == [uome]


class ConfirmUOMeTests(TestCase):
    def setUp(self):
        group = Group(name='test', owner='test')
        group.save()
        borrower = User(group=group, user_id='signature_key1', encryption_key='encryption_key1')
        borrower.save()
        lender = User(group=group, user_id='signature_key2', encryption_key='encryption_key2')
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
                                                 'user_id':self.borrower.user_id})

        # Confirm uome is marked as confirmed
        assert raw_response.content.decode('utf-8') == 'UOMe confirmed'
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
        group = Group(name='test', owner='test')
        group.save()
        borrower = User(group=group, user_id='signature_key1', encryption_key='encryption_key1')
        borrower.save()
        lender = User(group=group, user_id='signature_key2', encryption_key='encryption_key2')
        lender.save()

        self.group, self.borrower, self.lender = group, borrower, lender


    def test_check_totals_no_uome(self):
        raw_response = self.client.post(reverse('main_server_app:total_debt'), 
                                                {'group_uuid': self.group.uuid,
                                                 'user_id':self.borrower.user_id})

        response = json.loads(raw_response.content.decode("utf-8"))
        assert response['balance'] == 0
        assert response['user_debt'] == {}


    def test_check_totals_one_unconfirmed_uome(self):
        uome = UOMe(group=self.group, borrower=self.borrower, lender=self.lender,
                    value=10, description="test")
        uome.save()

        raw_response = self.client.post(reverse('main_server_app:total_debt'), 
                                            {'group_uuid': self.group.uuid,
                                             'user_id':self.borrower.user_id})

        response = json.loads(str(raw_response.content.decode("utf-8")))
        assert response['balance'] == 0
        assert response['user_debt'] == {}


    def test_check_totals_one_confirmed_uome(self):
        debt_value = 1000
        
        user_debt = UserDebt.objects.create(group=self.group, borrower=self.borrower, 
                                            lender=self.lender, value=debt_value)

        self.borrower.balance = -debt_value
        self.borrower.save()
        self.lender.balance = debt_value
        self.lender.save()

        raw_response = self.client.post(reverse('main_server_app:total_debt'), 
                                            {'group_uuid': self.group.uuid,
                                             'user_id':self.borrower.user_id})

        response = json.loads(str(raw_response.content.decode("utf-8")))
        assert response['balance'] == -debt_value
        assert response['user_debt'] == {self.lender.user_id: debt_value}


class RegisterGroupTests(TestCase):
    # TODO: add proxy/name server address
    def test_register_new_group(self):
        group_name = 'test_name'
        group_owner = 'test_owner'
        raw_response = self.client.post(reverse('main_server_app:register_group'), 
                                                {
                                                'group_name': group_name,
                                                'group_owner': group_owner
                                                })

        assert raw_response.content.decode("utf-8") == "Group '%s' registered" % group_name


class GetGroupInfoTests(TestCase):
    # TODO: add proxy/name server address
    def setUp(self):
        group = Group(name='test_name', owner='test_owner')
        group.save()
        self.group = group

    def test_get_existing_group(self):
        raw_response = self.client.post(reverse('main_server_app:get_group_info'), 
                                                {'group_uuid': self.group.uuid})

        expected_info = {
                         'uuid': str(self.group.uuid), 
                         'name': self.group.name, 
                         'owner': self.group.owner
                        }

        assert json.loads(raw_response.content.decode("utf-8")) == expected_info

