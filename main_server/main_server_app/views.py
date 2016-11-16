from django.shortcuts import render
from django.http import HttpResponse
import json
from base64 import b64encode
from os import urandom  # the secrets package is only for python 3.6 :'(

from .models import Group, User, UserDebt
# Create your views here.

def get_total_debt(request):
    # TODO: cripto stuff!
    group = Group.objects.filter(uuid=request.POST['group_uuid'])
    user = User.objects.filter(user_id=request.POST['user_id'])[0]
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
    return HttpResponse(json_payload)
