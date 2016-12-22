from django.core.serializers import serialize
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.db import transaction
from django.conf import settings
from collections import defaultdict
import json
import os

from .models import Group, User, Invitation, ConfirmedInvitation

from utils.crypto.rsa import sign, verify, InvalidSignature
from utils.messages import message_formats as msg
from utils.messages.message import DecodeError

# Create your views here.

def invite_user(request):
    message_class = msg.UserInvite
    
    try:  # convert the message into the request object
        request = message_class.load_request(request.POST['data'])
    except DecodeError:
        return HttpResponseBadRequest()
        
    try:  # check that the inviter belonging to group exists and return it
        inviter = User.objects.get(key=request.inviter, group_id=request.group_uuid)
        group = Group.objects.get(pk=request.group_uuid)
    except (ValueError, ObjectDoesNotExist):  # ValueError if the uuid is not valid
        return HttpResponseBadRequest()
        
    try:
        message_class.verify(inviter.key, 'inviter', request.inviter_signature,
                                 group_uuid=request.group_uuid,
                                 inviter=request.inviter,
                                 invitee=request.invitee,
                                 invitee_email=request.invitee_email)
    except InvalidSignature:
        return HttpResponse('401 Unauthorized', status=401)  # There's no class for it
        
        
    #Check if the invitee already exists in the group   
    
    if User.objects.filter(key=request.invitee).exists():
        return HttpResponse('409 Conflict', status=409)
        
    #Save invitee in the pending user database with his email
    user2 = User.objects.create(group=group, key=request.invitee, email=request.invitee_email)
    
    #Generate secret code
    secret_code = str(int.from_bytes(os.urandom(4), byteorder="big")) #Is it big enough?
    
    #Get invitee object
    invitee = User.objects.get(pk=request.invitee)
    
    #Create Invitation entry
    invitation = Invitation.objects.create(group=group, inviter=inviter, invitee=invitee, signature_inviter=request.inviter_signature, secret_code=secret_code)
    
    # create the signature
    sig = message_class.sign(settings.PRIVATE_KEY, 'group', group_uuid=group.uuid,
                             inviter=inviter.key, invitee=request.invitee, invitee_email=request.invitee_email)

    response = message_class.make_response(group_signature=sig)
    
    return HttpResponse(response.dumps(), status=201)
    
def join_group(request):
    message_class = msg.GroupServerJoin
    
    try:  # convert the message into the request object
        request = message_class.load_request(request.POST['data'])
    except DecodeError:
        return HttpResponseBadRequest()
        
    try:  # check that the inviter belonging to group exists and return it
        user = User.objects.get(key=request.user, group_id=request.group_uuid)
        group = Group.objects.get(pk=request.group_uuid)
    except (ValueError, ObjectDoesNotExist):  # ValueError if the uuid is not valid
        return HttpResponseBadRequest()
        
    try:
        message_class.verify(user.key, 'user', request.user_signature,
                                 group_uuid=request.group_uuid,
                                 user=user.key,
                                 secret_code=request.secret_code)
    except InvalidSignature:
        return HttpResponse('401 Unauthorized', status=401)  
     
    try:    
        invitation = Invitation.objects.get(secret_code=request.secret_code, invitee=user, group=group)
    except (ValueError, ObjectDoesNotExist):
        return HttpResponseForbiddenRequest()  
        
    #TODO: Confirm user registration now?
    
    # create the signature
    sig = message_class.sign(settings.PRIVATE_KEY, 'group', inviter_signature = invitation.signature_inviter)
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
        sig = message_class.sign(settings.PRIVATE_KEY, 'group', inviter_signature = invitation.signature_inviter)
        message_class.verify(user.key, 'user', request.user_signature, group_signature=sig)
    except InvalidSignature:
        return HttpResponse('401 Unauthorized', status=401)  
        
    if user.confirmed:
        return HttpResponse('409 Conflict', status=409)
        
    #Change user status to confirmed
    user.confirmed = True
    user.save()

    response = message_class.make_response(group_uuid=str(group.uuid), user=user.key)


    return HttpResponse(response.dumps(), status=200)

def email_key_map(request):
    return
