#!/usr/bin/env python3
#******************************************************************************
# Copyright (C) 2018 Thomas "Cakeisalie5" Touhey <thomas@touhey.fr>
# This file is part of the textoutpc project, which is MIT-licensed.
#******************************************************************************
""" HTML/CSS-like color parsing, mainly for the `[color]` tag.
	Defines the `get_color()` function which returns an rgba value.

	The functions in this module do not aim at being totally compliant with
	the W3C standards, although it is inspired from it.
"""

from ._read import get_color

# End of file.
