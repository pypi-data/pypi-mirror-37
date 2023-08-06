#!/usr/bin/env python3
#******************************************************************************
# Copyright (C) 2018 Thomas "Cakeisalie5" Touhey <thomas@touhey.fr>
# This file is part of the textoutpc project, which is MIT-licensed.
#******************************************************************************

import re as _re
import urllib.parse as _urlparse

from .. import Video as _Video

__all__ = ["YouTubeVideo", "DailymotionVideo", "VimeoVideo"]


class YouTubeVideo(_Video):
	""" Get a video from Youtube. """

	_hexcode = _re.compile('[a-zA-Z0-9_-]+')

	def __init__(self, url):
		url = _urlparse.urlparse(url)
		if url.scheme not in ('http', 'https'):
			raise Exception

		if   url.netloc == "youtu.be":
			self._id = url.path[1:]
			if not self._hexcode.match(self._id):
				raise ValueError("invalid id")
		elif url.netloc in ('youtube.com', 'www.youtube.com'):
			if url.path != '/watch':
				raise ValueError("invalid id")
			self._id = _urlparse.parse_qs(url.query)['v'][0]
			if not self._hexcode.fullmatch(self._id):
				raise Exception
		else:
			raise ValueError("unknown URL")

		self.embed = f"https://www.youtube.com/embed/{self._id}"


class DailymotionVideo(_Video):
	""" Get a video from Dailymotion. """

	_dailypath = _re.compile('^/video/([a-z0-9]+)$')

	def __init__(self, url):
		url = _urlparse.urlparse(url)
		if url.scheme not in ('http', 'https'):
			raise Exception

		if url.netloc in ('dailymotion.com', 'www.dailymotion.com'):
			self._code = self._dailypath.match(url.path).groups()[0]
		else:
			raise ValueError("unknown URL")

		self.embed = f"https://www.dailymotion.com/embed/video/{self._code}"


class VimeoVideo(_Video):
	""" Get a video from Vimeo. """

	_numcode = _re.compile('^/[0-9]+$')

	def __init__(self, url):
		url = _urlparse.urlparse(url)
		if url.scheme not in ('http', 'https'):
			raise Exception

		if url.netloc in ('vimeo.com', 'www.vimeo.com'):
			self._code = url.path[1:]
			if not self._numcode.match(self._code):
				raise ValueError("invalid video code")
		else:
			raise ValueError("unknown URL")

		self.embed = f"https://player.vimeo.com/video/{self._code}" \
			"?title=0&byline=0&portrait=0"

# WARNING: This is only for demonstration sake. Do not use without a cache!
# This demonstration class uses the `embed-python` module.
#
#from embed import Embed as _Embed
#
#class OpenWebVideo(_Video):
#	""" Decentralized way to gather a video data. """
#
#	def __init__(self, url):
#		u = _urlparse.urlparse(url)
#		if not u.scheme in ('https',):
#			raise Exception
#
#		embed = _Embed(url)
#		embed = embed.embed
#		assert embed['type'] == 'video'
#
#		self.embed = embed['url']
#		if 'ratio' in embed:
#			self.ratio = embed['ratio'] / 100

# End of file.
