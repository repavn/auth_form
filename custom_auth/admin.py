from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from custom_auth.models import UserInfo


class UserInfoInline(admin.TabularInline):
    model = UserInfo


class CustomUserAdmin(UserAdmin):
    inlines = [UserInfoInline]

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
