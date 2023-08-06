#!/usr/bin/env python3
#******************************************************************************
# Copyright (C) 2018 Thomas "Cakeisalie5" Touhey <thomas@touhey.fr>
# This file is part of the textoutpc project, which is MIT-licensed.
#******************************************************************************
""" Main translation function.
	See the `Translator` class documentation for more information.
"""

import string as _string
from copy import deepcopy as _deepcopy

from ._options import TextoutBlockTag as _TextoutBlockTag, \
    TextoutParagraphTag as _TextoutParagraphTag, TextoutOptions as _Options
from ._stream import TextoutStream as _TextoutStream
from ._html import escape as _htmlescape, urls as _htmlurls

__all__ = ["Translator"]

# ---
# Tweaks interface.
# ---

class _TweaksDictionary:
	""" Tweaks dictionary. Read-only, and makes sure to match equivalent
		tweak keyword, e.g. `label_prefix`, `LABELPREFIX` and
		`__LaBeL___PRE_FIX__`. """

	def __init__(self, base):
		self.__elts = {}

		for kw in base:
			self.__elts[self.__normalize(kw)] = base[kw]

	def __repr__(self):
		return f"{self.__class__.__name__}({repr(self.__elts)})"

	def __getitem__(self, key):
		return self.__elts[key]

	def __normalize(self, name):
		return ''.join(c for c in name if c in _string.ascii_letters).lower()

# ---
# Tag data utility.
# ---

class _TagData:
	BLOCK = 1
	INLINE = 2

	def __init__(self, tag, name, full):
		""" Tag data initialization.
			Here, we prepare all of the attributes from the tag's
			after-preparation attributes. """

		# `name` is the name through which the tag has been called.
		# `full` is the full tag beginning mark.

		self.name = name
		self.type = self.BLOCK if isinstance(tag, _TextoutBlockTag) \
			else self.INLINE
		self.full = full

		# Tag beginning displaying.
		# `notempty` is the moment when (and if) to start displaying the
		# tag's code and content.
		# `started` is whether the tag's beginning has been processed,
		# i.e. if the content is no longer processed.

		self.notempty = bool(tag.notempty) if hasattr(tag, 'notempty') \
			else False
		self.started = False

		# `base` is the actual tag object returned by `get_tag()`.

		self.base = tag

		# Flags and properties calculated from the tag's attributes, using the
		# rules given in `TAGS.md`.
		# `ign` is whether the content should be read while the tag is opened.
		# `generic` is whether the tag can be terminated by the generic
		# tag ending mark [/].
		# `raw` is whether the tag's content should be read as raw.
		# `super` is whether the tag is a superblock or not.
		# `inlined` is whether the next block on the same level is turned into
		# a superblock or not.

		self.ign = not hasattr(tag, 'preprocess') and hasattr(tag, 'content')

		self.generic = False if name == None else bool(tag.generic) \
			if hasattr(tag, 'generic') else True

		self.raw = bool(tag.raw) if hasattr(tag, 'raw') \
			else hasattr(tag, 'preprocess')

		self.super = True if hasattr(tag, 'preprocess') else \
			bool(tag.superblock) if hasattr(tag, 'superblock') \
			else False

		self.inlined = bool(tag.inlined) if self.super \
			and hasattr(tag, 'inlined') and bool(tag.inlined) else False

		# Content processing utilities.
		# `last` is the content of the tag. A boolean indicates that we
		# only want to know if the content is empty or not, and a string
		# means we want to get the full content to re-use it later.
		# In order not to manage a third case, even if the tag doesn't care
		# if its content is empty or not, this property should be set to
		# `False`.

		self.last = "" if hasattr(tag, 'preprocess') else False

		# Reset the tag.

		self.reset()

	def reset(self):
		""" Reset the tag, generally because it has been closed. """

		self.tag = _deepcopy(self.base)
		self.started = False
		if isinstance(self.last, bool):
			self.last = False
		else:
			self.last = ""

	def __repr__(self):
		return '<TagData tag=' + repr(self.tag) + '>'

# ---
# Translator main class.
# ---

class Translator:
	""" One-time usage class for translating.
		Use it this way: `Translator(my_inp, my_outp).process()`.

		You can even chain calls as the `process()` method returns
		the output stream object. """

	def __init__(self, inp, outp, output_type, tweaks, options):
		""" Initializer. """

		if not output_type in ('html', 'lightscript'):
			raise Exception("Invalid output type")
		self.output_type = output_type

		self.tweaks = _TweaksDictionary(tweaks)
		self.options = options

		self.inp = inp
		self.outp = outp

		# `queue` is the queue of tag containers, with the actual tag
		# objects, calculated tag properties, variables for content processing,
		# and other stuff.
		# `cign` is the number of tags requiring the content to be ignored.

		self.queue = []
		self.cign = 0

		# Text group management.
		# In the following example text:
		#
		#	some [incredible] text [align=center] you know
		#
		# There are two input groups, what's before and what's after the
		# valid `[align=center]` tag. We want to flush the text in two steps
		# only, in order to detect things such as URLs and smileys.
		#
		# The text group also manages the invalid tags, to manage URLs with
		# brackets in it, e.g. https://example.org/[some-incredible-thing]-yea

		self.text_group = ""

		# `raw_mode` is whether the no evaluating mode is on or not.
		# `raw_deg` is the number of times the raw tag has to be closed
		# to exit.

		self.raw_mode = False
		self.raw_deg = 0

		# `inline_mode` is whether the inline mode is on or not.
		# Actually, for now, this mode is only global and cannot be enabled
		# by tags.

		self.inline_mode = bool(self.tweak("inline", False))

	def __repr__(self):
		p = []
		p.append(f"inp = {repr(self.inp)}")
		p.append(f"outp = {repr(self.outp)}")
		p.append(f"output_type = {repr(self.output_type)}")
		p.append(f"tweaks = {repr(self.tweaks)}")
		p.append(f"options = {repr(self.options)}")

		return f"{self.__class__.__name__}({', '.join(p)})"

	def tweak(self, key, default = None):
		""" Get a tweak from the tweaks dictionary. """

		try:
			return self.tweaks[key]
		except KeyError:
			return default

	# ---
	# Text outputting utilities.
	# ---

	def process_text(self, text):
		""" Process text groups for naked URLs and stuff. """

		# In all cases, we want to escape for HTML things, so that the
		# user doesn't insert raw HTML tags (which would be a security flaw!).

		if self.output_type == 'html':
			text = _htmlescape(text)

		# For non-raw HTML, we want to add smiley and URLs conversion,
		# because it's nicer!

		if not self.raw_mode and self.output_type == 'html':
			text = _htmlurls(text)
			text = self.options.htmlsmileys(text)

		return text

	def put_text(self, text):
		""" Output some text. """

		# If we want to ignore the content (because it is not used
		# nor output), let the text fall into the void.

		if self.cign > 0:
			return

		# Add to the text group, which will be processed when `flush_text()`
		# is used.

		self.text_group += text

	def flush_text(self, superblocks_only = False,
		next_block_is_super = False):
		""" Flush the text that has been output. """

		# First of all, check if the text group is empty or if we want to
		# ignore it.

		if not self.text_group or self.cign > 0:
			return

		# Pop the text group and put the code, with the process function in
		# case it is given to a non-raw processing tag or given to the
		# output.

		text = self.text_group
		self.text_group = ""

		self.add_text(text, process_func = lambda x: self.process_text(x),
			superblocks_only = superblocks_only,
			next_block_is_super = next_block_is_super)

	# ---
	# Code outputting utilities.
	# ---

	def add_text(self, text, process_func = lambda x: x, start_tags = True,
		superblocks_only = False, next_block_is_super = False,
		skip_first = False):
		""" Add text to the higher blocks if available. """

		# The last queue is composed of booleans (does the group contain
		# something or not) and texts for content processing.
		# We want to set all of the booleans to True until the first text
		# group, to which we want to add the current text.
		# If there is no content preprocessing and we have to output it,
		# we want to start the tags first: `dat == None` will be our signal!

		blockfound = False
		for dat in self.queue:
			# Check if it is a tag we want to contribute to.

			if dat.type == dat.BLOCK:
				if dat.super or next_block_is_super:
					blockfound = True
					next_block_is_super = dat.inlined
				elif not superblocks_only and not blockfound:
					blockfound = True
					next_block_is_super = dat.inlined
				else:
					continue

			# Check if it is the first tag we want to skip.

			if skip_first:
				skip_first = False
				continue

			# Contribute to it, either by or-ing the content if it is
			# a boolean (but anything or True == True), or by contributing
			# to the buffer otherwise.

			if isinstance(dat.last, bool):
				dat.last = True
				continue

			# Start the tags if we're about to give this content to
			# preprocessing.

			if start_tags:
				self.start_tags()

			# Add the content to the preprocess buffer.

			if not dat.raw:
				text = process_func(text)
			dat.last += text

			break
		else:
			# No `break` has been encountered, which means the content has
			# not been added to any preprocessing tag. Please process it!

			if start_tags:
				self.start_tags()
			self.outp.write(process_func(text))

			return False

		# The content has been given for preprocessing.

		return True

	def put_debug(self, message):
		""" Put a debug message directly into the output. """

		self.outp.write(message)

	def put_code(self, code, start_tags = True, flush_text = True,
		superblocks_only = True, next_block_is_super = False,
		skip_first = False):
		""" Put some code. """

		# We don't want to mix text and code, so we'll flush to be sure that
		# the order doesn't get mixed up.

		if flush_text:
			self.flush_text()

		# First of all, check if the text is empty or if we want to ignore it.

		if not code or self.cign > 0:
			return

		# Add the code.

		self.add_text(code, start_tags = start_tags,
			superblocks_only = superblocks_only,
			next_block_is_super = next_block_is_super,
			skip_first = skip_first)

	def put_newline(self):
		""" Put a newline. """

		# The newline depends on the output type and the context, of course.

		if self.output_type == 'html' and not self.raw_mode:
			newline = '<br />\n'
		else:
			newline = '\n'

		# Then put this as one puts code.

		self.put_code(newline)

	# ---
	# Tag queue management.
	# ---

	def push_tag(self, dat):
		""" Push a tag onto the tag stack. """

		# If the tag does not process its content but replaces the content,
		# that means the content is ignored.

		if dat.ign:
			self.cign += 1

		# If we're about to put a tag or anything, empty the text block
		# here.

		self.flush_text()

		# Insert the tag into the queue.

		self.queue.insert(0, dat)

		# Start the tag (and parent tags) if required.

		self.start_tags()

		# Don't forget to add the tag to the queue, and to enable raw
		# mode if the tag expects a raw content (e.g. `[code]`).

		if dat.raw:
			self.raw_mode = True
			self.raw_deg = 0

	def pop_tag(self, end = ""):
		""" Pop a tag from the tag stack.
			`end` represents the full version of the ending tag marker,
			for displaying if the tag is invalid. """

		if not self.queue:
			return

		# Even if we had no beginning, no content and no end, what is
		# here has to be distinguished from what was right before!
		# So we need to flush the text group for this.
		# (this will probably be useless for tags with preprocessing enabled,
		# but that's okay, flushing doesn't modify the content processing
		# queue)

		self.flush_text()

		# Pop the tag out of the queue.

		dat = self.queue.pop(0)
		tag = dat.tag

		pcattrs = {'superblocks_only': dat.type == dat.BLOCK,
			'next_block_is_super': dat.inlined}

		# If preprocessing has been enabled, we ought to process the content,
		# check if the tag is valid, and do everything we would have done
		# while pushing the tag if it didn't do content processing.

		if hasattr(tag, 'preprocess'):
			# Take out the content of the content preprocessing queue.
			# If there is no content and the tag proposes a default content,
			# let's use it instead.

			content = dat.last
			if not content and hasattr(tag, 'default'):
				try:
					content = tag.default()
				except:
					# The tag is not supposed to have an empty content,
					# so we ought to put it as an invalid tag an go on.

					self.put_text(dat.full)
					self.put_text(end)
					return

			# Send the content to the tag while checking its validity (by
			# checking if the `preprocess()` method returns an exception).

			try:
				ct = tag.preprocess(content)
			except:
				# The tag is invalid in the end, so we ought to send the
				# raw things to the text group and forget about the tag.

				self.put_text(dat.full)
				self.put_text(content)
				self.put_text(end)
				return

			# If we're here, congrats, the tag is valid! Now, if the
			# `preprocess()` method returned something different, we
			# want to use it instead.

			if ct != None:
				content = ct

			# Output the beginning and the content. If there was no content,
			# just put the content that we got earlier.

			if hasattr(tag, 'begin'):
				self.put_code(tag.begin(), **pcattrs)
			dat.started = True

			if hasattr(tag, 'content'):
				self.put_code(tag.content(), **pcattrs)
			elif dat.raw:
				# XXX: I'm unsure about this. Shall raw tags return code
				# or text? The text will only be escaped as raw mode is
				# still enabled at this point.

				self.put_text(content)
			else:
				self.put_code(content, **pcattrs)
		elif hasattr(tag, 'content'):
			# Tag replaces content without preprocessing, which means
			# the content has been ignored and the tag only puts the
			# things.

			self.cign -= 1
			self.put_code(tag.content(), **pcattrs)
		elif hasattr(tag, 'default'):
			# Tag defines a default content if there might be none,
			# without text preprocessing. If there is no content, print it.
			# Notice that the default content method can also raise
			# an exception if the tag in its current configuration should
			# not have an empty content.

			if not dat.started:
				if hasattr(dat.tag, 'begin'):
					self.put_code(dat.tag.begin(), **pcattrs)
				dat.started = True

			if not dat.last:
				try:
					self.put_text(tag.default())
				except:
					# The tag is not supposed to have empty content!
					# Let's put the raw things again as when there is
					# content processing.

					self.put_text(dat.full)
					self.put_text(end)
					return

		# Don't forget to end the tag!

		if not dat.started:
			pass
		else:
			if dat.type == dat.BLOCK:
				self.close_inline_tags()
			if hasattr(tag, 'end'):
				self.put_code(tag.end(), start_tags = False, **pcattrs)

		# Disable raw mode if it was a raw tag (which means that it enabled it,
		# as tags into raw tags cannot be processed).

		if dat.raw:
			self.raw_mode = False

	# ---
	# Automatically start and end tags.
	# ---

	def start_tags(self):
		""" Start the tags that haven't been started yet.
			If a block has been newly opened, we ought to close the block at
			the same level as them before opening it.
			This is usually called when content is output, for tags that
			aren't empty. """

		# First, get the references to the blocks to end, the blocks to
		# start, and all of the inline tags.

		superblocks = []
		block_to_start = None
		block_to_end = None
		inlines = []

		next_block_is_super = False
		for idx, dat in enumerate(self.queue):
			# Check that the tag hasn't already been started or doesn't call
			# for content processing.

			if idx > 0 and type(dat.last) != bool:
				break

			# Then put the tag in the appropriate queue.

			if dat.type == dat.BLOCK:
				if   block_to_start is not None and \
					dat.super or next_block_is_super:
					# The block is to be considered as the block to start.
					# Sometimes the block to start is the latest superblock!

					superblocks.insert(0, dat)
					next_block_is_super = dat.inlined
				elif dat.started:
					block_to_end = dat
					next_block_is_super = dat.inlined
				elif block_to_end is None and block_to_start is None:
					block_to_start = dat
					next_block_is_super = dat.inlined
			else:
				inlines.insert(0, dat)

		# If there is no new block to start, there's no need to end the
		# current block.

		if not block_to_start:
			block_to_end = None

		# Put the tag ends for the blocks to end.
		# If there are some, we ought to close the inline tags first.

		if block_to_end is not None:
			for dat in inlines[::-1] + [block_to_end]:
				if not dat.started:
					continue

				if hasattr(dat.tag, 'end'):
					self.put_code(dat.tag.end(), start_tags = False,
						skip_first = True)
				dat.started = False
				dat.reset()

		# Then, put the tag beginnings.

		to_begin = superblocks \
			+ ([block_to_start] if block_to_start else []) \
			+ inlines

		for dat in to_begin:
			if dat.started:
				continue
			if dat.notempty and not dat.last:
				break

			if hasattr(dat.tag, 'begin'):
				self.put_code(dat.tag.begin(), start_tags = False,
					flush_text = False, skip_first = dat == self.queue[0])
			dat.started = True

	def close_inline_tags(self):
		""" We're about to close a block, so we want to close any inline tags
			that could have been taken within it. """

		for dat in self.queue:
			# Check that the tag hasn't already been closed.

			if dat.type != dat.INLINE or not dat.started:
				continue

			if hasattr(dat.tag, 'end'):
				self.put_code(dat.tag.end(), start_tags = False)
			dat.started = False
			dat.reset()

	# ---
	# Main function.
	# ---

	def process(self):
		""" Main function of the textout translator. """

		# By default, everything is in a paragraph.
		# Other blocks will supplant this by being further in the queue.

		if not self.inline_mode:
			self.push_tag(_TagData(_TextoutParagraphTag(None, None,
				self.output_type, self.tweaks, self.options), None, ''))

		# We want to get our elements out of the element stream (Lephe
		# told me that the `TextoutStream` class was actually a lexer,
		# but as I don't know the theory behind this...).

		for element in _TextoutStream(self.inp):
			# If it is a string or a newline, let's just put it.
			# Otherwise, the element is some tag data or at least something
			# that requires some special processing.

			if isinstance(element, str):
				self.put_text(element)
				continue

			tagdata = element
			if tagdata.type == tagdata.NEWLINE:
				self.put_newline()
				continue

			# XXX: As we don't manage paragraphs for now, end of lines and
			# paragraphs separator are just output for now.

			if not tagdata.type in (tagdata.BEGIN, tagdata.END, \
				tagdata.SPECIAL):
				self.put_text(tagdata.full)
				continue

			# Check if it is a tag end (we do not know for special tags,
			# as they usually are one-character long).

			if tagdata.type in (tagdata.END, tagdata.SPECIAL):
				# If raw mode is activated, that means that the queue is not
				# empty and that the top tag of the queue is the tag that
				# initiated raw mode. We're just going to check that the name
				# corresponds, and that the tag has not be opened into
				# itself (see the description of `raw_deg` in the
				# initializer).

				if self.raw_mode:
					if tagdata.name != self.queue[0].name \
					and not (tagdata.name == "[]" and self.queue[0].generic):
						self.put_text(tagdata.full)
						continue
					if self.raw_deg > 0:
						self.put_text(tagdata.full)
						self.raw_deg -= 1
						continue

				# Check to which opened tag the ending tag corresponds.

				pos = -1
				if tagdata.name == "[]":
					# Generic closing tag [/] management.
					# `pos` is set to 0 here.
					for qpos, qdat in enumerate(self.queue):
						if qdat.name != None:
							pos = qpos
							break
				else:
					# Get the position corresponding to the tag.
					for qpos, qdat in enumerate(self.queue):
						if tagdata.name == qdat.name:
							pos = qpos
							break

				# Then react to `pos`.
				# If `pos` is 0 or above, an opening tag has been found.
				# We ought to autoclose opened stuff which are not
				# terminated explicitely, and close the tag closed explicitely.

				if pos >= 0:
					while pos > 0:
						self.pop_tag()
						pos -= 1
					self.pop_tag(tagdata.full)
					continue

				if tagdata.type == tagdata.END:
					self.put_text(tagdata.full)
					continue

				# If we are here, the tag is a special tag which hasn't been
				# identified to be an ending tag. We don't want to stop because
				# that means it is a beginning tag.

			# From here, we know the tag is not a beginning tag.
			# In raw mode, always display the tag, but if the tag corresponds
			# to the raw tag opened, augment the number of tags required to
			# close the raw tag.

			if self.raw_mode:
				if tagdata.name == self.queue[0].name:
					self.raw_deg += 1

				self.put_text(tagdata.full)
				continue

			# Get the initialized tag with the name and value.
			# If the tag is unknown, output the full thing and just go on.

			try:
				tag = self.options.get_tag(tagdata.name)
			except:
				self.put_text(tagdata.full)
				continue

			value = tagdata.value
			if value != None and hasattr(tag, 'procvalue') and tag.procvalue:
				value = self.process_text(value)

			try:
				tag = tag(tagdata.name, value, self.output_type, self.tweaks,
					self.options)
			except:
				self.put_text(tagdata.full)
				continue

			# Check if it is a block tag.

			dat = _TagData(tag, tagdata.name, tagdata.full)
			if self.inline_mode and dat.type == dat.BLOCK:
				self.put_text(tagdata.full)
				continue

			# And don't forget to push the tag (through its data).

			self.push_tag(dat)

			# Push a paragraph tag if the block is a superblock.

			if dat.type == dat.BLOCK and dat.super and not dat.raw \
				and not dat.inlined:
				self.push_tag(_TagData(_TextoutParagraphTag(None, None,
					self.output_type, self.tweaks, self.options), None, ''))

		# End of file, it seems! Let's close the tags, flush the text
		# and just resume our lives from there.

		while self.queue:
			self.pop_tag()
		self.flush_text()

		# And don't forget to return the output for the user to chain
		# stuff easily ;)

		return self.outp

	def reopen(self, inp, outp):
		""" Open another instance of this translator for sub-translators. """

		return Translator(inp, outp, self.output_type, self.tweaks,
			self.options)

# End of file.
