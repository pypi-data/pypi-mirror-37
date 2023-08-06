#!/usr/bin/env python3
#******************************************************************************
# Copyright (C) 2018 Thomas "Cakeisalie5" Touhey <thomas@touhey.fr>
# This file is part of the textoutpc project, which is MIT-licensed.
#******************************************************************************

import urllib.parse as _urlparse

from .. import Image as _Image

__all__ = ["GenericImage"]


class GenericImage(_Image):
	""" Get a direct image. Actually this doesn't test anything, we should
		use like the Embed module again, as for videos. """

	# FIXME: make that disappear one day for the OpenWebImage.

	def __init__(self, content):
		url = _urlparse.urlparse(content)
		if url.scheme not in ('http', 'https'):
			raise Exception("No allowed prefix!")

		self.embed = content

# WARNING: This is only for demonstration sake. Do not use without a cache!
# This demonstration class uses the `embed-python` module.
#
#from embed import Embed as _Embed
#
#class OpenWebImage(_Image):
#	""" Decentralized way to gather an image data. """
#
#	def __init__(self, url):
#		u = _urlparse.urlparse(url)
#		if not u.scheme in ('https',):
#			raise Exception
#
#		embed = _Embed(url)
#		embed = embed.embed
#		assert embed['type'] == 'image'
#
#		self.embed = embed['url']

# End of file.
