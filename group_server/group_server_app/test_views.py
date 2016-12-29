from django.test import TestCase  # TODO: check out pytest
from django.urls import reverse
from django.core import serializers
from django.conf import settings
import json
from uuid import uuid4

from collections import defaultdict

from .models import Group, User, Invitation

from utils.crypto.rsa import generate_keys, sign, verify
from utils.crypto import example_keys
from utils.messages import message_formats as msg


# Create your tests here.

# Good rules-of-thumb include having:
#
# - a separate TestClass for each model or view
# - a separate test method for each set of conditions you want to test
# - test method names that describe their function


class InviteUserTests(TestCase):
    def setUp(self):
        self.message_class = msg.UserInvite
        self.private_key, self.key = example_keys.C1_priv, example_keys.C1_pub
        self.group = Group.objects.create(name='test', key=example_keys.G1_pub)
        self.group2 = Group.objects.create(name='test2', key=example_keys.G2_pub)
        self.inviter = User.objects.create(group=self.group, key=self.key, email='c1@example.pt', confirmed=True)
        
    def test_correct_input(self):
        signature = self.message_class.sign(self.private_key, 'inviter', group_uuid=str(self.group.uuid), inviter=self.inviter.key, invitee=example_keys.C2_pub,invitee_email='c2@example.pt')
        request = self.message_class.make_request(group_uuid=str(self.group.uuid), inviter=self.inviter.key, invitee=example_keys.C2_pub, invitee_email='c2@example.pt', inviter_signature=signature)
        raw_response = self.client.post(reverse('group_server_app:invite_user'),{'data': request.dumps()})
        assert raw_response.status_code == 201
    
    def test_inviter_different_group_error(self):
        signature = self.message_class.sign(self.private_key, 'inviter', group_uuid=str(self.group.uuid), inviter=self.inviter.key, invitee=example_keys.C2_pub,invitee_email='c2@example.pt')
        request = self.message_class.make_request(group_uuid=str(self.group2.uuid), inviter=self.inviter.key, invitee=example_keys.C2_pub, invitee_email='c2@example.pt', inviter_signature=signature)
        raw_response = self.client.post(reverse('group_server_app:invite_user'),{'data': request.dumps()})
        assert raw_response.status_code == 400
        
    def test_invalid_signature(self):
        signature = 'invalidsignature'
        request = self.message_class.make_request(group_uuid=str(self.group.uuid), inviter=self.inviter.key, invitee=example_keys.C2_pub, invitee_email='c2@example.pt', inviter_signature=signature)
        raw_response = self.client.post(reverse('group_server_app:invite_user'),{'data': request.dumps()})
        assert raw_response.status_code == 401
        
    def test_valid_user2_entry(self):
        signature = self.message_class.sign(self.private_key, 'inviter', group_uuid=str(self.group.uuid), inviter=self.inviter.key, invitee=example_keys.C2_pub,invitee_email='c2@example.pt')
        request = self.message_class.make_request(group_uuid=str(self.group.uuid), inviter=self.inviter.key, invitee=example_keys.C2_pub, invitee_email='c2@example.pt', inviter_signature=signature)
        
        self.user2 = User.objects.create(group=self.group, key=request.invitee, email=request.invitee_email)
        
        assert self.user2.key == request.invitee
        assert self.user2.email == request.invitee_email
       
    def test_invited_user_already_exists(self):
        self.invitee = User.objects.create(group=self.group, key=example_keys.C2_pub, email='c2@example.pt')
        signature = self.message_class.sign(self.private_key, 'inviter', group_uuid=str(self.group.uuid), inviter=self.inviter.key, invitee=example_keys.C2_pub,invitee_email='c2@example.pt')
        request = self.message_class.make_request(group_uuid=str(self.group.uuid), inviter=self.inviter.key, invitee=example_keys.C2_pub, invitee_email='c2@example.pt', inviter_signature=signature)
        raw_response = self.client.post(reverse('group_server_app:invite_user'),{'data': request.dumps()})
        
        assert raw_response.status_code == 409
        
    def test_inviter_not_confirmed(self):
        inviter3 = User.objects.create(group=self.group, key=example_keys.C3_pub, email='c1@example.pt')
        signature = self.message_class.sign(example_keys.C3_priv, 'inviter', group_uuid=str(self.group.uuid), inviter=inviter3.key, invitee=example_keys.C2_pub,invitee_email='c2@example.pt')
        request = self.message_class.make_request(group_uuid=str(self.group.uuid), inviter=inviter3.key, invitee=example_keys.C2_pub, invitee_email='c2@example.pt', inviter_signature=signature)
        raw_response = self.client.post(reverse('group_server_app:invite_user'),{'data': request.dumps()})
        
        assert raw_response.status_code == 403        
        
class JoinGroupTests(TestCase):
    def setUp(self):
        self.message_class = msg.GroupServerJoin
        self.private_key2, self.key2 = example_keys.C2_priv, example_keys.C2_pub
        self.group = Group.objects.create(name='test', key=example_keys.G1_pub)
        self.user = User.objects.create(group=self.group, key=self.key2, email='c2@example.pt')
        self.private_key1, self.key1 = example_keys.C1_priv, example_keys.C1_pub
        self.inviter = User.objects.create(group=self.group, key=self.key1, email='c1@example.pt', confirmed=True)
        self.group2 = Group.objects.create(name='test2', key=example_keys.G2_pub)
        
    
    def test_correct_input(self):
        signature = msg.UserInvite.sign(self.private_key1, 'inviter', group_uuid=str(self.group.uuid), inviter=self.inviter.key, invitee=example_keys.C2_pub, invitee_email='c2@example.pt')
        invitation = Invitation.objects.create(group=self.group, invitee=self.user, inviter=self.inviter, signature_inviter=signature, secret_code='0000')
        
        signature2 = self.message_class.sign(self.private_key2, 'user', group_uuid=str(self.group.uuid), user=self.user.key, secret_code='0000')
        request = self.message_class.make_request(group_uuid=str(self.group.uuid), user=self.user.key, secret_code='0000', user_signature=signature2)
        raw_response = self.client.post(reverse('group_server_app:join_group'),{'data': request.dumps()})
        
        assert raw_response.status_code == 201
        
        
    
        

class ConfirmJoinTests(TestCase): 
    def setUp(self): 
        self.message_class = msg.ConfirmJoin 
        self.private_key2, self.key2 = example_keys.C2_priv, example_keys.C2_pub 
        self.group = Group.objects.create(name='test', key=example_keys.G1_pub) 
        self.user = User.objects.create(group=self.group, key=self.key2, email='c2@example.pt') 
        self.private_key1, self.key1 = example_keys.C1_priv, example_keys.C1_pub 
        self.inviter = User.objects.create(group=self.group, key=self.key1, email='c1@example.pt', confirmed=True) 
        
         
    def test_correct_input(self): 
        inviter_signature = msg.UserInvite.sign(self.private_key1, 'inviter', group_uuid=str(self.group.uuid), inviter=self.inviter.key, invitee=example_keys.C2_pub, invitee_email='c2@example.pt')  
        group_signature = msg.GroupServerJoin.sign(settings.PRIVATE_KEY, 'group', inviter_signature=inviter_signature)
        invitation = Invitation.objects.create(group=self.group, invitee=self.user, inviter=self.inviter, signature_inviter=inviter_signature, signature_group=group_signature, secret_code='0000') 
        invitee_signature = self.message_class.sign(self.private_key2, 'user', group_server_signature=invitation.signature_group) 
         
        request = self.message_class.make_request(group_uuid=str(self.group.uuid), user=self.user.key, signature=invitee_signature) 
        raw_response = self.client.post(reverse('group_server_app:confirm_join'),{'data': request.dumps()}) 
        assert raw_response.status_code == 200 
        
class EmailKeyMap(TestCase):
    def setUp(self):   
        self.message_class = msg.EmailKeyMap
        self.private_key, self.key = example_keys.C1_priv, example_keys.C1_pub
        self.group = Group.objects.create(name='test', key=example_keys.G1_pub)
        self.user = User.objects.create(group=self.group, key=self.key, email='c1@example.pt', confirmed=True)
        self.user2 = User.objects.create(group=self.group, key=example_keys.C2_pub, email='c2@example.pt', confirmed=True)
        self.user3 = User.objects.create(group=self.group, key=example_keys.C3_pub, email='c3@example.pt', confirmed=True)
        
    def test_correct_input(self):
        signature = self.message_class.sign(self.private_key, 'user', group_uuid=str(self.group.uuid), request_type='email-key-map')
        request = self.message_class.make_request(group_uuid=str(self.group.uuid), user=self.user.key, request_type='email-key-map', signature=signature)
        raw_response = self.client.post(reverse('group_server_app:email_key_map'),{'data': request.dumps()})
        assert raw_response.status_code == 200
        
        
