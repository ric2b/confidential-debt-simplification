from django.contrib import admin
from .models import Group, User, Invitation



# Register your models here.

admin.site.register(Group)
admin.site.register(User)
admin.site.register(Invitation)

