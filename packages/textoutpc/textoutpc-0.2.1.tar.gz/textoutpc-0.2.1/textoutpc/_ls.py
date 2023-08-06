#!/usr/bin/env python3
#******************************************************************************
# Copyright (C) 2018 Thomas "Cakeisalie5" Touhey <thomas@touhey.fr>
# This file is part of the textoutpc project, which is MIT-licensed.
#******************************************************************************
""" Utilities for Lightscript conversions. """

import regex as _re

__all__ = ["urls"]

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

	def _sub_ls(m):
		sp = m.group('sp')
		url = m.group('url')
		aft = ''

		# Hack for the last comma.
		if url[-1] == ',':
			url, aft = url[:-1], ','

		url = url.replace('<', '%3C')
		url = url.replace('>', '%3E')
		text = '{}<{}>{}'.format(sp, url, aft)
		return text

	return _regurl.sub(_sub_ls, text)

# End of file.
