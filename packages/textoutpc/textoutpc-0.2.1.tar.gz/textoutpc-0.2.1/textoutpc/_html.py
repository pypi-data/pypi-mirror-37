#!/usr/bin/env python3
#******************************************************************************
# Copyright (C) 2018 Thomas "Cakeisalie5" Touhey <thomas@touhey.fr>
# This file is part of the textoutpc project, which is MIT-licensed.
#******************************************************************************
""" Utilities for HTML conversions. """

import regex as _re
from html import escape

__all__ = ["escape", "urls", "SmileyConvertor"]

# ---
# Smileys.
# ---

class SmileyConvertor:
	""" Smileys convertor. """

	def __init__(self, smileys = {}):
		self._html = {escape(a): b.url \
			for a, b in smileys.items() if b.url != None}
		self._re = _re.compile('(^|\\s)(' + '|'.join(map(_re.escape,
			self._html.keys())) + ')(\\s|$)')

	def convert(self, text):
		cv = ""

		while text:
			try:
				m = next(self._re.finditer(text))
			except StopIteration:
				break

			cv += text[:m.start()] + m.group(1)
			cv += '<img src="' + self._html[m.group(2)] + '">'
			text = m.group(3) + text[m.end():]

		return cv + text

# ---
# URLs.
# ---

_urlreg = _re.compile("""\
	(?P<sp>^|\s|[[:punct:]])
	(?P<url>(https?|ftp):
		(?P<ucore>[^\[\]\(\)\s]* (\[(?&ucore)\]?)* (\((?&ucore)\)?)*)*
	)
""", _re.VERBOSE | _re.M)

def urls(text):
	""" Convert URLs. """

	def _sub_html(m):
		sp = m.group('sp')
		url = m.group('url')
		aft = ''

		# Hack for the last comma.
		if url[-1] == ',':
			url, aft = url[:-1], ','

		text = '{}<a href="{}">{}</a>{}' \
			.format(sp, url, url, aft)
		return text

	return _urlreg.sub(_sub_html, text)

# End of file.
