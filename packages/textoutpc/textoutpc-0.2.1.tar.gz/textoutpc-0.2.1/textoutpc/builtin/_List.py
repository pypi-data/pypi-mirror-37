#!/usr/bin/env python3
#******************************************************************************
# Copyright (C) 2018 Thomas "Cakeisalie5" Touhey <thomas@touhey.fr>
# This file is part of the textoutpc project, which is MIT-licensed.
#******************************************************************************

from .. import BlockTag as _BlockTag

__all__ = ["ListTag", "ListElementTag"]


# Bullet style names.

_ol_list_style_types = {
	'disc':   'disc',
	'circle': 'circle',
	'square': 'square',
}
_ul_list_style_types = {
	'1':      'decimal',
	'a':      'lower-alpha',
	'A':      'upper-alpha',
	'i':      'lower-roman',
	'I':      'upper-roman',
}

_list_style_types = _ol_list_style_types.copy()
_list_style_types.update(_ul_list_style_types)

_ul_lst_names = set(_ul_list_style_types.keys())
_ol_lst_names = set(_ol_list_style_types.keys())

# Tag definitions.

class ListElementTag(_BlockTag):
	""" List element for basic lists (see `ListTag`). """

	aliases = ('[*]', '[li]')
	notempty = True
	superblock = True
	not_within_itself = True

	def begin_html(self):
		return '<li>'

	def end_html(self):
		return '</li>'

class ListTag(_BlockTag):
	""" Main tag for making basic lists.
		Example use:

		[ul]
		[*] Item number one.
		[*] Item number [b]two[/b].
		[/ul]
	"""

	aliases = ('[list]', '[ul]', '[ol]')
	notempty = True
	superblock = True
	allowed_tags = (_ListElement,)
	only_allowed_tags = True

	def prepare(self, name, value):
		us = _ul_lst_names
		os = _ol_lst_names

		if   name == '[list]' and value == None:
			self._tag = 'ul'
			self._style = None
		elif name == '[list]' and value in us:
			self._tag = 'ul'
			self._style = value
		elif name == '[list]' and value in os:
			self._tag = 'ol'
			self._style = value
		elif name == '[ul]'   and value == None:
			self._tag = 'ul'
			self._style = None
		elif name == '[ul]'   and value in us:
			self._tag = 'ul'
			self._style = value
		elif name == '[ol]'   and value == None:
			self._tag = 'ol'
			self._style = None
		elif name == '[ol]'   and value in os:
			self._tag = 'ol'
			self._style = value
		else:
			raise ValueError("invalid bullet style")

		# Find out the HTML style name.

		if self._style != None:
			self._style = _list_style_types[self._style]

	def begin_html(self):
		tag = f'<{self._tag}'
		if self._style != None:
			tag += f' style="list-style-type: {self._style}"'
		tag += '>'

		return tag

	def end_html(self):
		return '</ul>'

# End of file.
