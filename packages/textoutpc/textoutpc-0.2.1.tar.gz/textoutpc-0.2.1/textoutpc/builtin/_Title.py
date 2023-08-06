#!/usr/bin/env python3
#******************************************************************************
# Copyright (C) 2018 Thomas "Cakeisalie5" Touhey <thomas@touhey.fr>
# This file is part of the textoutpc project, which is MIT-licensed.
#******************************************************************************

from .. import BlockTag as _BlockTag

__all__ = ["TitleTag"]


class TitleTag(_BlockTag):
	""" The title tag.
		Example uses:

		[title]Some title[/title]
		[subtitle]Some subtitle[/subtitle]
	"""

	aliases = ('[title]', '[subtitle]')
	raw = True

	def prepare(self, name, value):
		level = self.tweak("title_level", "1")
		if level[0] == "h":
			level = level[1:]
		level = int(level)
		assert 1 <= level <= 5

		# Name.

		self._level = name[1:-1]

		# HTML tag.

		level += self._level == "subtitle"
		self._tag = f"h{level}"

	def begin_html(self):
		return f'<{self._tag} class="{self._level}">'

	def end_html(self):
		return f'</{self._tag}>'

	def begin_lightscript(self):
		return '#' * ((self._level == "subtitle") + 1) + ' '

# End of file.
