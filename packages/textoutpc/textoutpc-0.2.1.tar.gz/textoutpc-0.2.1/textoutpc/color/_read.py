#!/usr/bin/env python3
#******************************************************************************
# Copyright (C) 2018 Thomas "Cakeisalie5" Touhey <thomas@touhey.fr>
# This file is part of the textoutpc project, which is MIT-licensed.
#******************************************************************************
""" HTML/CSS like color parsing, mainly for the `[color]` tag.
	Defines the `get_color()` function which returns an rgba value.
"""

import re as _re
import math as _math

from ._named import colors as _named_colors
from ._sys import hls_to_rgb as _hls_to_rgb, hwb_to_rgb as _hwb_to_rgb

__all__ = ["get_color"]

_cr = _re.compile("""
	rgba?\s*\(
		\s* (?P<rgb_r>[0-9]{1,3}) \s* ([,\\s]
		\s* (?P<rgb_g>[0-9]{1,3}) \s* ([,\\s]
		\s* (?P<rgb_b>[0-9]{1,3}) \s* ([,\\s]
		\s* ((?P<rgb_a_per> ([0-9]+\.?|[0-9]*\.[0-9]+) ) \s*%
			|(?P<rgb_a_flt> (0*[01]\.?|0*\.[0-9]+) )) \s*
		)?)?)?
	\)|
	hsla?\s*\(
		\s* (?P<hsl_hue>-? ([0-9]+\.?|[0-9]*\.[0-9]+) )
			(?P<hsl_agl>deg|grad|rad|turn|) \s*[,\\s]
		\s* ((?P<hsl_sat_per> ([0-9]+\.?|[0-9]*\.[0-9]+) ) \s*%
			|(?P<hsl_sat_flt> (0*[01]\.?|0*\.[0-9]+) )) \s*[,\\s]
		\s* ((?P<hsl_lgt_per> ([0-9]+\.?|[0-9]*\.[0-9]+) ) \s*%
			|(?P<hsl_lgt_flt> (0*[01]\.?|0*\.[0-9]+) )) \s*([,\\s/]
		\s* ((?P<hsl_aph_per> ([0-9]+\.?|[0-9]*\.[0-9]+) ) \s*%
			|(?P<hsl_aph_flt> (0*[01]\.?|0*\.[0-9]+) )) \s*
		)?
	\)|
	hlsa?\s*\(
		\s* (?P<hls_hue>-? ([0-9]+\.?|[0-9]*\.[0-9]+) )
			(?P<hls_agl>deg|grad|rad|turn|) \s*[,\\s]
		\s* ((?P<hls_lgt_per> ([0-9]+\.?|[0-9]*\.[0-9]+) ) \s*%
			|(?P<hls_lgt_flt> (0*[01]\.?|0*\.[0-9]+) )) \s*[,\\s]
		\s* ((?P<hls_sat_per> ([0-9]+\.?|[0-9]*\.[0-9]+) ) \s*%
			|(?P<hls_sat_flt> (0*[01]\.?|0*\.[0-9]+) )) \s*([,\\s/]
		\s* ((?P<hls_aph_per> ([0-9]+\.?|[0-9]*\.[0-9]+) ) \s*%
			|(?P<hls_aph_flt> (0*[01]\.?|0*\.[0-9]+) )) \s*)?
	\)|
	hwb\s*\(
		\s* (?P<hwb_hue>-? ([0-9]+\.?|[0-9]*\.[0-9]+) )
			(?P<hwb_agl>deg|grad|rad|turn|) \s*[,\\s]
		\s* ((?P<hwb_wht_per> ([0-9]+\.?|[0-9]*\.[0-9]+) ) \s*%
			|(?P<hwb_wht_flt> (0*[01]\.?|0*\.[0-9]+) )) \s*[,\\s]
		\s* ((?P<hwb_blk_per> ([0-9]+\.?|[0-9]*\.[0-9]+) ) \s*%
			|(?P<hwb_blk_flt> (0*[01]\.?|0*\.[0-9]+) )) \s*([,\\s/]
		\s* ((?P<hwb_aph_per> ([0-9]+\.?|[0-9]*\.[0-9]+) ) \s*%
			|(?P<hwb_aph_flt> (0*[01]\.?|0*\.[0-9]+) )) \s*)?
	\)|
		\# (?P<hex_digits> [0-9a-f]+)
	|
		(?P<legacy_chars> [0-9a-z]+)
""", _re.VERBOSE | _re.I | _re.M)

def get_color(value):
	""" Get a color from a string.
		Returns an (r, g, b, a) color.
		Raises an exception if the color could not be read. """

	# Check if is a color name.
	value = value.strip()
	try:    value = _named_colors[value.lower()]
	except: pass

	# Initialize the alpha.

	alpha = 1.0

	# Get the match.

	match = _cr.fullmatch(value)
	if not match:
		raise ValueError("invalid color string")

	match = match.groupdict()

	if   match['hex_digits'] or match['legacy_chars']:
		# Imitate the Netscape behaviour. Find more about this here:
		# https://stackoverflow.com/a/8333464
		#
		# I've also extended the thing as I could to introduce more
		# modern syntaxes described on the dedicated MDN page:
		# https://developer.mozilla.org/en-US/docs/Web/CSS/color_value
		#
		# First of all, depending on our source, we will act differently:
		# - if we are using the `hex_digits` source, then we use the modern
		#   behaviour and do the fancy things such as `#ABC -> #AABBCC`
		#   management and possible alpha decoding;
		# - if we are using the `legacy_chars` source, then we sanitize our
		#   input by replacing invalid characters by '0' characters (the
		#   0xFFFF limit is due to how UTF-16 was managed at the time).
		#   We shall also truncate our input to 128 characters.
		#
		# After these sanitization options, we will keep the same method as
		# for legacy color decoding. It should work and be tolerant enough…

		members = 3
		if match['hex_digits']:
			hx = match['hex_digits'].lower()

			# RGB and RGBA (3 and 4 char.) notations.
			if len(hx) in (3, 4):
				hx = hx[0:1] * 2 + hx[1:2] * 2 + hx[2:3] * 2 + hx[3:4] * 2

			# Check if there is transparency or not.
			if len(hx) % 3 != 0 and len(hx) % 4 == 0:
				members = 4

		else: # our source is `legacy_chars`
			hx = match['legacy_chars'].lower()
			hx = ''.join(c if c in '0123456789abcdef' \
				else ('0', '00')[ord(c) > 0xFFFF] for c in hx[:128])[:128]

		# First, calculate some values we're going to need.
		# `iv` is the size of the zone for a member.
		# `sz` is the size of the digits slice to take in that zone (max. 8).
		# `of` is the offset in the zone of the slice to take.

		iv = _math.ceil(len(hx) / members)
		of = iv - 8 if iv > 8 else 0
		sz = iv - of

		# Then isolate the slices using the values calculated above.
		# `gr` will be an array of 3 or 4 digit strings (depending on the
		# number of members).

		gr = list(map(lambda i: hx[i * iv + of:i * iv + iv] \
			.ljust(sz, '0'), range(members)))

		# Check how many digits we can skip at the beginning of each slice.

		pre = min(map(lambda x: len(x) - len(x.lstrip('0')), gr))
		pre = min(pre, sz - 2)

		# Then extract the values.

		it = map(lambda x: int('0' + x[pre:pre + 2], 16), gr)
		if members == 3:
			r, g, b = it
		else:
			r, g, b, alpha = it
			alpha /= 255.0
	elif match['rgb_r']:
		# Extract the values.

		r = int(match['rgb_r'])
		g = int(match['rgb_g']) if match['rgb_g'] else 0
		b = int(match['rgb_b']) if match['rgb_b'] else 0

		if   match['rgb_a_per']:
			alpha = float(match['rgb_a_per']) / 100.0
		elif match['rgb_a_flt']:
			alpha = float(match['rgb_a_flt'])
	elif match['hsl_hue'] or match['hls_hue']:
		# Extract the values.

		if match['hsl_hue']:
			hue = float(match['hsl_hue'])
			agl = match['hsl_agl']

			# Saturation.
			if match['hsl_sat_per']:
				sat = float(match['hsl_sat_per']) / 100.0
			else:
				sat = float(match['hsl_sat_flt'])
				if sat > 1.0:
					sat /= 100.0

			# Light.
			if match['hsl_lgt_per']:
				lgt = float(match['hsl_lgt_per']) / 100.0
			else:
				lgt = float(match['hsl_lgt_flt'])
				if lgt > 1.0:
					lgt /= 100.0

			# Alpha value.
			if   match['hsl_aph_per']:
				alpha = float(match['hsl_aph_per']) / 100.0
			elif match['hsl_aph_flt']:
				alpha = float(match['hsl_aph_flt'])
		else:
			hue = float(match['hls_hue'])
			agl = match['hls_agl']

			# Saturation.
			if match['hls_sat_per']:
				sat = float(match['hls_sat_per']) / 100.0
			else:
				sat = float(match['hls_sat_flt'])

			# Light.
			if match['hls_lgt_per']:
				lgt = float(match['hls_lgt_per']) / 100.0
			else:
				lgt = float(match['hls_lgt_flt'])

			# Alpha value.
			if   match['hls_aph_per']:
				alpha = float(match['hls_aph_per']) / 100.0
			elif match['hls_aph_flt']:
				alpha = float(match['hls_aph_flt'])

		# Prepare the angle.
		if   agl == 'grad':
			hue = hue * 400.0
		elif agl == 'rad':
			hue = hue / (2 * _math.pi)
		elif not agl or agl == 'deg':
			hue = hue / 360.0
		hue = hue % 1.0

		if sat > 1 or lgt > 1:
			raise Exception

		r, g, b = _hls_to_rgb(hue, lgt, sat)
		r, g, b = map(lambda x:int(round(x * 255)), (r, g, b))
	elif match['hwb_hue']:
		hue = float(match['hwb_hue'])
		agl = match['hwb_agl']

		# Prepare the angle.
		if   agl == 'grad':
			hue = hue * 400.0
		elif agl == 'rad':
			hue = hue / (2 * _math.pi)
		elif not agl or agl == 'deg':
			hue = hue / 360.0
		hue = hue % 1.0

		# Saturation.
		if match['hwb_wht_per']:
			wht = float(match['hwb_wht_per']) / 100.0
		else:
			wht = float(match['hwb_wht_flt'])

		# Light.
		if match['hwb_blk_per']:
			blk = float(match['hwb_blk_per']) / 100.0
		else:
			blk = float(match['hwb_blk_flt'])

		if wht > 1 or blk > 1:
			raise Exception
		r, g, b = _hwb_to_rgb(hue, wht, blk)
		r, g, b = map(lambda x: int(round(x * 255)), (r, g, b))

	if r < 0 or r > 255 or g < 0 or g > 255 or b < 0 or b > 255:
		raise ValueError("invalid color string")
	if alpha < 0.0 or alpha > 1.0:
		raise ValueError("invalid color string")
	alpha = round(alpha, 4)

	return (r, g, b, alpha)

# End of file.
