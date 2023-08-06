Welcome to textoutpc's documentation!
=====================================

textoutpc is a BBcode markup language translator project for `Planète Casio`_.

BBcode has been invented in the 90s/2000s for bulletin board systems.
It has been implemented in `Planète Casio`_ during its first years (although
some research has to be made on how that choice was done…).

On `Planète Casio`_, which is coded in PHP at the time I'm writing this,
we have our own custom version of BBcode, which we pass through an internal
utility named ``textout()``.

I, Thomas “Cakeisalie5” Touhey, rewrote it recently, and it works pretty well
while being secure, but as the next version of `Planète Casio`_ (the ”v5”)
will be written from scratch, I figured out I could rewrite the ``textout()``
utility in Python, and improve the language parsing to be more practical and
add features that are in the original BBcode markup language.

As this is a rewrite, the vulnerabilities and bug will not be common to this
project and the online version of the transcoder.

.. toctree::
	:maxdepth: 2
	:caption: Contents:

	language
	usage
	tags

.. _Planète Casio: https://www.planet-casio.com/Fr/
