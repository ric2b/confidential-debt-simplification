from django.test import TestCase
from django.urls import reverse
import json

from .models import Group, User, UOMe, UserDebt
# Create your tests here.

#Good rules-of-thumb include having:
#
# - a separate TestClass for each model or view
# - a separate test method for each set of conditions you want to test
# - test method names that describe their function

class CheckTotalsTests(TestCase):

    def test_check_totals_one_uome(self):
        group = Group(name='test', owner='test')
        group.save()
        borrower = User(group=group, user_id='signature_key1', encryption_key='encryption_key1')
        borrower.save()
        lender = User(group=group, user_id='signature_key2', encryption_key='encryption_key2')
        lender.save()
        uome = UOMe(group=group, borrower=borrower, lender=lender, value=10, description="test").save()

        raw_response = self.client.post(reverse('main_server_app:total_debt'), 
                                            {'group_uuid': group.uuid, 'user_id':borrower.user_id})

        print(raw_response.content.decode("utf-8"))
        response = json.loads(str(raw_response.content.decode("utf-8")))
        self.assertIsNone(response['is_borrower'])
        self.assertEqual(response['user_debt'], {})
        #self.assertTrue(response['is_borrower'])
        #self.assertEqual(response['user_debt'], {lender.user_id: uome.value})