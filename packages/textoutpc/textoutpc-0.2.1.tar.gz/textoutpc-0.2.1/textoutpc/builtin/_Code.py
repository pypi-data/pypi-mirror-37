#!/usr/bin/env python3
#******************************************************************************
# Copyright (C) 2018 Thomas "Cakeisalie5" Touhey <thomas@touhey.fr>
# This file is part of the textoutpc project, which is MIT-licensed.
#******************************************************************************

from .. import BlockTag as _BlockTag, InlineTag as _InlineTag

__all__ = ["CodeTag", "InlineCodeTag", "NoEvalTag"]


class CodeTag(_BlockTag):
	""" The basic code tag, for displaying code.
		Example uses:

		[code]int main()
		{
			printf("hello, world");
		}[/code] """

	aliases = ('[code]',)
	generic = False
	raw = True
	notempty = True

	def begin_html(self):
		return '<div class="code">'

	def end_html(self):
		return '</div>'

	def begin_lightscript(self):
		return '```\n'

	def end_lightscript(self):
		return '```\n'


class InlineCodeTag(_InlineTag):
	""" Inline code tag, doesn't display a box, simply doesn't evaluate
		the content and uses monospace font.
		Example uses:

		`some inline code`
		[inlinecode][b]The tags will be shown verbatim.[/b][/inlinecode]
		[inlinecode][inlinecode][i]This also[/inlinecode] works![/inlinecode]
	"""

	aliases = ('`', '[inlinecode]')
	generic = False
	raw = True

	def begin_html(self):
		return '<span class="inline-code">'

	def end_html(self):
		return '</span>'

	def begin_lightscript(self):
		return '`'

	def end_lightscript(self):
		return '`'


class NoEvalTag(_InlineTag):
	""" Inline code tag, simply doesn't evaluate the content.
		Example uses:

		[noeval][b]wow, and no need for monospace![/b][/noeval]
	"""

	aliases = ('[noeval]', '[nobbcode]')
	generic = False
	raw = True

# End of file.
