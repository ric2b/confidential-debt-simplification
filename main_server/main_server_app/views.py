from django.shortcuts import render
from django.core.serializers import serialize
from django.http import HttpResponse
import json
from base64 import b64encode
from os import urandom  # the secrets package is only for python 3.6 :'(
from collections import defaultdict

from .models import Group, User, UOMe, UserDebt
from .services import simplify_debt
# Create your views here.
# TODO: cripto stuff!

def add_uome(request):
    group = Group.objects.filter(uuid=request.POST['group_uuid']).first()
    lender = User.objects.filter(user_id=request.POST['user_id']).first()
    borrower = User.objects.filter(user_id=request.POST['borrower']).first()
    value = request.POST['value']
    description = request.POST['description']

    UOMe.objects.create(group=group, lender=lender, borrower=borrower,
                        value=value, description=description)

    return HttpResponse('UOMe added')


def get_unconfirmed_uomes(request):
    group = Group.objects.filter(uuid=request.POST['group_uuid']).first()
    user = User.objects.filter(user_id=request.POST['user_id']).first()

    unconfirmed_uomes = UOMe.objects.filter(group=group, borrower=user, confirmed=False)

    return HttpResponse(serialize('json', unconfirmed_uomes), content_type='application/json')


def confirm_uome(request):
    group = Group.objects.filter(uuid=request.POST['group_uuid']).first()
    uome = UOMe.objects.filter(group=group, uuid=request.POST['uome_uuid']).first()
    uome.confirmed = True
    uome.save()

    group_users = User.objects.filter(group=group)

    totals = defaultdict(int)
    for user in group_users:
        totals[user.user_id] = user.balance

    new_uome = [uome.borrower, uome.lender, uome.value]
    new_totals, new_simplified_debt = simplify_debt.update_total_debt(totals, [new_uome])

    for user in group_users:
        user.balance = new_totals[user.user_id]

    # drop the previous user debt for this group
    UserDebt.objects.filter(group=group).delete()

    for borrower, user_debts in new_simplified_debt.items():
        # debts is a dict of users this borrower owes to, like {'user1': 3, 'user2':8}
        for lender, value in user_debts.items():
            new_user_debt = UserDebt.objects.create(group=group, borrower=borrower,
                                                    lender=lender, value=value)

    return HttpResponse('UOMe confirmed')


def get_total_debt(request):
    group = Group.objects.filter(uuid=request.POST['group_uuid']).first()
    user = User.objects.filter(user_id=request.POST['user_id']).first()
    
    user_debt = {}
    if user.balance < 0:
        for debt in UserDebt.objects.filter(group=group, borrower=user):
            user_debt[debt.lender] = debt.value
    elif user.balance > 0:
        for debt in UserDebt.objects.filter(group=group, lender=user):
            user_debt[debt.borrower] = debt.value

    # example: {is_borrower: True, user_debt: {'user1': val1, 'user2': val2}, rnd: 'Drmhze6EPcv0fN_81Bj-nA'}
    json_payload = json.dumps({'balance': user.balance, 'user_debt': user_debt, 'rnd': str(b64encode(urandom(32)))})
    return HttpResponse(json_payload, content_type='application/json')
