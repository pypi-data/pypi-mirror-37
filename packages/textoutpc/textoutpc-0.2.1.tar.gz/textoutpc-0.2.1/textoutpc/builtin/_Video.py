#!/usr/bin/env python3
#******************************************************************************
# Copyright (C) 2018 Thomas "Cakeisalie5" Touhey <thomas@touhey.fr>
# This file is part of the textoutpc project, which is MIT-licensed.
#******************************************************************************

import urllib.parse as _urlparse
from html import escape as _htmlescape

from .. import BlockTag as _BlockTag

__all__ = ["VideoTag", "YoutubeTag"]

_defaultratio_w = 16
_defaultratio_h = 9


class VideoTag(_BlockTag):
	""" The video tag, puts a preview of the video whose URL is given.
		Only a few 'big' services are supported for now.
		Example uses:

		[video]video_url[/video]
		[video=4:3]video_url[/video]
		[video tiny]video_url[/video tiny]
		[video]https://www.youtube.com/watch?v=yhXpV8hRKxQ[/video]
	"""

	aliases = ('[video]', '[video tiny]')
	raw = True

	def prepare(self, name, value):
		""" Prepare the video tag. """

		_align = {
			'center':       ('center', False),
			'centre':       ('center', False),
			'left':         ('left',   False),
			'right':        ('right',  False),
			'float':        (None,     True),
			'floating':     (None,     True),
			'float-left':   ('left',   True),
			'float-center': ('center', True),
			'float-centre': ('center', True),
			'float-right':  ('right',  True),
		}

		self._sizeclass = "video-tiny" if "tiny" in name \
			else None
		self._align = None
		self._float = False
		self._ratio = None

		for arg in map(str.strip, (value or "").split('|')):
			if   not arg:
				pass
			elif arg[0] in '0123456789:':
				rx, ry = _defaultratio_w, _defaultratio_h
				rn = 0
				rat = arg.split(':')

				try:    rx = int(rat[0]); rn += 1
				except: pass
				try:    ry = int(rat[1]); rn += 1
				except: pass

				if rn:
					self._ratio = round(ry / rx, 4)
			elif arg in _align:
				al, fl = _align[arg]
				if al != None:
					self._align = al
				if fl:
					self._float = True

	def preprocess(self, content):
		try:
			self._video = self.video(content)
		except:
			url = _urlparse.urlparse(content)
			if url.scheme not in ('http', 'https'):
				raise Exception("No allowed prefix!")

			self._video = content

	def content_html(self):
		""" Produce the embed code for the given type. """

		if isinstance(self._video, str):
			url = _htmlescape(self._video)
			return '<p><a href="{}">{}</a></p>'.format(url, url)

		align = "float-" + (self._align or "left") if self._align \
			else self._align

		if self._ratio:
			ratio = self._ratio * 100
		elif hasattr(self._video, 'ratio'):
			ratio = self._video.ratio * 100
		else:
			ratio = round(_defaultratio_h / _defaultratio_w, 4) * 100
		iratio = int(ratio)
		if ratio == iratio:
			ratio = iratio
		ratio = str(ratio)

		code = '<div class="video-wrapper{}{}"{}>' \
			.format(f" {self._sizeclass}" if self._sizeclass else "",
				f' img-{align}' if align else "",
				f' style="padding-bottom: {ratio}%"')

		code += '<iframe src="{}" frameborder="0" allowfullscreen>' \
			'</iframe>'.format(self._video.embed)

		return code + '</div>'

	def content_lightscript(self):
		url = self._url.replace('[', '%5B').replace(']', '%5D')
		return '[[image:{}]]'.format(url)


class YoutubeTag(VideoTag):
	""" Alias for the video tag with only the Youtube possibility.
		Example uses:

		[youtube]okMK1NYRySI[/youtube] """

	aliases = ('[youtube]',)

	def preprocess(self, content):
		super().preprocess(f'https://www.youtube.com/watch?v={content}')

# End of file.
