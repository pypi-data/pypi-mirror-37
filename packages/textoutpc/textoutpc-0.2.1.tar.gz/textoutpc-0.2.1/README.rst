Planète Casio's textout() BBcode markup language translator
===========================================================

This module contains a BBcode to HTML translator for
`Planète Casio`_. For more information, read the
documentation accessible on `the official website`_.

.. warning::

	If you are accessing this repository from `Planète Casio's forge`_,
	keep in mind that it is only a mirror and that the real repository
	is located `in my forge <Thomas' forge_>`_ for now.

What is left to do
------------------

- Implement the ``not_within_itself`` attribute (for ``[*]``).
- Implement the ``allowed_tags`` attribute to only allow a set of tags within
  itself.
- Implement the ``only_allowed_tags`` attribute (for ``[list] blah [*]`` to
  ignore ``blah`` and anything outside of ``[*]`` tags which is in
  ``allow_tags``).
- Add an ``[imgurl]`` tag?
- Manage lightscript (or even markdown?) as output languages;
- Check where the errors are to display them to the user:

  * Count character offset, line number and column number in the lexer;
  * Produce readable exceptions;
  * Make a clean interface to transmit them;
- Check why exceptions on raw tags effectively escape the content, as it
  shouldn't…?
- Look for security flaws (we really don't want stored XSS flaws!).
- Implement match names (such as ``\[\*+\]`` for lists).
- Manage keywords with tags such as ``[tag key=value other="something else"]``.

.. _Planète Casio: https://www.planet-casio.com/
.. _Planète Casio's forge: https://gitea.planet-casio.com/
.. _Thomas' forge: https://forge.touhey.fr/pc/textout.git
.. _the official website: https://textout.touhey.fr/
