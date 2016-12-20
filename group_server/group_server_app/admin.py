from django.contrib import admin
from .models import Group, User, Invitation, ConfirmedInvitation



# Register your models here.

admin.site.register(Group)
admin.site.register(User)
admin.site.register(Invitation)
admin.site.register(ConfirmedInvitation)
