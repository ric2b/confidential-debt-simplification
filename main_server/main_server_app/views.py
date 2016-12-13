from django.core.serializers import serialize
from django.http import HttpResponse
from django.db import transaction
from django.conf import settings
from collections import defaultdict
import json

from .models import Group, User, UOMe, UserDebt
from .services import simplify_debt

from utils.crypto.rsa import sign, verify
from utils.messages import requests, responses

# Create your views here.
# TODO: crypto stuff!
# TODO: RESTify this stuff: adequate error codes, http verbs and reponses:
# https://github.com/dsi-dev-sessions/02-rest-microservices/blob/master/slides.pdf


def register_group(request):
    # convert the message into the request object
    request = requests.RegisterGroup.load(request.POST['data'])

    # verify the signature
    signature_content = [request.group_name, request.group_key]
    verify(request.group_key, request.group_signature, *signature_content)

    # signature is correct, create the group
    group = Group(name=request.group_name, key=request.group_key)
    group.save()

    # group created, create the response object
    signature = sign(settings.PRIVATE_KEY, group.uuid, group.name, group.key)
    response = responses.RegisterGroup(group_uuid=str(group.uuid), main_signature=signature)

    # send the response, the status for success is 201 Created
    return HttpResponse(response.body, status=201)


def register_user(request):
    group = Group.objects.filter(uuid=request.POST['group_uuid']).first()

    user = User(group=group,
                key=request.POST['user_key'])
    user.save()

    return HttpResponse("User '%s' registered" % user.key)


def add_uome(request):
    group = Group.objects.filter(uuid=request.POST['group_uuid']).first()
    lender = User.objects.filter(key=request.POST['lender']).first()
    borrower = User.objects.filter(key=request.POST['borrower']).first()
    value = request.POST['value']
    description = request.POST['description']

    UOMe.objects.create(group=group, lender=lender, borrower=borrower,
                        value=value, description=description)

    return HttpResponse('UOMe added')


def cancel_uome(request):
    user = User.objects.filter(group=request.POST['group_uuid'],
                               key=request.POST['user_key']).first()

    uome = UOMe.objects.filter(uuid=request.POST['uome_uuid']).first()

    if not uome:
        return HttpResponse('UOMe #%i not found' % uome.uuid)

    else:
        if user.key == uome.lender.key:
            uome_uuid = uome.uuid
            uome.delete()
            return HttpResponse('UOMe #%i canceled' % uome_uuid)
        else:
            return HttpResponse('User is not the issuer of uuid #%i' % uome.uuid)


def get_unconfirmed_uomes(request):
    group = Group.objects.filter(uuid=request.POST['group_uuid']).first()
    user = User.objects.filter(key=request.POST['user_key']).first()

    unconfirmed_uomes = UOMe.objects.filter(group=group, borrower=user, confirmed=False)

    return HttpResponse(serialize('json', unconfirmed_uomes), content_type='application/json')


# TODO: Think about data races a lot more
@transaction.atomic
def confirm_uome(request):
    group = Group.objects.filter(uuid=request.POST['group_uuid']).first()
    uome = UOMe.objects.filter(group=group, uuid=request.POST['uome_uuid']).first()
    uome.confirmed = True
    uome.save()

    group_users = User.objects.filter(group=group)

    totals = defaultdict(int)
    for user in group_users:
        totals[user] = user.balance

    new_uome = [uome.borrower, uome.lender, uome.value]
    new_totals, new_simplified_debt = simplify_debt.update_total_debt(totals, [new_uome])

    for user in group_users:
        user.balance = new_totals[user]
        user.save()

    # drop the previous user debt for this group, since it's now useless
    UserDebt.objects.filter(group=group).delete()

    for borrower, user_debts in new_simplified_debt.items():
        # debts is a dict of users this borrower owes to, like {'user1': 3, 'user2':8}
        for lender, value in user_debts.items():
            UserDebt.objects.create(group=group, value=value,
                                    borrower=borrower, lender=lender, )

    return HttpResponse('UOMe confirmed')


def get_total_debt(request):
    group = Group.objects.filter(uuid=request.POST['group_uuid']).first()
    user = User.objects.filter(key=request.POST['user_key']).first()
    
    user_debt = {}

    if user.balance < 0:  # filter by borrower
        for debt in UserDebt.objects.filter(group=group, borrower=user):
            user_debt[debt.lender.key] = debt.value

    elif user.balance > 0:  # filter by lender
        for debt in UserDebt.objects.filter(group=group, lender=user):
            user_debt[debt.borrower.key] = debt.value

    # example: {is_borrower: True, user_debt: {'user1': val1, 'user2': val2}}
    json_payload = json.dumps({'balance': user.balance,
                               'user_debt': user_debt,
                               })

    return HttpResponse(json_payload, content_type='application/json')
