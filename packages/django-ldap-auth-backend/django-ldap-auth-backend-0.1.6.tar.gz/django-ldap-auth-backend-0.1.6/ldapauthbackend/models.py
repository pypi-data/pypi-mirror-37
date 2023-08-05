# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import models


class LDAPUserProfile(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	dn = models.CharField(max_length=255)
	account_uid = models.BigIntegerField(default=-1)
	account_name = models.CharField(max_length=127)
	import_staff = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="+", editable=False)

	def __unicode__(self):
		return "LDAPUserProfile(user=%r, dn=%s, account_uid=%d, account_name=%r, import_staff=%r)" % (
				self.user,
				self.dn,
				self.account_uid,
				self.account_name,
				self.import_staff,
		)
