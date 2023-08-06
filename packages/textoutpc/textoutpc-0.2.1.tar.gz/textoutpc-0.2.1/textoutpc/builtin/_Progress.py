#!/usr/bin/env python3
#******************************************************************************
# Copyright (C) 2018 Thomas "Cakeisalie5" Touhey <thomas@touhey.fr>
# This file is part of the textoutpc project, which is MIT-licensed.
#******************************************************************************

from .. import BlockTag as _BlockTag

__all__ = ["ProgressTag"]


class ProgressTag(_BlockTag):
	""" Progress tag, used to display the progress on anything.
		Usage:

		[progress=50]My great progress bar[/progress]
		[progress=100][/progress] """

	aliases = ('[progress]',)
	raw = True

	def prepare(self, name, value):
		self._val = int(value)
		if self._val < 0 or self._val > 100:
			raise Exception("progress value should be between 0 and 100 incl.")

	def begin_html(self):
		return '<div>'

	def end_html(self):
		return '' \
			'<div class="progress">' \
			'<div class="progress-inner" style="width: {}%;">   {}%' \
			'</div></div></div>'.format(self._val, self._val)

# End of file.
