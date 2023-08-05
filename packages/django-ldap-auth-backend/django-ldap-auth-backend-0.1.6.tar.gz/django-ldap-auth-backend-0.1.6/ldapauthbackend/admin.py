# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from ldapauthbackend.models import LDAPUserProfile


class LDAPUserProfileInline(admin.StackedInline):
	model = LDAPUserProfile
	can_delete = False
	fk_name = 'user'
	verbose_name_plural = 'ldapuserprofile'


class UserAdmin(BaseUserAdmin):
	inlines = (LDAPUserProfileInline, )


# Re-register management classes

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
