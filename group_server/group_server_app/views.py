from django.core.serializers import serialize
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.db import transaction
from django.conf import settings
from collections import defaultdict
from django.core.mail import send_mail
from utils.messages.connection import connect, Connection
import json
import os

from .models import Group, User, Invitation

from utils.crypto.rsa import sign, verify, InvalidSignature
from utils.messages import message_formats as msg
from utils.messages.message import DecodeError

# Create your views here.

class SecurityException(Exception):
    pass


def invite_user(request):
    message_class = msg.UserInvite
    
    try:  # convert the message into the request object
        request = message_class.load_request(request.POST['data'])
    except DecodeError:
        return HttpResponseBadRequest()
        
    try:  # check that the inviter belonging to group exists and return it
        user = User.objects.get(key=request.user, group_id=request.group_uuid)
        group = Group.objects.get(pk=request.group_uuid)
    except (ValueError, ObjectDoesNotExist):
        return HttpResponseBadRequest()
        
    try:
        message_class.verify(user.key, 'user', request.user_signature,
                                 group_uuid=request.group_uuid,
                                 user=request.user,
                                 invitee=request.invitee,
                                 invitee_email=request.invitee_email)
    except InvalidSignature:
        return HttpResponse('401 Unauthorized', status=401)  # There's no class for it
        
        
    #Check if the invitee already exists in the group   
    
    if User.objects.filter(key=request.invitee).exists():
        return HttpResponse('409 Conflict', status=409)
        
    #Check if the inviter is a registered (confirmed) user
    if not user.confirmed:
        return HttpResponseForbidden()
        
    #Save invitee in the pending user database with his email (not yet confirmed)
    invitee = User.objects.create(group=group, key=request.invitee, email=request.invitee_email)
    
    #Generate secret code
    secret_code = str(int.from_bytes(os.urandom(4), byteorder="big")) #Is it big enough?
    
    #Set proxy URL
    proxy_url = 'proxy.com' #TODO: change to proxy address
    
    # SEND EMAIL TO C2
    
    send_mail(
    'MutualDebt Registration',
    user.key + ' ' + secret_code + ' ' + proxy_url,
    'registration@example.com',
    [invitee.email],
    fail_silently=False, 
    )
    
    #Create Invitation entry
    invitation = Invitation.objects.create(group=group, inviter=user, invitee=invitee, signature_inviter=request.user_signature, secret_code=secret_code)
    
    # create the signature
    sig = message_class.sign(settings.PRIVATE_KEY, 'group', group_uuid=group.uuid,
                             user=user.key, invitee=request.invitee, invitee_email=request.invitee_email)

    response = message_class.make_response(group_signature=sig)
    
    return HttpResponse(response.dumps(), status=201)
    
def join_group(request):
    message_class = msg.GroupServerJoin
    
    try:  # convert the message into the request object
        request = message_class.load_request(request.POST['data'])
    except DecodeError:
        return HttpResponseBadRequest()
        
    try:  
        user = User.objects.get(key=request.user, group_id=request.group_uuid)
        group = Group.objects.get(pk=request.group_uuid)
    except (ValueError, ObjectDoesNotExist):
        return HttpResponseBadRequest()
        
    try:
        message_class.verify(user.key, 'user', request.user_signature,
                                 group_uuid=request.group_uuid,
                                 user=user.key,
                                 secret_code=request.secret_code)
    except InvalidSignature:
        return HttpResponse('401 Unauthorized', status=401)  
        
    #Check if user has already been registered before
    if user.confirmed:
        return HttpResponse('409 Conflict', status=409)
    
    #Check id the secret code is valid 
    try:    
        invitation = Invitation.objects.get(secret_code=request.secret_code, invitee=user, group=group)
    except (ValueError, ObjectDoesNotExist):
        return HttpResponseForbiddenRequest()  
        
    # create the signature
    sig = message_class.sign(settings.PRIVATE_KEY, 'group', inviter_signature = invitation.signature_inviter)
    invitation.signature_group = sig
    invitation.save()
    response = message_class.make_response(inviter=invitation.inviter.key, user=user.key, user_email=user.email, inviter_signature=invitation.signature_inviter, group_signature=sig)
        
    return HttpResponse(response.dumps(), status=201)

def confirm_join(request):

    message_class = msg.ConfirmJoin
    
    try:  # convert the message into the request object
        request = message_class.load_request(request.POST['data'])
    except DecodeError:
        return HttpResponseBadRequest()
        
    try:  
        user = User.objects.get(key=request.user, group_id=request.group_uuid)
        group = Group.objects.get(pk=request.group_uuid)
    except (ValueError, ObjectDoesNotExist):  # ValueError if the uuid is not valid
        return HttpResponseBadRequest()
        
    try:
        invitation = Invitation.objects.get(invitee=user, group=group)
        message_class.verify(user.key, 'user', request.user_signature, group_uuid=str(group.uuid), user=user.key, group_server_signature=invitation.signature_group)
    except InvalidSignature:
        return HttpResponse('401 Unauthorized', status=401)  
        
    if user.confirmed:
        return HttpResponse('409 Conflict', status=409)
        
    #Confirm to main server successfull registration of user
    main_server_url = 'address/join-group' #TODO: change to real address
    
    group_signature = msg.MainServerJoin.sign(settings.PRIVATE_KEY, 'group', group_uuid=str(group.uuid), user=user.key)
    
    with connect(main_server_url) as connection:
        request_main = msg.MainServerJoin.make_request(group_uuid=str(group.uuid), user=user.key, group_signature=group_signature)
        connection.request(request_main)
        
        try:
            response = connection.get_response(msg.MainServerJoin)   

        except DecodeError:
            raise SecurityException('Response format not correct')
            
        try:
            msg.MainServerJoin.verify(settings.MAIN_PUBLIC_KEY, 'main', response.main_signature, group_uuid=str(group.uuid), user=user.key)
        except InvalidSignature:
            raise SecurityException('Signature of the response is invalid')    
    
    #Save user_signature
    invitation.signature_invitee = request.user_signature
    invitation.save()
        
    #Change user status to confirmed
    user.confirmed = True
    user.save()

    response = message_class.make_response(group_uuid=str(group.uuid), user=user.key)


    return HttpResponse(response.dumps(), status=200)

def email_key_map(request):

    message_class = msg.EmailKeyMap
    
    try:  # convert the message into the request object
        request = message_class.load_request(request.POST['data'])
    except DecodeError:
        return HttpResponseBadRequest()

    try:  
        user = User.objects.get(key=request.user, group_id=request.group_uuid)
        group = Group.objects.get(pk=request.group_uuid)
    except (ValueError, ObjectDoesNotExist):  # ValueError if the uuid is not valid
        return HttpResponseBadRequest()

    if not user.confirmed:
        return HttpResponseForbiddenRequest()

    try:
        message_class.verify(user.key, 'user', request.signature,
                                 group_uuid=request.group_uuid,
                                 request_type='email-key-map')
    except InvalidSignature:
        return HttpResponse('401 Unauthorized', status=401)
        
    keymap = User.objects.filter(group_id=request.group_uuid, confirmed=True)
    
    mapkey = ''
    
    for person in keymap:
        mapkey = mapkey + person.email + ':' + person.key + '\n'
        
    response = message_class.make_response(mapkey=mapkey)     
      

    return HttpResponse(response.dumps(), status=200)
