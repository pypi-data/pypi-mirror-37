# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist

from ldapauthbackend.backend import Connection, sanitize_username
from ldapauthbackend.models import LDAPUserProfile


def fetch_existed_user_dn():
	user_dn = {}
	dn_collection = set()
	for u in get_user_model().objects.all():
		try:
			if u.ldapuserprofile.dn:
				user_dn[u.username] = u.ldapuserprofile.dn
				dn_collection.add(u.ldapuserprofile.dn)
				continue
		except ObjectDoesNotExist:
			pass
		user_dn[u.username] = None
	return (user_dn, dn_collection)


def fetch_nonexist_candidate_members():
	conn = Connection.build_via_configuration()
	candidate_uids = conn.fetch_candidate_member_uids()
	existed_user, existed_dn = fetch_existed_user_dn()
	for n in existed_user.iterkeys():
		candidate_uids.discard(n)
	result = {}
	for u in candidate_uids:
		dn = conn.get_account_dn(u)
		if (not dn) or (dn in existed_dn):
			continue
		result[u] = dn
	return result


def import_candidate_member(user_name, user_dn, assoc_staff_user):
	user_name = sanitize_username(user_name)
	try:
		u = get_user_model().objects.get(username=user_name)
		raise ValueError("duplicated user: %r (given user-name=%r)" % (u, user_name))
	except ObjectDoesNotExist:
		pass
	conn = Connection.build_via_configuration()
	profile = conn.fetch_user_profile(user_dn)
	u = get_user_model().objects.create_user(user_name)
	ldap_profile = LDAPUserProfile(user=u, dn=user_dn, account_uid=profile.account_uid, account_name=profile.account_name, import_staff=assoc_staff_user)
	ldap_profile.save()
	return u


def sync_user_ldap_profile(user):
	conn = Connection.build_via_configuration()
	profile = conn.fetch_user_profile(user.ldapuserprofile.dn)
	user.ldapuserprofile.account_uid = profile.account_uid
	user.ldapuserprofile.account_name = profile.account_name
	user.save()
	return user
