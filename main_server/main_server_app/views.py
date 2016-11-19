from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
import json
from base64 import b64encode
from os import urandom  # the secrets package is only for python 3.6 :'(

from .models import Group, User, UOMe, UserDebt
# Create your views here.


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
    group = Group.objects.filter(uuid=request.POST['group_uuid'])
    user = User.objects.filter(user_id=request.POST['user_id']).first()

    unconfirmed_uomes = UOMe.objects.filter(group=group, borrower=user, confirmed=False)

    return HttpResponse(serializers.serialize('json', unconfirmed_uomes), content_type='application/json')


def confirm_uome(request):
    raise NotImplementedError
    group = Group.objects.filter(uuid=request.POST['group_uuid'])
    previous_totals = UserDebt.objects.filter(group=group)
    # TODO: convert previous_totals to defaultdict
    new_totals = simplify_debt.compute_totals(previous_totals, [new_uome])


def get_total_debt(request):
    # TODO: cripto stuff!
    group = Group.objects.filter(uuid=request.POST['group_uuid'])
    user = User.objects.filter(user_id=request.POST['user_id']).first()
    is_borrower = user.is_net_borrower
    
    user_debt = {}
    if is_borrower is not None:
        if is_borrower:
            for debt in UserDebt.objects.filter(group=group, borrower=user):
                user_debt[debt.lender] = debt.value
        else:
            for debt in UserDebt.objects.filter(group=group, lender=user):
                user_debt[debt.borrower] = debt.value

    # example: {is_borrower: True, user_debt: {'user1': val1, 'user2': val2}, rnd: 'Drmhze6EPcv0fN_81Bj-nA'}
    json_payload = json.dumps({'is_borrower': is_borrower, 'user_debt': user_debt, 'rnd': str(b64encode(urandom(32)))})
    return HttpResponse(json_payload, content_type='application/json')
