# -*- coding: utf-8 -*-
""" Setup script of common utilities for Django REST Framework """

from setuptools import setup

setup(
		name="django-commonutil-restframework",
		version="0.1.1",  # REV-CONSTANT:rev 5d022db7d38f580a850cd995e26a6c2f
		description="Common utilities for Django REST Framework",
		py_modules=[
				'django_commonutil_restframework',
		],
		classifiers=[
				'Development Status :: 5 - Production/Stable',
				'Intended Audience :: Developers',
				'License :: OSI Approved :: MIT License',
				'Programming Language :: Python :: 2.7',
				'Framework :: Django :: 1.11',
		],
		license='MIT License',
)

# vim: ts=4 sw=4 ai nowrap
