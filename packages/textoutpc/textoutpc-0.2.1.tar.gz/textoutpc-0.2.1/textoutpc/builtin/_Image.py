#!/usr/bin/env python3
#******************************************************************************
# Copyright (C) 2018 Thomas "Cakeisalie5" Touhey <thomas@touhey.fr>
# This file is part of the textoutpc project, which is MIT-licensed.
#******************************************************************************

import urllib.parse as _urlparse

from .. import BlockTag as _BlockTag
from html import escape as _htmlescape

__all__ = ["ImageTag", "AdminImageTag"]


class ImageTag(_BlockTag):
	""" The main tag for displaying an image.
		Example uses:

		[img]picture_url[/img]
		[img=center]picture_url[/img]
		[img=12x24]picture_url[/img]
		[img=center|12x24]picture_url[/img]
		[img=x24|right]picture_url[/img]
	"""

	aliases = ('[img]',)
	raw = True

	def prepare(self, name, value):
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

		self._width = None
		self._height = None
		self._align = None
		self._float = False

		for arg in ("", value)[value is not None].split('|'):
			if   not arg:
				pass
			elif arg[0] in '0123456789x':
				self._width = None
				self._height = None

				dim = arg.split('x')
				try:
					self._width = int(dim[0])
				except ValueError:
					pass
				try:
					self._height = int(dim[1])
				except ValueError:
					pass
			elif arg in _align:
				al, fl = _align[arg]
				if al is not None:
					self._align = al
				if fl:
					self._float = True

	def preprocess(self, content):
		try:
			self._image = self.image(content)
		except:
			url = _urlparse.urlparse(content)
			if url.scheme not in ('http', 'https'):
				raise Exception("No allowed prefix!")

			self._image = content

	def content_html(self):
		if isinstance(self._image, str):
			url = _htmlescape(self._image)
			return '<p><a href="{}">{}</a></p>'.format(url, url)

		style = []
		cls = []
		if   self._width:
			style.append('width: {}px'.format(self._width))
		elif self._height:
			style.append('width: auto')
		if   self._height:
			style.append('height: {}px'.format(self._height))
		elif self._width:
			style.append('height: auto')
		if   self._float:
			cls.append('img-float-{}'.format(self._align or 'right'))
		elif self._align:
			cls.append('img-{}'.format(self._align))

		return '<img src="{}"{}{} />'.format(_htmlescape(self._image.embed),
			' class="{}"'.format(' '.join(cls)) if cls else '',
			' style="{}"'.format('; '.join(style)) if style else '')

	def content_lightscript(self):
		url = self._image.embed.replace('[', '%5B').replace(']', '%5D')
		return '[[image:{}]]'.format(url)


class AdminImageTag(ImageTag):
	""" This tag is special for Planète Casio, as it takes images from
		the `ad`ministration's image folder.
		It just adds this folder's prefix.
		Example uses:

		[adimg]some_picture.png[/img]
		[adimg=center]some_picture.png[/img]
		[adimg=12x24]some_picture.png[/img]
		[adimg=center|12x24]some_picture.png[/img]
		[adimg=x24|right]some_picture.png[/img]
	"""

	aliases = ('[adimg]',)

	def preprocess(self, content):
		self._url = 'https://www.planet-casio.com/images/ad/' + content
		self._checkurl()

# End of file.
