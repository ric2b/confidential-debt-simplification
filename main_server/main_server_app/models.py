from django.db import models
import uuid

description_length = 80
key_length = 400  # 2048 bit key in base 64? I don't know what I'm doing :) 
# Create your models here.


class Group(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=80)

    owner = models.CharField(max_length=key_length)
    #owner_email = models.EmailField(max_length=254)
    

class User(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    # the uuid is the signing key of the user!
    user_id = models.CharField(primary_key=True, max_length=key_length)
    encryption_key = models.CharField(max_length=key_length)

    # if the user, after simplification, is a borrower
    is_net_borrower = models.NullBooleanField(default=None)

class UOMe(models.Model):
    class Meta:
        verbose_name_plural = "UOMe's"  # for the Django Admin panel

    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)    

    borrower = models.ForeignKey(User, on_delete=models.PROTECT, related_name='uome_borrower')
    lender = models.ForeignKey(User, on_delete=models.PROTECT, related_name='uome_lender')
    value = models.PositiveIntegerField()  # In cents!
    
    description = models.CharField(max_length=description_length)
    issuing_date = models.DateField('date issued', auto_now_add=True)

    confirmed = models.BooleanField(default=False)

    def __str__(self):
        string_representation = "%i€ from %s to %s: %s"
        return string_representation % self.value*100, self.borrower, self.lender


class UserDebt(models.Model):
    # the debt between users after simplification
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    borrower = models.ForeignKey(User, on_delete=models.PROTECT, related_name='debt_borrower')
    lender = models.ForeignKey(User, on_delete=models.PROTECT, related_name='debt_lender')

    value = models.PositiveIntegerField()  # In cents!




