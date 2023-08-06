#!/usr/bin/env python3
#******************************************************************************
# Copyright (C) 2018 Thomas "Cakeisalie5" Touhey <thomas@touhey.fr>
# This file is part of the textoutpc project, which is MIT-licensed.
#******************************************************************************

from .. import BlockTag as _BlockTag

__all__ = ["SpoilerTag"]


class SpoilerTag(_BlockTag):
	""" Hide content at first glance, force people to click to read content.
		These elements can contain 'secret' elements such as solutions, source
		code, or various other things.
		Example uses:

		[spoiler]This is hidden![/spoiler]
		[spoiler=Y a quelque chose de caché !|Ah, bah en fait non :)]:E
		And it's multiline, [big]and formatted[/big], as usual :D[/spoiler]
	"""

	aliases = ('[spoiler]',)
	superblock = True
	notempty = True
	procvalue = True

	def prepare(self, name, value):
		self._closed = "Cliquez pour découvrir"
		self._open = "Cliquez pour recouvrir"

		if value:
			titles = value.split('|')
			if titles[0]:
				self._closed = titles[0]
			if len(titles) >= 2 and (len(titles) > 2 or titles[1]):
				self._open = '|'.join(titles[1:])

	def begin_html(self):
		return '<div class="spoiler">' \
			'<div class="title on" onclick="toggleSpoiler(this.parentNode, ' \
				'\'open\');"><p>{}</p></div>' \
			'<div class="title off" onclick="toggleSpoiler(this.parentNode, ' \
				'\'close\');"><p>{}</p></div>' \
			'<div class="off">'.format(self._closed, self._open)

	def end_html(self):
		return '</div></div>'

# End of file.
