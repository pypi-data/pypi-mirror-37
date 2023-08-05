# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from collections import namedtuple
from string import ascii_letters
from string import digits as ascii_digits
from json import load as json_load
import logging

from django.utils.encoding import force_text
from django.contrib.auth import get_user_model
from django.conf import settings as django_settings

import ldap

_log = logging.getLogger(__name__)

_mod = None
_cfg = None


class LDAPAuthBackendConfig(object):
	def __init__(self, urls, account_base_dn, candidate_group_dn, *args, **kwds):
		super(LDAPAuthBackendConfig, self).__init__(*args, **kwds)
		self.urls = urls
		self.account_base_dn = account_base_dn
		self.candidate_group_dn = candidate_group_dn

	@classmethod
	def load_configuration(cls):
		cfg_path = getattr(django_settings, "LDAP_AUTH_CONFIG_FILE")
		with open(cfg_path, "r") as fp:
			cmap = json_load(fp)
		urls = tuple(cmap["urls"])
		account_base_dn = tuple(cmap["account_base_dn"])
		candidate_group_dn = tuple(cmap["candidate_group_dn"])
		return cls(urls, account_base_dn, candidate_group_dn)


def get_config():
	# type: () -> LDAPAuthBackendConfig
	global _cfg
	if _cfg is None:
		_cfg = LDAPAuthBackendConfig.load_configuration()
	return _cfg


def get_module():
	# type: () -> ldap
	global _mod
	if _mod is None:
		mod_opt = getattr(django_settings, "LDAP_AUTH_MODULE_OPTIONS", None)
		if mod_opt:
			for opt_k, opt_v in mod_opt.iteritems():
				ldap.set_option(opt_k, opt_v)
		_mod = ldap
	return _mod


USERNAME_ACCEPT_CHAR = ascii_letters + ascii_digits + "_-."

UserProfile = namedtuple("UserProfile", ("dn", "account_uid", "account_name"))


def sanitize_username(n):
	return "".join([ch if (ch in USERNAME_ACCEPT_CHAR) else "_" for ch in n])


class ConnectError(Exception):
	def __init__(self, urls, *args, **kwds):
		super(ConnectError, self).__init__(*args, **kwds)
		self.urls = urls

	def __repr__(self):
		return "ConnectError(%r)" % (self.urls, )


_EMPTY_ITERABLE = ()


class Connection(object):
	def __init__(self, cfg, *args, **kwds):
		super(Connection, self).__init__(*args, **kwds)
		self.urls = cfg.urls
		self.account_base_dn = cfg.account_base_dn
		self.candidate_group_dn = cfg.candidate_group_dn
		self._link = None

	@classmethod
	def build_via_configuration(cls):
		# type: () -> Connection
		cfg = get_config()
		return cls(cfg)

	def _get_link(self):
		if self._link:
			yield self._link
		m_ldap = get_module()
		for u in self.urls:
			self._link = None
			l = m_ldap.initialize(u, bytes_mode=False)
			self._link = l
			yield l

	def _invoke(self, n, *args, **kwds):
		for lnk in self._get_link():
			c = getattr(lnk, n)
			try:
				r = c(*args, **kwds)
				return r
			except Exception:
				pass
		raise ConnectError(self.urls)

	def simple_bind(self, who, cred):
		return self._invoke("simple_bind_s", who, cred)

	def search(self, base, scope, filterstr='(objectClass=*)', attrlist=None, attrsonly=0, timeout=10):
		r = self._invoke("search_st", base, scope, filterstr, attrlist, attrsonly, timeout)
		if r:
			return r
		return _EMPTY_ITERABLE

	def user_authenticate(self, user_dn, password):
		try:
			self.simple_bind(user_dn, password)
			return True
		except Exception:
			_log.exception("failed on authorize user %r", user_dn)
		return False

	def get_account_dn(self, username):
		username = sanitize_username(username)
		filterstr = '(&(objectClass=account)(uid=' + username + '))'
		for base_dn in self.account_base_dn:
			r = self.search(base_dn, ldap.SCOPE_SUBTREE, filterstr, ('uid', ), 1)
			for dn, _entry in r:
				return dn

	def fetch_candidate_member_uids(self):
		result = set()
		for base_dn in self.candidate_group_dn:
			r = self.search(base_dn, ldap.SCOPE_SUBTREE, '(objectClass=posixGroup)', ('memberUid', ))
			for _dn, entry in r:
				l = entry.get('memberUid', None)
				if not l:
					continue
				result.update(l)
		return result

	def fetch_user_profile(self, user_dn):
		result = None
		r = self.search(user_dn, ldap.SCOPE_BASE, attrlist=('uid', 'uidNumber'))
		for dn, entry in r:
			user_name = entry['uid'][0]
			user_id = int(entry['uidNumber'][0])
			result = UserProfile(dn, user_id, user_name)
		if not result:
			raise KeyError("User DN not found: %r" % (user_dn, ))
		return result


UserModel = get_user_model()


class LDAPAuthBackend(object):
	def _can_authenticate(self, u):
		is_active = getattr(u, 'is_active', True)
		return is_active

	def _get_user_dn(self, username):
		if not username:
			raise ValueError('username must not empty')
		u = UserModel.objects.get(username=username)
		if not self._can_authenticate(u):
			raise ValueError('given user cannot authenticate')
		return (u, u.ldapuserprofile.dn)

	def authenticate(self, request, username=None, password=None):  # pylint: disable=unused-argument
		try:
			user_obj, user_dn = self._get_user_dn(username)
		except Exception:
			_log.exception("failed on get DN for user %r", username)
			return None
		if (not user_dn) or (not password):
			_log.error("empty user DN or not given password")
			return None
		conn = Connection.build_via_configuration()
		if conn.user_authenticate(force_text(user_dn), force_text(password)):
			return user_obj
		return None

	def get_user(self, user_id):
		try:
			return UserModel.objects.get(pk=user_id)
		except UserModel.DoesNotExist:
			pass
		return None
