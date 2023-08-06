#!/usr/bin/env python3
#******************************************************************************
# Copyright (C) 2018 Thomas "Cakeisalie5" Touhey <thomas@touhey.fr>
# This file is part of the textoutpc project, which is MIT-licensed.
#******************************************************************************

from html import escape as _htmlescape
from .. import BlockTag as _BlockTag

__all__ = ["ShowTag"]


class ShowTag(_BlockTag):
	""" Tag which shows the HTML code that is produced by textout().
		Example uses:

		[show][b]hello world![/show]
	"""

	aliases = ('[show]',)
	notempty = True
	superblock = True
	inlined = True
	generic = False
	raw = False

	def preprocess_html(self, content):
		return _htmlescape(content)

	def begin_html(self):
		return '<span class="inline-code">'

	def end_html(self):
		return '</span>'

# End of file.
