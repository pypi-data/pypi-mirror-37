#!/usr/bin/env python3
#******************************************************************************
# Copyright (C) 2018 Thomas "Cakeisalie5" Touhey <thomas@touhey.fr>
# This file is part of the textoutpc project, which is MIT-licensed.
#******************************************************************************

from .. import InlineTag as _InlineTag
from ..color import get_color as _get_color

__all__ = ["TextTag"]

# ---
# Data.
# ---

_big_size = 2.00
_sml_size = 0.75

_fonts = {
	"arial": "Arial",
	"comic": "Comic MS",
	"tahoma": "Tahoma",
	"courier": "Courier",
	"haettenschweiler": "Haettenschweiler",
	"mono": "monospace",
	"monospace": "monospace"
}

# ---
# Tag definition.
# ---


class TextTag(_InlineTag):
	""" Main tag for setting text formatting.
		Example uses:

		[b]Bold text.[/b]
		[i]Italic text.[/i]
		[u]Underlined text.[/u]
		[strike]Striked text.[/strike]
		[striked]Text strikes again.[/striked]
		[font=arial]Arial text.[/font]
		[arial]Arial text again.[/arial]
		[blue]This will be in blue[/blue]
		[color=blue]This as well[/color]
		[color=rgb(255, 255, 255, 0.4)]BLACKNESS[/color]
		[color=hsl(0, 100%, 0.5)]This will be red.[/color]

		Also supports a hack used on Planète Casio for a while, which
		is a CSS injection, e.g.:

		[color=brown; size: 16pt]Hello world![/color]
	"""

	aliases = ('[css]', '[b]', '[i]', '[u]', '[o]', '[s]', '[strike]',
		'[monospace]', '[mono]', '[font]', '[color]', '[c]',
		'[size]', '[big]', '[small]',
		'[arial]', '[comic]', '[tahoma]', '[courier]',
		'[haettenschweiler]', '[red]', '[green]', '[blue]',
		'[yellow]', '[maroon]', '[purple]', '[gray]',
		'[grey]', '[brown]')
	notempty = True

	def prepare(self, name, value):
		self._bold = False
		self._italic = False
		self._underline = False
		self._overline = False
		self._strike = False
		self._font = None
		self._color = None
		self._bgcolor = None
		self._size = None

		# Récupérer la partie correspondant à l'injection CSS s'il y
		# en a une.

		def get_props(value):
			props = ''
			if value is not None:
				index = value.find(';')
				if index >= 0:
					props = value[index + 1:]
					value = value[:index]
			return value, props

		# Définir les propriétés à partir du truc principal.

		name = name[1:-1]
		props = ""
		if   name == "css":
			props = value
		elif name == "b":
			self._bold = True
		elif name == "i":
			self._italic = True
		elif name == "u":
			self._underline = True
		elif name == "o":
			self._overline = True
		elif name in ("s", "strike", "striked"):
			self._strike = True
		elif name in ("color", 'c'):
			value, props = get_props(value)
			self._color = _get_color(value)
		elif name == 'f':
			value, props = get_props(value)
			self._bgcolor = _get_color(value)
		elif name == "font":
			value, props = get_props(value)
			assert value in _fonts
			self._font = _fonts[value]
		elif name in ('size', 'big', 'small'):
			if name != 'size':
				value = name
			if value == 'big':
				self._size = _big_size
			elif value == 'small':
				self._size = _sml_size
			else:
				self._size = round(int(value) / 100.0, 2)
				assert 0 < self._size <= 3.0

			if self._size == 1.0:
				self._size = None
		elif name in _fonts:
			self._font = name
		else:
			self._color = _get_color(name)

		# Gestion des propriétés CSS (par injection ou via `[css]`).

		for prop in props.split(';'):
			prop = prop.strip()
			if not prop:
				continue

			name, *value = prop.split(':')
			if not value:
				continue
			name = name.strip()
			value = ':'.join(value).strip()

			if name in ('size', 'font-size'):
				# Control the font size.

				unit = 'pt'
				if   value.endswith('pt'):
					value = value[:-2].rstrip()
				elif value.endswith('em'):
					unit = 'em'
					value = value[:-2].rstrip()

				if not value or \
					any(c != '0' for c in value[:-3]) or \
					any(c not in '0123456789' for c in value[-3:]):
					continue

				value = int(value[-3:])
				if unit == 'pt':
					value /= 12 # XXX: default em size

				if 0 < value <= 3.0:
					self._size = value
			elif name == 'color':
				# Control the text color.

				self._color = _get_color(value)
			elif name == 'background-color':
				# Control the background color.

				self._bgcolor = _get_color(value)

	def _get_css(self):
		""" Get the `style` CSS classes and properties for HTML output. """

		classes, props = [], []

		if not self.tweak('obsolete_tags', True):
			if self._bold:
				props.append('font-weight: bold')
			if self._italic:
				props.append('font-style: italic')
			if self._underline or self._strike or self._overline:
				props.append('text-decoration:{}{}{}'.format(' underline'
					if self._underline else '', ' line-through'
					if self._strike else '', ' overline'
					if self._overline else ''))
		else:
			if self._overline:
				props.append('text-decoration:{}'.format(' overline'
					if self._overline else ''))

		if self._font:
			props.append('font-family: ' + self._font)

		if self._color:
			# `transparent` is at least considered as a special value,
			# or at most as an alias to `rgba(0,0,0,0)`.

			if self._color[3] == 0.0:
				props.append('color: transparent')
			else:
				# always append the #rgb color: it will be read by older
				# browsers if the `rgba()` function isn't supported.

				props.append('color: #%02X%02X%02X' % self._color[0:3])
				if self._color[3] < 1.0:
					props.append('color: rgba({}, {}, {}, {})'
						.format(*self._color))

		if self._bgcolor and self._bgcolor[3] != 0.0:
			props.append('background-color: #%02X%02X%02X' % self._color[0:3])
			if self._bgcolor[3] < 1.0:
				props.append('background-color: rgba({}, {}, {}, {})'
					.format(*self._bgcolor))

		if self._size:
			props.append('font-size: {}em'.format(self._size))

		return classes, props

	def begin_html(self):
		obsoletetags = self.tweak('obsolete_tags', True)

		cls, props = self._get_css()
		if cls or props:
			props = '<span{}{}>'.format(' class="{}"'.format(' '.join(cls))
				if cls else '', ' style="{}"'.format('; '.join(props))
				if props else '')
		else:
			props = ''

		return '' \
			+ ('', '<b>')[obsoletetags and self._bold] \
			+ ('', '<i>')[obsoletetags and self._italic] \
			+ ('', '<u>')[obsoletetags and self._underline] \
			+ ('', '<strike>')[obsoletetags and self._strike] \
			+ props

	def end_html(self):
		obsoletetags = self.tweak('obsolete_tags', True)

		return '' \
			+ ('', '</span>')[any(self._get_css())] \
			+ ('', '</strike>')[obsoletetags and self._strike] \
			+ ('', '</u>')[obsoletetags and self._underline] \
			+ ('', '</i>')[obsoletetags and self._italic] \
			+ ('', '</b>')[obsoletetags and self._bold]

# End of file.
