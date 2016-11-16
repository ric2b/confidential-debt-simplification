from django.contrib import admin

# Register your models here.
from .models import Group, User, UOMe, UserDebt

class UserInLine(admin.TabularInline):
    model = User
    extra = 1


class GroupAdmin(admin.ModelAdmin):
    inlines = [UserInLine]
    search_fields = ['name']


admin.site.register(Group, GroupAdmin)
admin.site.register(User)
admin.site.register(UOMe)
admin.site.register(UserDebt)
