# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from json import loads as json_loads

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import JsonResponse
from django.views.generic.base import View
from django.shortcuts import render

from ldapauthbackend.operations import fetch_nonexist_candidate_members
from ldapauthbackend.operations import import_candidate_member
from ldapauthbackend.operations import sync_user_ldap_profile


@staff_member_required
def index(request):  # pylint: disable=unused-argument
	return render(request, "ldapauthbackend/index.html")


class AccessCheckMixin(UserPassesTestMixin):
	raise_exception = True
	permission_required = None

	def test_func(self):
		u = self.request.user
		if not (u.is_active and u.is_staff):
			return False
		if self.permission_required:
			return u.has_perms(self.permission_required)
		return True


class CandidateMembers(AccessCheckMixin, View):
	def get(self, request, *args, **kwds):  # pylint: disable=unused-argument
		candidate_member_dn = fetch_nonexist_candidate_members()
		d = [{"username": u, "dn": d} for u, d in candidate_member_dn.iteritems()]
		d.sort(key=lambda x: x.get("username", None))
		result = {"candidates": d, "access_via": request.user.username}
		return JsonResponse(result)


class ImportMember(AccessCheckMixin, View):
	permission_required = ('auth.add_user', )

	def post(self, request, *args, **kwds):  # pylint: disable=unused-argument
		cmap = json_loads(request.body)
		username = cmap["username"]
		memberdn = cmap["memberdn"]
		u = import_candidate_member(username, memberdn, request.user)
		result = {
				"username": u.username,
		}
		return JsonResponse(result)


class SyncProfile(AccessCheckMixin, View):
	permission_required = ('auth.add_user', )

	def post(self, request, *args, **kwds):  # pylint: disable=unused-argument
		cmap = json_loads(request.body)
		username = cmap["username"]
		u = get_user_model().objects.get(username=username)
		u = sync_user_ldap_profile(u)
		result = {
				"username": u.username,
				"account_uid": u.ldapuserprofile.account_uid,
				"account_name": u.ldapuserprofile.account_name,
		}
		return JsonResponse(result)
