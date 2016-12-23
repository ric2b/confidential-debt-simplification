from django.core.serializers import serialize
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, \
    Http404
from django.db import transaction
from django.conf import settings
from collections import defaultdict
import json

from .models import Group, User, UOMe, UserDebt
from .services import simplify_debt

from utils.crypto.rsa import sign, verify, InvalidSignature
from utils.messages import message_formats as msg
from utils.messages.message import DecodeError
from utils.messages.uome_tools import UOMeTools


# Create your views here.
# TODO: crypto stuff!
# TODO: RESTify this stuff: adequate error codes, http verbs and reponses:
# https://github.com/dsi-dev-sessions/02-rest-microservices/blob/master/slides.pdf


def register_group(request):
    # convert the message into the request object
    try:
        request = msg.RegisterGroup.load_request(request.POST['data'])
    except DecodeError:
        return HttpResponseBadRequest()

    # verify the signature
    try:
        msg.RegisterGroup.verify(request.group_key, 'group', request.group_signature,
                                 group_name=request.group_name,
                                 group_key=request.group_key)
    except InvalidSignature:
        return HttpResponse('401 Unauthorized', status=401)  # There's no class for it

    # signature is correct, create the group
    # TODO: limit the length of the group name?
    group = Group.objects.create(name=request.group_name, key=request.group_key)

    # group created, create the response object
    signature = msg.RegisterGroup.sign(settings.PRIVATE_KEY, 'main',
                                       group_uuid=group.uuid,
                                       group_name=group.name,
                                       group_key=group.key)

    response = msg.RegisterGroup.make_response(group_uuid=str(group.uuid),
                                               main_signature=signature)

    # send the response, the status for success is 201 Created
    return HttpResponse(response.dumps(), status=201)


def join_group(request):
    message_class = msg.MainServerJoin

    try:  # convert the message into the request object
        request = message_class.load_request(request.POST['data'])
    except DecodeError:
        return HttpResponseBadRequest()

    try:  # check that the group exists and get it
        group = Group.objects.get(pk=request.group_uuid)
    except (ValueError, ObjectDoesNotExist):  # ValueError if the uuid is not valid
        return HttpResponseBadRequest()

    try:  # verify the signatures
        message_class.verify(request.user, 'user', request.user_signature,
                             group_uuid=group.uuid,
                             user=request.user)
        message_class.verify(group.key, 'group', request.group_signature,
                             group_uuid=group.uuid,
                             user=request.user)
    except InvalidSignature:
        return HttpResponse('401 Unauthorized', status=401)

    user = User.objects.create(group=group, key=request.user)

    # create the signature
    signature = message_class.sign(settings.PRIVATE_KEY, 'main', group_uuid=group.uuid,
                                   user=request.user)

    # user created, create the response object
    response = message_class.make_response(group_uuid=str(group.uuid), user=user.key,
                                           main_signature=signature)

    # send the response, the status for success is 201 Created
    return HttpResponse(response.dumps(), status=201)


def issue_uome(request):
    message_class = msg.IssueUOMe

    try:  # convert the message into the request object
        request = message_class.load_request(request.POST['data'])
    except DecodeError:
        return HttpResponseBadRequest()

    try:  # check that the group exists and get it
        group = Group.objects.get(pk=request.group_uuid)
        user = User.objects.filter(group=group, key=request.user).first()
        borrower = User.objects.filter(group=group, key=request.borrower).first()
    except (ValueError, ObjectDoesNotExist):  # ValueError if the uuid is not valid
        return HttpResponseBadRequest()

    if request.value <= 0:  # So it's not possible to invert the direction of the UOMe
        return HttpResponseBadRequest()

    if request.user == request.borrower:  # That would just be weird...
        return HttpResponseForbidden()

    value = request.value
    description = request.description[:settings.UOME_DESCRIPTION_MAX_LENGTH]

    try:  # verify the signatures
        message_class.verify(user.key, 'user', request.user_signature, value=value,
                             description=description, group_uuid=str(group.uuid),
                             user=user.key, borrower=borrower.key)
    except InvalidSignature:
        return HttpResponse('401 Unauthorized', status=401)

    # TODO: the description can leak information, maybe it should be encrypted
    uome = UOMe(group=group, lender=user, borrower=borrower, value=value,
                description=description)

    # create the signature
    sig = message_class.sign(settings.PRIVATE_KEY, 'main', group_uuid=group.uuid,
                             user=user.key, borrower=borrower.key, value=value,
                             description=description, uome_uuid=uome.uuid)

    # user created, create the response object
    response = message_class.make_response(uome_uuid=str(uome.uuid), main_signature=sig)

    # send the response, the status for success is 201 Created
    return HttpResponse(response.dumps(), status=201)


def cancel_uome(request):
    message_class = msg.CancelUOMe

    try:  # convert the message into the request object
        request = message_class.load_request(request.POST['data'])
    except DecodeError:
        return HttpResponseBadRequest()

    try:  # check that the group exists and get it
        group = Group.objects.get(pk=request.group_uuid)
        user = User.objects.filter(group=group, key=request.user).first()
        uome = UOMe.objects.filter(group=group, uuid=request.uome_uuid).first()
    except (ValueError, ObjectDoesNotExist):  # ValueError if the uuid is not valid
        return HttpResponseBadRequest()

    try:  # verify the signatures
        message_class.verify(user.key, 'user', request.user_signature,
                             user=user.key,
                             group_uuid=str(group.uuid),
                             uome_uuid=uome.uuid)
    except InvalidSignature:
        return HttpResponse('401 Unauthorized', status=401)

    if not uome:
        return Http404()

    else:
        if user.key == uome.lender.key and uome.borrower_signature == '':
            signature = message_class.sign(settings.PRIVATE_KEY, 'main',
                                           group_uuid=str(group.uuid),
                                           user=user.key,
                                           uome_uuid=uome.uuid)

            response = message_class.make_response(group_uuid=str(group.uuid),
                                                   user=user.key,
                                                   uome_uuid=uome.uuid,
                                                   main_signature=signature)

            uome.delete()
            return HttpResponse(response.dumps(), status=200)
        else:
            return HttpResponseForbidden()


def get_pending_uomes(request):
    message_class = msg.GetPendingUOMes

    try:  # convert the message into the request object
        request = message_class.load_request(request.POST['data'])
    except DecodeError:
        return HttpResponseBadRequest()

    try:  # check that the group exists and get it
        group = Group.objects.get(pk=request.group_uuid)
        user = User.objects.filter(group=group, key=request.user).first()
    except (ValueError, ObjectDoesNotExist):  # ValueError if the uuid is not valid
        return HttpResponseBadRequest()

    try:  # verify the signatures
        message_class.verify(user.key, 'user', request.user_signature,
                             group_uuid=str(group.uuid), user=user.key, )
    except InvalidSignature:
        return HttpResponse('401 Unauthorized', status=401)

    uomes_by_user = UOMe.objects.filter(group=group, borrower_signature='',
                                        lender=user)
    uomes_for_user = UOMe.objects.filter(group=group, borrower_signature='',
                                         borrower=user)
    issued_by_user = []
    for uome in uomes_by_user:
        issued_by_user.append(uome.to_array_unconfirmed())
    waiting_for_user = []
    for uome in uomes_for_user:
        waiting_for_user.append(uome.to_array_unconfirmed())

    signature = message_class.sign(settings.PRIVATE_KEY, 'main',
                                   group_uuid=str(group.uuid),
                                   user=user.key,
                                   issued_by_user=json.dumps(issued_by_user),
                                   waiting_for_user=json.dumps(waiting_for_user))

    response = message_class.make_response(group_uuid=str(group.uuid),
                                           user=user.key,
                                           issued_by_user=issued_by_user,
                                           waiting_for_user=waiting_for_user,
                                           main_signature=signature)

    return HttpResponse(response.dumps(), status=200)


# TODO: Think about data races a lot more
@transaction.atomic
def accept_uome(request):
    message_class = msg.AcceptUOMe

    try:  # convert the message into the request object
        request = message_class.load_request(request.POST['data'])
    except DecodeError:
        return HttpResponseBadRequest()

    try:  # check that the group exists and get it
        group = Group.objects.get(pk=request.group_uuid)
        lender = User.objects.filter(group=group, key=request.lender).first()
        user = User.objects.filter(group=group, key=request.user).first()
        uome = UOMe.objects.filter(group=group, uuid=request.uome_uuid).first()
    except (ValueError, ObjectDoesNotExist):  # ValueError if the uuid is not valid
        return HttpResponseBadRequest()

    if uome.group != group:
        return HttpResponseBadRequest()

    try:  # verify the signatures
        message_class.verify(user.key, 'user', request.user_signature,
                             group_uuid=str(group.uuid),
                             lender=lender.key,
                             user=user.key,
                             value=request.value,
                             description=request.description,
                             uome_uuid=str(uome.uuid))

        UOMeTools.borrower_verify(user.key, request.user_signature,
                                  group_uuid=str(group.uuid),
                                  issuer=lender.key,
                                  borrower=user.key,
                                  value=request.value,
                                  description=request.description,
                                  uome_uuid=str(uome.uuid))
    except InvalidSignature:
        return HttpResponse('401 Unauthorized', status=401)

    uome.borrower_signature = request.user_signature
    uome.save()

    # create the signature
    sig = message_class.sign(settings.PRIVATE_KEY, 'main', group_uuid=group.uuid,
                             user=user.key, uome_uuid=uome.uuid)
    # create the response object
    response = message_class.make_response(uome_uuid=str(uome.uuid), main_signature=sig)

    # update the balances and suggestions of users
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

    # send the response, the status for success is 200 OK
    return HttpResponse(response.dumps(), status=200)


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
