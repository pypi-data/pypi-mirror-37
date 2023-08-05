# -*- coding: utf-8 -*-
""" Setup script of LDAP authentication backend for Django """

from setuptools import setup

setup(
		name="django-ldap-auth-backend",
		version="0.1.6",  # REV-CONSTANT:rev 5d022db7d38f580a850cd995e26a6c2f
		description="LDAP authentication backend for Django",
		packages=[
				"ldapauthbackend",
				"ldapauthbackend.migrations",
		],
		include_package_data=True,
		install_requires=[
				"python-ldap >= 3.1.0, < 4.0.0",
				"django-angular-host-page-template-backend >= 0.1.0, < 2.0.0",
		])

# vim: ts=4 sw=4 ai nowrap
