from django.contrib import admin

# Register your models here.
from .models import Group, User, UOMe, UserDebt


class UserInLine(admin.TabularInline):
    model = User
    extra = 1


class GroupAdmin(admin.ModelAdmin):
    list_display = ['uuid', 'name', 'key']
    inlines = [UserInLine]
    search_fields = ['name']


class UOMeAdmin(admin.ModelAdmin):
    list_display = ['group', 'uuid', 'lender', 'borrower', 'value', 'description']


admin.site.register(Group, GroupAdmin)
admin.site.register(User)
admin.site.register(UOMe, UOMeAdmin)
admin.site.register(UserDebt)
