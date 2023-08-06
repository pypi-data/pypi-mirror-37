#!/usr/bin/env python3
#******************************************************************************
# Copyright (C) 2018 Thomas "Cakeisalie5" Touhey <thomas@touhey.fr>
# This file is part of the textoutpc project, which is MIT-licensed.
#******************************************************************************

from .. import BlockTag as _BlockTag

__all__ = ["AlignTag"]


class AlignTag(_BlockTag):
	""" Main tag for aligning paragraphs.
		Example uses:

		[align=center]This text is centered horizontally.[/align]
		[justify]This text is justified.[/justify]
	"""

	aliases = ('[align]', '[center]', '[centre]', '[left]', '[right]',
		'[justify]')
	superblock = True
	notempty = True

	def prepare(self, name, value):
		_align = {
			'center':  'center',
			'centre':  'center',
			'left':    'left',
			'right':   'right',
			'justify': 'justify'}

		if not name:
			align = None
		elif name == 'align' and value is not None:
			align = _align[value]
		else:
			align = _align[name[1:-1]]

		self._align = align

	def begin_html(self):
		if not self._align:
			return ''

		cl = []
		if self._align:
			cl.append('align-' + self._align)

		return '<div{}>'.format(' class="' + ' '.join(cl) + '"' if cl else '')

	def end_html(self):
		if not self._align:
			return ''
		return '</div>'

# End of file.
