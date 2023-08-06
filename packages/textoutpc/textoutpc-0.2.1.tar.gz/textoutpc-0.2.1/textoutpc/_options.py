#!/usr/bin/env python3
#******************************************************************************
# Copyright (C) 2018 Thomas "Cakeisalie5" Touhey <thomas@touhey.fr>
# This file is part of the textoutpc project, which is MIT-licensed.
#******************************************************************************
""" Base classes to use with options (tags, smileys) in textoutpc, with a
	manager class.

	For your tag to be used as a textoutpc tag, you have to make it
	inherit one of the `TextoutBlockTag` or `TextoutInlineTag` classes.

	Making separate tag modules is possible through the manager class,
	which allows not to hardcode the tags into the module. """

from functools import partial as _p
from inspect import ismodule as _ismod, isclass as _isclass, \
	getargspec as _getargspec, getfullargspec as _getfullargspec, \
	currentframe as _currentframe, getouterframes as _getouterframes
from importlib import import_module as _importmod

from ._html import SmileyConvertor as _htmlsm

__all__ = ["TextoutOptions",
	"TextoutTag", "TextoutBlockTag", "TextoutInlineTag", "TextoutParagraphTag",
	"TextoutSmiley", "TextoutImage", "TextoutVideo"]

def _getargscount(func):
	try:
		return len(_getfullargspec(func).args)
	except:
		return len(_getargspec(func).args)

# ---
# Tags.
# ---

# Main base tag class.
# For more about defining a tag, see `doc/tags.md`.

class TextoutTag:
	""" The textout tag base class.
		Is initialized with these values:

		<name><content><name>
			| name: "<name>" (only special chars such as `)
			| value: None
		[<name>]<content>[/<name>]
			| name: "[<name>]"
			| value: None
		[<name>]<content>[/] (when possible)
			| name: "[<name>]"
			| value: None
		[<name>=<value>]<content>[/<name>]
			| name: "[<name>]"
			| value: "<value>"
		[<name>=<value>]<content>[/] (when possible)
			| name: "[<name>]"
			| value: "<value>" """

	aliases = ()

	def __init__(self, name, value, ot, tweaks, options):
		""" Initialize the textout tag with the documented members. """

		# Store internal data.

		self.__name = name
		self.__value = value
		self.__output_type = ot
		self.__tweaks = tweaks
		self.__options = options

		self.output_type = ot

		# Call both prepare functions.

		if hasattr(self, 'prepare'):
			try:
				assert _getargscount(self.prepare) == 4
				args = (name, value, ot)
			except:
				args = (name, value)
			self.prepare(*args)
		if hasattr(self, 'prepare_' + ot):
			prep = getattr(self, 'prepare_' + ot)
			try:
				assert len(_getargspec(prep).args) == 4
				args = (name, value, ot)
			except:
				args = (name, value)
			prep(*args)

		# Prepare the preprocessing elements.

		if hasattr(self, 'preprocess'):
			if hasattr(self, 'preprocess_' + ot):
				self.__preprocess0 = self.preprocess
				self.preprocess = self.__preprocess_double
		elif hasattr(self, 'preprocess_' + ot):
			self.preprocess = getattr(self, 'preprocess_' + ot)

		if hasattr(self, 'preprocess'):
			self.__preprocess2 = self.preprocess
			self.preprocess = self.__preprocess_and_prepare
		else:
			self.__after_preprocess()

		if hasattr(self, 'default_' + ot):
			self.default = getattr(self, 'default_' + ot)

	def __repr__(self):
		return f"{self.__class__.__name__}(name = {repr(self.__name)}, " \
			f"value = {repr(self.__value)}, " \
			f"ot = {repr(self.__output_type)})"

	def __preprocess_double(self, content):
		""" Preprocess using the two methods. """

		ct = self.__preprocess0(content)
		if ct != None:
			content = ct
			del ct

		ct = self.__preprocess1(content)
		if ct != None:
			content = ct
			del ct

		return content

	def __preprocess_and_prepare(self, content):
		""" Preprocess and do the things after. """

		ret = self.__preprocess2(content)
		self.__after_preprocess()
		return ret

	def __out(self, name):
		""" Generic function to call two output functions of the same
			type. """

		getattr(self, '__' + name)()
		getattr(self, name + '_' + self.__output_type)()

	def __after_preprocess(self):
		""" After preprocessing, check the begin, content and end that may
			have been set by the preprocessing function. """

		ot = self.__output_type

		for otype in ('begin', 'content', 'end'):
			if hasattr(self, otype):
				if hasattr(self, otype + '_' + ot):
					setattr(self, '__' + otype, getattr(self, otype))
					setattr(self, otype, _p(self.__out, otype))
			elif hasattr(self, otype + '_' + ot):
				setattr(self, otype, getattr(self, otype + '_' + ot))

	def tweak(self, key, default = None):
		try:
			return self.__tweaks[key]
		except KeyError:
			return default

	def image(self, *args, **kwargs):
		return self.__options.get_image(*args, **kwargs)

	def video(self, *args, **kwargs):
		return self.__options.get_video(*args, **kwargs)

# Role-specific base tag classes.

class TextoutBlockTag(TextoutTag):
	pass
class TextoutInlineTag(TextoutTag):
	pass

# Default tag: paragraph.

class TextoutParagraphTag(TextoutBlockTag):
	""" Main tag for basic paragraphs. """

	notempty = True

	def begin_html(self):
		return '<p>'

	def end_html(self):
		return '</p>'

# ---
# Smileys.
# ---

class TextoutSmiley:
	""" Base class for smileys. """

	aliases = ()
	url = None

	def __repr__(self):
		return f"{self.__class__.__name__}(aliases = {repr(self.aliases)}, " \
			f"url = {repr(self.url)})"

# ---
# Multimedia.
# ---

class TextoutImage:
	""" Base class for images. """

	def __init__(self, url):
		raise ValueError("no URL supported")

class TextoutVideo:
	""" Base class for videos. """

	def __init__(self, url):
		raise ValueError("no URL supported")

# ---
# Options extractor and manager.
# ---

_builtin_module = None
def _get_builtin_module():
	""" Get the `.builtin` module. """

	global _builtin_module

	if _builtin_module == None:
		_builtin_module = _importmod('..builtin', __name__)
	return _builtin_module

class TextoutOptions:
	""" Options manager.
		Object responsible for getting the tags. """

	def __init__(self, *modules, default = True):
		self._aliases = {}
		self._s_aliases = {}
		self._videos = []
		self._images = []

		if default:
			self.add(_get_builtin_module())
		for mod in modules:
			self.add(mod)

	def __repr__(self):
		return f"{self.__class__.__name__}()"

	def add(self, element):
		""" Add an option. """

		if isinstance(element, str):
			element = str(element)
			element = _importmod(element,
				_getouterframes(_currentframe(), 1)[0].name)

		if _ismod(element):
			self.__extract(element)
			return True

		if _isclass(element) and issubclass(element, TextoutTag):
			for alias in element.aliases:
				self._aliases[alias] = element
			return True

		if _isclass(element) and issubclass(element, TextoutSmiley):
			for alias in element.aliases:
				self._s_aliases[alias] = element

			self._htmlsm = None
			return True

		if _isclass(element) and issubclass(element, TextoutImage):
			if not any(image is element for image in self._images):
				self._images.append(element)

		if _isclass(element) and issubclass(element, TextoutVideo):
			if not any(video is element for video in self._videos):
				self._videos.append(element)

	def __extract(self, module):
		""" Extract options from a module. """

		tags = []
		smileys = []

		# Obtain the list of properties from the module.

		try:
			ds = module.__all__
		except:
			ds = dir(module)

		# Get the submodules from the module (usually different files in the
		# tags module folder).

		for submodule in (obj for name, obj in ((nm, getattr(module, nm)) \
		for nm in ds) if (name == '__init__' or name[0] != '_') \
		and _ismod(obj)):
			self.__extract(submodule)

		# Extract the tags from the current module.

		for obj in (obj for name, obj in ((nm, getattr(module, nm)) \
			for nm in ds) if name[0] != '_'):
			self.add(obj)

	def get_smileys(self):
		""" Get the smileys dictionary. """

		return self._s_aliases.copy()

	def htmlsmileys(self, text):
		""" Get the smileys convertor for HTML. """

		if not self._htmlsm:
			self._htmlsm = _htmlsm(self._s_aliases)
		return self._htmlsm.convert(text)

	def get_video(self, url):
		""" Get a video using its URL. """

		for video in self._videos:
			try:
				v = video(url)
			except:
				continue
			break
		else:
			raise ValueError("invalid video URL")
		return v

	def get_image(self, url):
		""" Get an image using its URL. """

		for image in self._images:
			try:
				i = image(url)
			except:
				continue
			break
		else:
			raise ValueError("invalid image URL")
		return i

	def get_tag(self, name):
		""" Get the tag class corresponding to a name. """

		return self._aliases[name]

# End of file.
