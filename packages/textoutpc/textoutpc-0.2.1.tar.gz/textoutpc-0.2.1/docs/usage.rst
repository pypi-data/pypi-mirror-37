Using textoutpc
===============

To use this module, simply use the ``to<language>()`` functions once imported:

.. code-block:: python

	#!/usr/bin/env python3
	import textoutpc

	text = "Hello, [i]beautiful [b]world[/i]!"
	print(textoutpc.tohtml(text))
	print("---")
	print(textoutpc.tolightscript(text))

The supported output types are:

- ``html``: `HTML`_ compatible output, requiring some additional style and
  script;
- ``lightscript``: `Lightscript`_ Markdown-like language. See
  `the Lightscript topic on Planète Casio <Lightscript topic>`_ for
  more information.

The ``tohtml()`` and ``tolightscript()`` can take additional keywords that
tags can read so that they can adapt their behaviour. The name of the tweaks
are case-insensitive and non-alphanumeric characters are ignored: for example,
``label_prefix``, ``LABELPREFIX`` and ``__LaBeL___PRE_FIX__`` are all
equivalent.

The following tweaks are read by the translator and built-in tags:

- ``inline``: if ``True``, only use inline tags, not blocks (for inline
  contexts such as instant messaging or one-line comments).
- ``label_prefix`` (HTML): prefix to be used by the ``[label]`` and
  ``[target]`` tags, e.g. ``msg45529-``. Defaults to `""` for PCv42
  compatibility;
- ``obsolete_tags`` (HTML): use obsolete HTML tags for old browsers
  (e.g. lynx) compatibility, e.g. ``<b>``, ``<i>``, ``<center>``, and
  others. Defaults to ``True``.
- ``title_level`` (HTML): level at which to start for titles and subtitles,
  e.g. ``h5`` for ``h5`` for titles and ``h6`` for subtitles``.

An example call would be:

.. code-block:: python

	#!/usr/bin/env python3
	import textoutpc

	print(textoutpc.tohtml("Hello, [i]beautiful[/i]!", obsolete__TAGS=False))

.. _HTML: https://www.w3.org/html/
.. _Lightscript: https://git.planet-casio.com/lephe/lightscript
.. _Lightscript topic: https://planet-casio.com/Fr/forums/lecture_sujet.php?id=15022
