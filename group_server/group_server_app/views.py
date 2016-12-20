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
        
    #Save invitee in the pending user database with his email
    user2 = User.objects.create(group=group, key=request.invitee, email=request.invitee_email)
    
    #Generate secret code
    secret_code = str(int.from_bytes(os.urandom(4), byteorder="big"))
    
    #Get invitee object
    invitee = User.objects.get(pk=request.invitee)
    
    #Create Invitation entry
    invitation = Invitation.objects.create(inviter=inviter, invitee=invitee, signature_inviter=request.inviter_signature, secret_code=secret_code)
    
    # create the signature
    sig = message_class.sign(settings.PRIVATE_KEY, 'group', group_uuid=group.uuid,
                             inviter=inviter.key, invitee=request.invitee, invitee_email=request.invitee_email)

    # user created, create the response object
    response = message_class.make_response(group_signature=sig)
    
    return HttpResponse(response.dumps(), status=201)
    
def join_group(request):
    return

def confirm_join(request):
    return

def email_key_map(request):
    return
