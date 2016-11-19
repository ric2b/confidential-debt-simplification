from django.test import TestCase  # TODO: check out pytest
from django.urls import reverse
from django.core import serializers
import json

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

        self.assertEqual(raw_response.content.decode('utf-8'), 'UOMe added')


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
        self.assertEqual([item.object for item in response], [uome])


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

        self.assertEqual(raw_response.content.decode('utf-8'), 'UOMe confirmed')
        self.assertIs(UOMe.objects.filter(group=self.group, uuid=uome.uuid).first().confirmed, True)


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
        self.assertIs(response['is_borrower'], None)
        self.assertEqual(response['user_debt'], {})


    def test_check_totals_one_unconfirmed_uome(self):
        return
        raise NotImplementedError


    def test_check_totals_one_confirmed_uome(self):
        return
        raise NotImplementedError
        uome = UOMe(group=group, borrower=borrower, lender=lender, value=10, description="test").save()

        raw_response = self.client.post(reverse('main_server_app:total_debt'), 
                                            {'group_uuid': group.uuid, 'user_id':borrower.user_id})

        response = json.loads(str(raw_response.content.decode("utf-8")))
        self.assertIs(response['is_borrower'], True)
        self.assertEqual(response['user_debt'], {lender.user_id: uome.value})
