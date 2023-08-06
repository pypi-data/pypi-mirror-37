The textout BBcode markup language
==================================

The BBcode markup language mainly uses tags, which the starting mark looks
like ``[xxx]`` and the ending mark looks like ``[/xxx]``. You can add an
attribute to the starting mark to modify the tag's behaviour.

There is a generic/quick ending mark which looks like ``[/]``.
It cannot be used with all tags, so when it is used in the examples below,
suppose you can use it, otherwise, it might not be possible (or not
implemented yet).

--------------
Align the text
--------------

To align the text, you can use either ``[<alignment mode>]`` or
``[align=<alignment mode>]`` with any of the following modes:

- ``left``: the text is left-aligned;
- ``right``: the text is right-aligned;
- ``center``: the text is aligned at the horizontal middle of the document;
- ``justify``: the text is justified, i.e. the text spaces are optimized for
  the right'n'word to end at the right of the line.

For example, to right-align some text, you could do something like this:

.. code::

	[right]some text[/]

----------------
Inserting titles
----------------

Do you want to include titles or subtitles to your message, integrated with
the website's design? Use the ``[title]`` and ``[subtitle]`` tags for that:

.. code::

	[title]Just do it![/]
	[subtitle]Don't let your dreams be dreams![/]

Notice that this tag cannot embed another tag.

----------------
Styling the text
----------------

You can add some basic text style by using the following tags:

- ``[b]`` for **bold** text;
- ``[i]`` for *italic* text;
- ``[u]`` for underlined text;
- ``[o]`` for overlined text;
- ``[s]`` or ``[strike]`` for striked text.

They can all be ended with the generic ending mark ``[/]``.

----------------------
Changing the text font
----------------------

You can change the font of the text by using the ``[font=xxx]`` (or ``[xxx]``
directly, where ``xxx`` represents the font identifier) tag. The following
fonts are available:

- ``arial`` represents Arial;
- ``comic`` represents Comic MS;
- ``tahoma`` represents Tahoma;
- ``courier`` represents Courier;
- ``haettenschweiler`` represents Haettenschweiler;
- ``mono`` and ``monospace`` represents the basic monospace font.

They can be ended with the generic ending mark ``[/]`` as well.

-----------------------
Changing the text color
-----------------------

You can change the color of the text using the ``[color=xxx]`` (or ``[xxx]``
directly for simple colors, where ``xxx`` represents the color) tag. This
tag accepts several types of values:

- simple color names (`inspired from CSS <CSS named colors_>`_) such as
  ``red``, ``blue``, ``green``, ``transparent``;
- color hex codes using a hash (``#``) followed by hex digits, e.g.
  ``#01020F``, where the first group of hex digits represents the
  red component from 0 to 255, the second group of hex digits represents
  the green component from 0 to 255, and the third group of hex digits
  represents the blue component from 0 to 255.
  Incomplete composites will be filled by zero on the left (e.g. ``#0000F``
  is equivalent to ``#00000F``), invalid characters such as ``A`` will be
  replaced by ``0``s;
- three hex digits codes using ``#`` followed by three hex digits, e.g.
  ``#123`` which will be translated to ``#112233``;
- ``rgb(<red>, <green>, <blue>)``, where the red, green and blue components
  are represented using decimal digits and are between 0 and 255 included;
- ``rgba(<red>, <green>, <blue>, <alpha>)``, where the red, green and blue
  components are expressed as said before and the alpha component is either
  expressed as a percentage (e.g. ``12.34%``) or as a proportion between
  ``0.0`` and ``1.0``;
- ``hsl(<hue>, <saturation>, <light>)`` or
  ``hls(<hue>, <light>,<saturation>)``;
- ``hsl(<hue>, <saturation>, <light>, <alpha>)`` or
  ``hls(<hue>, <light>, <saturation>, <alpha>)``;
- ``hwb(<hue>, <white proportion>, <black proportion>)``.

Here are some examples:

.. code::

	[blue]I'm blue![/]
	[color=#ff69b4]That color is called “Cuisse de Nymphe émue”![/]
	[color=rgb(255, 255,255,0.4)]I'm black![/]
	[color=hsl(0,100%, 0.5)]I'm red![/]

--------------------
Inserting hyperlinks
--------------------

Creating hyperlinks on a bunch of text is possible through the ``[url]`` tag.
The URL has to be either absolute, relative, or related to an anchor. It has
to be passed to the tag either through the argument (which allows the content
to be the displayed title of the link) or through the content if there is
no argument. By default, if there is no content and an argument, the argument
will be taken as the link title.

Here are examples:

.. code::

	[url]https://planet-casio.com[/]
	[url=https://planet-casio.com]Planète Casio[/]
	[url=/relative/url.html][/]

For links to profiles, the ``[profil]`` and ``[profile]`` tags can be used.
They take no attribute but take a content which is the user whose the profile
is to be linked's name. For example:

.. code::

	[profil]Cakeisalie5[/]

For links to topics and tutorials, the ``[topic]`` and ``[tutorial]``
tags can be used. They take no attribute but take a content which is the
identifier of the topic or tutorial to which to link to.
For example:

.. code::

	[topic]234[/]
	[tutorial]32[/]

For links to programs, the ``[program]`` and ``[prog]`` tags can be used.
They take no attribute but take a content which is the identifier of the
program to which to link to. For example:

.. code::

	[program]3598[/program]

---------------
Quoting someone
---------------

To quote someone visually, you can use the ``[quote]`` tag, which takes the
name of the person you're quoting as the attribute and the quote as the
content. A quote can contain another one, of course. If there is no name,
the display will just be generalistic.

Here are examples:

.. code::

	[quote]Someone said that.[/]
	[quote=Cakeisalie5]Ever realized that my name contained “Cake”?[/]

-------------------------
Spoilers/Content Warnings
-------------------------

To hide something behind a deliberate action of your user, usually to avoid
hurting people or to hide the solution to a problem, you can use the
``[spoiler]`` tag.

.. code::

	[spoiler]This is hidden![/]
	[spoiler=Uncover the dark secrets of the night]Boo![/]
	[spoiler=Uncover this!|Cover this quick!!]BOOO![/]

---------------
Presenting code
---------------

There are two code tags:

- ``[code]``, which is supposed to be used as a block for multiline code or
  to isolate the code from the text;
- ``[inlinecode]`` or the *backquotes* to include code in the text.

For example:

.. code::

	[code]Some multiline code, with [center]tags shown as they are[/center].
	Incredible, heh?[/code]
	[inlinecode]Some inline code.[/inlinecode]
	`Some more inline code.`

------------------
Inserting an image
------------------

In order to insert an image, you will have to use the ``[img]`` tag. It will
make a new paragraph containing the image which the URL is given in the
tag content. The tag can be bundled with some attributes, separated with
the pipe (``|``) character:

- ``<width>x<height>``: set the dimensions to the image. If the width isn't
  given (i.e. if this attribute starts with ``x``), the height will be set
  automatically. If the height isn't given (i.e. no ``x`` or nothing after
  the ``x``), the width will be set automatically;
- ``left``, ``right``, ``center``: align the image accordingly;
- ``float``: make the image float, i.e. let the text be where the image isn't.

For example:

.. code::

	[img=right|float|x24]https://example.org/image.jpg[/]

is a right-aligned image, floating (which means text will be allowed on
the left of the image), and with a height of 24 pixels and an automatic
width.

Planète Casio admins can use the ``[adimg]`` tag which is equivalent to the
``[img]`` tag but adds the special admin image folder prefix to the image
URLs, so this is possible:

.. code::

	[adimg]incredible.jpg[/]

-----------------
Inserting a video
-----------------

This BBcode translator has the ability to integrate videos from some online
platforms into your message, as a block. To do this, you can use the
``[video]`` and ``[video tiny]`` tags. For example:

.. code::

	[video]https://www.youtube.com/watch?v=yhXpV8hRKxQ[/]
	[video tiny]https://www.youtube.com/watch?v=yhXpV8hRKxQ[/]

------------------------
Inserting a progress bar
------------------------

Do you want to present how your project is evolving using a simple graph,
the progress bar? This is possible using the ``[progress]`` tag, which takes
the percentage (between 0 and 100 included) of the advancement as its
attribute. For example:

.. code::

	[progress=50]Building a great wall…[/]
	[progress=100][/]

----------------------------
Inserting labels and targets
----------------------------

Is your message in several parts and you only want to link one without using
an entire separate page for the section? This is the tag you might want
to use. To link to a point in your message:

- first, define the label using the ``[label]`` tag, with the name of the
  label as the attribute;
- then link to the label using the ``[target]`` tag.

You are not obliged to terminate the ``[label]`` tag (the original version of
it didn't support the ``[label]`` tag termination, in fact). For example:

.. code::

	[label=sometag][subtitle]Some chapter[/subtitle]

	...

	[target=sometag]Go back to the beginning of the chapter[/]

.. _CSS named colors: https://drafts.csswg.org/css-color/#named-colors
