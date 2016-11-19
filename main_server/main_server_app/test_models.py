from django.test import TestCase  # TODO: check out pytest
from django.urls import reverse
import json

from .models import Group, User, UOMe, UserDebt
# Create your tests here.

#Good rules-of-thumb include having:
#
# - a separate TestClass for each model or view
# - a separate test method for each set of conditions you want to test
# - test method names that describe their function

class GroupTests(TestCase):
    pass


class UserTests(TestCase):
    pass


class UOMeTests(TestCase):
    pass


class UserDebtTests(TestCase):
    pass
