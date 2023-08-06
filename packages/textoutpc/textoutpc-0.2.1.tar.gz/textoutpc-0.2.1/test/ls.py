#!/usr/bin/env python3
#******************************************************************************
# Copyright (C) 2018 Thomas "Cakeisalie5" Touhey <thomas@touhey.fr>
# This file is part of the textoutpc project, which is MIT-licensed.
#******************************************************************************
""" Unit tests for the Python version of textout, lightscript-related funcs.
	Uses the builtin `unittest` module.
"""

import unittest as _unittest

__all__ = ["TextoutLSTest"]

# Define the tests.

__test_cases = {
	# Basic text.

	'': '',
}

# Define the tests wrapper, and define the classes.

_cnt = 0
_len = len(str(len(__test_cases)))
_templ = """\
  def test_lgsp{n:0>{l}}(self):
    import textoutpc as _textoutpc
    self.assertEqual(_textoutpc.tolightscript({i}), {r}, {i})
"""

def _wrap_test(inp, res):
	global _cnt

	_cnt += 1
	return _templ.format(n = _cnt, l = _len, i = repr(inp), r = repr(res))

exec("class TextoutLSTest(_unittest.TestCase):\n  maxDiff = None\n" + \
	'\n'.join(map(lambda args: _wrap_test(*args), __test_cases.items())),
	globals())

# If run as main script, run the test function.

if __name__ == '__main__':
	_unittest.main()

# End of file.
