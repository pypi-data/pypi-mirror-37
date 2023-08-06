#!/usr/bin/env python3
#******************************************************************************
# Copyright (C) 2018 Thomas "Cakeisalie5" Touhey <thomas@touhey.fr>
# This file is part of the textoutpc project, which is MIT-licensed.
#******************************************************************************
""" Layer on top of the character stream.

	See the `TextoutStream` class description for more information.
"""

import io as _io
import regex as _re

__all__ = ["TextoutStream", "TextoutUnit"]

# ---
# Class definitions.
# ---

class TextoutUnit:
	""" Raw textout stream unit. """

	BEGIN   = 1
	END     = 2
	SPECIAL = 3
	NEWLINE = 4
	PARSEP  = 5

	def __init__(self, *args):
		if len(args) > 1:
			self.type, self.name, self.value, *_ = args + (None,)
			return

		result = args[0]
		gr = result.groupdict()

		self.name = None
		self.value = None

		if   gr['sname'] == '\n':
			self.type = self.NEWLINE
		elif gr['parsep'] != None:
			self.type = self.PARSEP
		elif gr['bname'] != None:
			self.type = self.BEGIN
			self.name = gr['bname']
			self.value = gr['value']

			self.full = "[{}{}]".format(self.name,
				"=" + self.value if self.value != None else "")
		elif gr['ename'] != None:
			self.type = self.END
			self.name = gr['ename']
			self.full = "[/" + self.name + "]"
		else:
			self.type = self.SPECIAL
			self.name = gr['sname']

			self.full = self.name

		if self.name != None:
			self.name = self.name.lower()
			if self.type != self.SPECIAL:
				self.name = "[{}]".format(self.name)

	def __repr__(self):
		typetab = {self.BEGIN: "begin", self.END: "end",
			self.SPECIAL: "special", self.NEWLINE: "newline"}
		return '_TextoutUnit(type={}{}{})'.format(\
			typetab[self.type],
			', name=' + repr(self.name) if self.name != None else "",
			', value=' + repr(self.value) if self.value != None else "")

	def __equ__(self, other):
		if not isinstance(other, TextoutUnit):
			return False
		if self.type == other.type \
		and (self.type == self.NEWLINE or self.name == other.name) \
		and (self.type != self.BEGIN or self.value == other.value):
			return False
		return True

class TextoutStream:
	""" Textout stream, for easier stream processing.

		The idea behind this stream is that it will provide more suitable
		(therefore easier to process) data for the applications above,
		with raw text and tags. """

	# A tag can basically be one of the following things:
	# - a starting tag, looking like [<name>] or [<name>=<attribute>]
	# - an ending tag, looking like [/<name>]
	# - a special tag (starting or ending), usually one-char (the only
	#   one currently available is the ` tag).
	#
	# A tag name is 32 chars at most (at least 1 char).
	# A closing tag can have no name, which means that it will close the
	# last opened tag automatically.
	# A tag attribute is 256 chars at most.
	#
	# FIXME: check the sizes? it seems that it stopped working…

	_Tag = _re.compile("""\
		\[\s?
		(?P<bname>
			(?P<bname_e>[^\/\[\]\=][^\[\]\=]* (\[(?&bname_e)\]?)*)*
		)
		(\s?=\s?(?P<value>
			(?P<value_e>[^\[\]]* (\[(?&value_e)\]?)*)*
		))?
		\s?\]
	|
		\[[\\\/]\s?(?P<ename>
			(?P<ename_e>[^\/\[\]\=][^\[\]\=]* (\[(?&ename_e)\]?)*)*
		)\s?\]
	|
		(?P<parsep>[\n]{2,})
	|
		(?P<sname>`|[\n])
	""", _re.VERBOSE | _re.DOTALL | _re.MULTILINE)

	# Keep this buffer size above the maximum size of a tag (387)
	# for this class to work alright. Anything above 512 should work great.

	BUFFER_SIZE = 1024

	def __init__(self, stream):
		# If the 'stream' is a string, we want to use standard stream
		# functions, so we're gonna enforce them using the `StringIO` class.

		if isinstance(stream, str):
			stream = _io.StringIO(stream)

		# Buffer management.

		self.stream = stream
		self.buf = ""

		# Management of the last tag match.

		self.result = None
		self.last = None

		# Error position.

		self.pos = 0
		self.line = 0
		self.col = 0

	def __iter__(self):
		# This class is (obviously) iterable.
		# We want to use this class as the iterator as well.

		return self

	def __next__(self):
		# If we have a result, process it.

		if self.result:
			data, self.result = TextoutUnit(self.result), None
			self.last = data
			return data

		# Make sure to have enough data to read.

		self.buf += self.stream.read(self.BUFFER_SIZE - len(self.buf))
		if not self.buf:
			self.last = None
			raise StopIteration

		# Check that we have a result.

		result = self._Tag.search(self.buf, partial = True)
		if not result:
			text = self.buf
			self.buf = ''
			self.last = text
			return text

		# If there is some text, return it.
		# Eventually store the result so we can process it later.

		if result.start() > 0:
			ret = self.buf[:result.start()]
			self.buf = self.buf[result.end():]
			if not result.partial:
				self.result = result
			self.last = ret
			return ret

		# Process the result now!

		self.buf = self.buf[result.end():]
		data = TextoutUnit(result)
		self.last = data
		return data

# End of file.
