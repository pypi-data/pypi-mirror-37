# -*- coding: utf-8 -*-
"""
Utilities for Django REST Framework
"""

from __future__ import unicode_literals


def _make_targeted_get_serializer(serializer_cls, instance_cls):
	def get_serializer(self, instance=None, *args, **kwds):  # pylint: disable=unused-argument
		if (instance is None) or isinstance(instance, instance_cls):
			return serializer_cls(instance=instance, *args, **kwds)
		return serializer_cls(instance=None, *args, **kwds)

	return get_serializer


def attach_targeted_get_serializer(serializer_cls, instance_cls):
	"""
	Decorator for attaching serializer and data instance class to DRF APIView.

	Args:
		serializer_cls - Class object for serializer
		instance_cls - Class object for data instance
	"""

	def f(cls):
		cls.get_serializer = _make_targeted_get_serializer(serializer_cls, instance_cls)
		return cls

	return f
