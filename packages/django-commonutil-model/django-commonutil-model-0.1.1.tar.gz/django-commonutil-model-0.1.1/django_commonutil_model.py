# -*- coding: utf-8 -*-
"""
Utilities for Django Model and Model Field
"""

from __future__ import unicode_literals

from django.db.models.fields.related import RelatedField, ForeignKey


def _make_default_kwd_method(orig_method, k, v):
	""" (internal)
	"""

	def f(self, *args, **kwds):
		kwds.setdefault(k, v)
		return orig_method(self, *args, **kwds)

	return f


def _make_default_kwd_modelfield_deconstruct(orig_deconstruct, k, v):
	""" (internal)
	"""

	def f(self, *args, **kwds):
		name, path, dargs, dkwds, = orig_deconstruct(self, *args, **kwds)
		if not (dkwds.get(k) is v):
			del dkwds[k]
		return name, path, dargs, dkwds

	return f


def attach_default_help_text_for_modelfield(help_text):
	"""
	Decorator to attach default help text for model field

	Args:
		help_text - Help text
	"""

	def f(cls):
		cls.__init__ = _make_default_kwd_method(cls.__init__, "help_text", help_text)
		cls.deconstruct = _make_default_kwd_modelfield_deconstruct(cls.deconstruct, "help_text", help_text)
		return cls

	return f


def fetch_model_field_contents(model_cls, instance, include_none=False):
	"""
	Fetch contents from model instance.

	Args:
		model_cls - Model class for given instance to fetch from.
		instance - Model instance to fetch content from.
		include_none=False - Include None field or not

	Return:
		Tuple of (values, relations) which contains fetched values and relations in dictionaries.
	"""
	result_value = {}
	result_relation = {}
	for f in model_cls._meta.get_fields():
		n = f.name
		d = getattr(instance, n)
		if (d is None) and (include_none is False):
			continue
		if isinstance(f, RelatedField) and (not isinstance(f, ForeignKey)):
			result_relation[n] = tuple(d.all())
		else:
			result_value[n] = d
	return (result_value, result_relation)


def duplicate_model_relation_contents(instance, relation_contents):
	"""
	Apply relations to given model instance

	Args:
		instance - Model instance to apply relations
		relation_contents - Content of relationships
	"""
	for name, relations in relation_contents.iteritems():
		rel = getattr(instance, name)
		if rel is None:
			continue
		rel.set(relations)
