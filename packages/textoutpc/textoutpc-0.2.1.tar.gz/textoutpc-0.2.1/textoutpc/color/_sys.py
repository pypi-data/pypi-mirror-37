#!/usr/bin/env python3
#******************************************************************************
# Copyright (C) 2018 Thomas "Cakeisalie5" Touhey <thomas@touhey.fr>
# This file is part of the textoutpc project, which is MIT-licensed.
#******************************************************************************
""" Conversions between color systems. """

from colorsys import hls_to_rgb

__all__ = ["hls_to_rgb", "hwb_to_rgb"]

def hwb_to_rgb(hue, w, b):
	""" Convert HWB to RGB color.
		https://drafts.csswg.org/css-color/#hwb-to-rgb """

	r, g, b = hls_to_rgb(hue, 0.5, 1.0)
	f = lambda x: x * (1 - w - b) + w
	r, g, b = f(r), f(g), f(b)

	return r, g, b

# End of file.
