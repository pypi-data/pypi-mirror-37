#!/usr/bin/env python3
#******************************************************************************
# Copyright (C) 2018 Thomas "Cakeisalie5" Touhey <thomas@touhey.fr>
# This file is part of the textoutpc project, which is MIT-licensed.
#******************************************************************************
""" Functions for the user.
	Really simplifies the thing.
"""

from io import StringIO as _StringIO

from ._options import TextoutOptions as Options, \
	TextoutBlockTag as BlockTag, TextoutInlineTag as InlineTag, \
	TextoutParagraphTag as ParagraphTag, TextoutSmiley as Smiley, \
	TextoutImage as Image, TextoutVideo as Video
from ._translate import Translator as _Translator

__all__ = ["version", "tohtml", "tolightscript",
	"Options", "BlockTag", "ParagraphTag", "InlineTag",
	"Smiley", "Image", "Video"]

version = "0.2.1"

# ---
# Public functions.
# ---

_default_options = Options()

def tohtml(message, options = _default_options, **tweaks):
	""" Converts textout BBcode to HTML.
		Receives a string, returns a string. """

	t = _Translator(_StringIO(message), _StringIO(), 'html', \
		tweaks, options)
	return t.process().getvalue()

def tolightscript(message, options = _default_options, **tweaks):
	""" Converts textout BBcode to Lightscript.
		Receives a string, returns a string. """

	return "" # TODO: real thing one day

	return _Translator(_StringIO(message), _StringIO(), 'lightscript', \
		tweaks, options).process().getvalue()

# End of file.
