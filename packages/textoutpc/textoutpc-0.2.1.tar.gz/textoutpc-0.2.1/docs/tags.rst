Defining tags for textoutpc
===========================

A tag is a class defined in the ``textoutpc.Tags`` submodule and referenced
in the `_tags` array in ``textoutpc.Tags.__init__``. It usually takes a name
that starts with ``Textout`` and an uppercase character, and finishes by
``Tag``, and shall inherit one of the base classes defined in
``textoutpc.Tags.__base__`` depending on how the tag will be used:

- ``TextoutInlineTag``: tag to be used inside a paragraph,
  e.g. text formatting;
- ``TextoutBlockTag``: tag to be used at paragraph level, e.g. video.

There are a few public members you can define as a tag:

- ``aliases``: the array of names this tag can be accessed as.
  Basic tags (the ones with brackets ``[]``) are defined as ``[<name>]``
  (e.g. ``[hello]``) and special characters are defined with their symbol,
  e.g. ``\```;
- ``raw``: the tag's content shall not be interpreted, which is generally
  only useful when the content is preprocessed (see below). The default
  is ``False`` if there is no preprocess method, and `True` otherwise;
- ``generic``: the tag can be ended using the generic tag ending mark ``[/]``.
  It is defined as ``True`` by default for all tags;
- ``notempty``: ignore the tag when its content is empty. By default, this
  value is `False`;
- ``superblock``: is a super-block (for blocks) which means it adds a block
  level, and adds a paragraph tag implicitely.
- ``inlined``: if is a block, transforms automatically the surrounding block
  into a superblock while it's there.
- ``procvalue``: process the value as normal text before passing it.
- ``not_within_itself``: make that if a tag is opened within itself (depth
  included), the tag above and all tags below are closed first.
- ``expect_child``: make that all content below (without depth) that isn't
  within the specified tags is ignored.

So for example, if I want to make the inline tag ``[hello]`` as an example,
with the alternate name ``[hai]``, I'd start off by writing:

.. code-block:: python

	from .__base__ import *

	class TextoutHelloTag(TextoutInlineTag):
		""" The [hello] tag, which does things.
			Example uses:

			[hello]world[/hello]
			[hai=something]world[/hai] """

		aliases = ('[hello]', '[hai]')

		# ...

---------------------
Getting the arguments
---------------------

There are two methods the tag can define to get various parts of the user
input:

- ``prepare(name, value)``: the tag has been called, but the content has not
  yet been read — this method uses the name and the value to define the tag's
  behaviour. By default, when prepared, the tag does nothing;
- ``preprocess(content)``: the content has been read and the tag wants to know
  about it — this method uses the content to define the tag's behaviour.
  By default, the tag prints its content while reading it (instead of
  storing it for this method);
- ``default()``: the content is empty and the tag wants to know about it (this
  method is only called when ``preprocess()`` is not defined).

Both methods can raise an exception (whatever the exception is) if the tag
is called with invalid arguments; when this is the case, the tag is just
printed as is, e.g. in ``[color=;;]test[/color]``, the ``TextoutColorTag``
will return an exception at preparation, and the tag will be printed as is.

The ``prepare()`` and ``preprocess()`` method can be defined for given output
types (languages, e.g. ``html`` or ``lightscript``) by setting up
``<action>_<output type>()``-like methods. The ``preprocess()`` methods can
also be defined dynamically by the ``prepare()`` methods, as their existence
is checked after the preparation.

It is recommended to only use the ``preprocess()`` method when the tag is a
raw tag, and not to check if the content is empty or not, as the ``default()``
method is here to test this.

If the ``preprocess()`` method returns a modified content, this content will
be used instead of the original one (and will be escaped for output languages
such as HTML).

-----------------------
Defining the tag output
-----------------------

For each output type, there are three output methods the tag can define:

- ``begin()``: output what comes before the content, e.g. ``<b>``;
- ``content()``: output what comes instead of content, e.g. ``hello``;
- ``end()``: output what comes after the content, e.g. ``</b>``.

These methods are **not supposed** to modify any (not even internal) members
or methods, they are just supposed to output, although you can define
variables in ``begin()`` to be used in ``end()``.

As for ``prepare()`` and ``preprocess()``, these output methods can be defined
for given output types by appending ``_<output type>`` to the name, e.g.
``begin_html()``. They can also be defined dynamically by the ``prepare()``
and ``preprocess()`` methods.

A ``content()`` method without a ``preprocess()`` means that the content of
the tag in the user input will be ignored.

-------------------------------------
Defining internal members and methods
-------------------------------------

For all members and methods specific to the tag objects (except the ones
presented previously), it is recommended to use an underscore before the
name of the member or method, e.g. ``self._bold``.
