#!/usr/bin/env python3
#******************************************************************************
# Copyright (C) 2018 Thomas "Cakeisalie5" Touhey <thomas@touhey.fr>
# This file is part of the textoutpc project, which is MIT-licensed.
#******************************************************************************
""" Unit tests for the Python version of textout.
	Uses the builtin `unittest` module.
"""

import unittest as _unittest

__all__ = ["TextoutHTMLTest"]

# Define the tests.

__test_cases = {
	# Basic text.
	'': '',
	'lol': '<p>lol</p>',
	'<script>alert(1);</script>': \
		'<p>&lt;script&gt;alert(1);&lt;/script&gt;</p>',

	# Other tests. (?)
	'[a][c][/a]': '<p>[a][c][/a]</p>',
	'[a][a]': '<p>[a][a]</p>',
	"[<>]><[/<>]": "<p>[&lt;&gt;]&gt;&lt;[/&lt;&gt;]</p>",

	# Autolinking.
	'(http://www.example.org/some-[damn-url]-(youknow))': \
		'<p>(<a href="http://www.example.org/some-[damn-url]-(youknow)">' \
		'http://www.example.org/some-[damn-url]-(youknow)</a>)</p>',
	'https://thomas.touhey.fr/, tu vois ?': \
		'<p><a href="https://thomas.touhey.fr/">https://thomas.touhey.fr/' \
		'</a>, tu vois ?</p>',

	# Basic text styling.
	'[u][b][a][i][/b]': "<p><u><b>[a]</b></u></p>",
	'[u][b]a[/]mdr': '<p><u><b>a</b>mdr</u></p>',

	# Blocks, alignment.
	'[left]': '',
	'[left]lol[/]hi': '<div class="align-left"><p>lol</p></div><p>hi</p>',
	'a[justify]b': '<p>a</p><div class="align-justify"><p>b</p></div>',
	'a[i]': '<p>a</p>',
	'a[i][justify]b': '<p>a</p>' \
		'<div class="align-justify"><p><i>b</i></p></div>',
	'a[i]k[center]b': '<p>a<i>k</i></p>' \
		'<div class="align-center"><p><i>b</i></p></div>',
	'a[i]k[center][b]b[justify]c[/center]d[/]wouhou': \
		'<p>a<i>k</i></p>' \
		'<div class="align-center"><p><i><b>b</b></i></p>' \
		'<div class="align-justify"><p><i><b>c</b></i></p></div></div>' \
		'<p><i>d</i>wouhou</p>',

	# Show tag for super preprocessing blocks.
	'[show]lol': '<p><span class="inline-code">lol</span></p>',
	'[quote][show][justify]hehe': \
		'<div class="citation"><p><span class="inline-code">' \
		'&lt;div class=&quot;align-justify&quot;&gt;' \
		'&lt;p&gt;hehe&lt;/p&gt;&lt;/div&gt;' \
		'</span></p></div>',

	# Titles.
	'lolk[title]smth': '<p>lolk</p>' '<h1 class="title">smth</h1>',
	'[subtitle]<>': '<h2 class="subtitle">&lt;&gt;</h2>',

	# Fonts.
	'[arial]test': '<p><span style="font-family: arial">test</span></p>',
	'[font=mono]stereo': \
		'<p><span style="font-family: monospace">stereo</span></p>',
	'[haettenschweiler]': '',
	'[font=hello]yea': '<p>[font=hello]yea</p>',

	# Color.
	'yea[color=blue]dabadee': \
		'<p>yea<span style="color: #0000FF">dabadee</span></p>',
	'[color=#12345F]a': '<p><span style="color: #12345F">a</span></p>',
	'[color=#123]a': '<p><span style="color: #112233">a</span></p>',
	'[color=123]a': '<p><span style="color: #010203">a</span></p>',
	'[color=chucknorris]a': '<p><span style="color: #C00000">a</span></p>',
	'[color=rgb(1, 22,242)]a': '<p><span style="color: #0116F2">a</span></p>',
	'[color= rgb (1,22, 242 , 50.0% )]a': '<p><span style="color: #0116F2; ' \
		'color: rgba(1, 22, 242, 0.5)">a</span></p>',
	'[color=rgba(1,22,242,0.500)]a': '<p><span style="color: #0116F2; ' \
		'color: rgba(1, 22, 242, 0.5)">a</span></p>',
	'[color=hsl(0, 1,50.0%)]r': '<p><span style="color: #FF0000">r</span></p>',
	# TODO: hls, hwb

	# Links.
	'[url]': '<p>[url]</p>',
	'[url=https://thomas.touhey.fr/]mon profil est le meilleur[/url]':
		'<p><a href="https://thomas.touhey.fr/">mon profil est le meilleur' \
		'</a></p>',
	'[url=https://thomas.touhey.fr/]': \
		'<p><a href="https://thomas.touhey.fr/">https://thomas.touhey.fr/' \
		'</a></p>',
	'[url=http://hey.org/lol[]>"a]': '<p><a href="http://hey.org/lol[]&gt;' \
		'&quot;a">' \
		'http://hey.org/lol[]&gt;&quot;a</a></p>',
	'[url]javascript:alert(1)[/url]': '<p>[url]javascript:alert(1)[/url]</p>',
	'[url]<script>alert(1);</script>[/url]': \
		'<p>[url]&lt;script&gt;alert(1);&lt;/script&gt;[/url]</p>',

	'[profil]cake[/profil]': \
		'<p><a href="https://www.planet-casio.com/Fr/compte/voir_profil.php' \
		'?membre=cake">cake</a></p>',
	'[profile]ekac': \
		'<p><a href="https://www.planet-casio.com/Fr/compte/voir_profil.php' \
		'?membre=ekac">ekac</a></p>',

	# Quotes.
	'[quote]': '',
	'[quote]a': \
		'<div class="citation"><p>a</p></div>',
	'[quote=Test 1 :)]lel[/quote]': \
		'<div class="citation"><p><b>Test 1 ' \
		'<img src="/images/smileys/smile.gif"> a écrit :</b></p><p>' \
		'lel</p></div>',

	# Spoilers.
	'[spoiler]': '',
	'[spoiler=Hello|world> :D]Close this, quick![/spoiler]': \
		'<div class="spoiler"><div class="title on" ' \
		'onclick="toggleSpoiler(this.parentNode, ' "'open'" ');"><p>Hello' \
		'</p></div><div class="title off" ' \
		'onclick="toggleSpoiler(this.parentNode, ' "'close'" ');"><p>world' \
		'&gt; <img src="/images/smileys/grin.gif"></p></div>' \
		'<div class="off"><p>Close this, quick!</p></div></div>',

	# Code.
	'[code]': '',
	"`[code]`": '<p><span class="inline-code">[code]</span></p>',

	'[inlinecode]': '',
	"[inlinecode]`[/inlinecode]": '<p><span class="inline-code">`</span></p>',

	"[b]a[noeval]b[/b]c[/noeval]d": "<p><b>ab[/b]cd</b></p>",
	"a[noeval]b[noeval]c[/noeval]d[/noeval]e": "<p>ab[noeval]c[/noeval]de</p>",
	"[noeval]``[/noeval]": "<p>``</p>",
	'[noeval]<>[/noeval]': '<p>&lt;&gt;</p>',

	# Pictures.
	'[img]': '<p>[img]</p>',
	'[img]"incroyable<>"[/img]': \
		'<p>[img]&quot;incroyable&lt;&gt;&quot;[/img]</p>',
	'[img=right|float|12x345]https://example.org/image.png': \
		'<img src="https://example.org/image.png" class="img-float-right" ' \
		'style="width: 12px; height: 345px" />',

	# Videos.
	'[video]"><script>alert(1)</script>[/video]': \
		'<p>[video]&quot;&gt;&lt;script&gt;alert(1)&lt;/script&gt;' \
		'[/video]</p>',
	'[video]<script>alert(document.cookie)</script>[/video]': \
		'<p>[video]&lt;script&gt;alert(document.cookie)&lt;/script&gt;' \
		'[/video]</p>',
	'[video]https://www.youtube.com/watch?v=6odDOOyUawY[/video]': \
		'<div class="video-wrapper" style="padding-bottom: 56.25%"><iframe ' \
		'src="https://www.youtube.com/embed/6odDOOyUawY" ' \
		'frameborder="0" allowfullscreen></iframe></div>',
	'[video]https://www.youtube.com/watch?v=<script>alert(1)</script>': \
		'<p><a href="https://www.youtube.com/watch?v=&lt;script&gt;alert(1)' \
		'&lt;/script&gt;">' \
		'https://www.youtube.com/watch?v=&lt;script&gt;alert(1)' \
		'&lt;/script&gt;</a></p>',
	'[video=left|float|4:3]https://www.youtube.com/watch?v=XEjLoHdbVeE': \
		'<div class="video-wrapper img-float-left" ' \
		'style="padding-bottom: 75%"><iframe ' \
		'src="https://www.youtube.com/embed/XEjLoHdbVeE" frameborder="0" ' \
		'allowfullscreen></iframe></div>',
	'lol[youtube]h4WLX8hfpJw': '<p>lol</p><div class="video-wrapper" ' \
		'style="padding-bottom: 56.25%"><iframe ' \
		'src="https://www.youtube.com/embed/h4WLX8hfpJw" frameborder="0" ' \
		'allowfullscreen></iframe></div>',

	# Progress bars.
	'[progress=lol]mdr[/progress]': '<p>[progress=lol]mdr[/progress]</p>',

	# Text rotation obfuscation.
	'[rot13]obawbhe[/rot13]': '<p>bonjour</p>',

	# Lists.
	'[list]haha[b][*]wow[*]incredible[/b][/*]wow[*]yuy[/list]': \
		'<ul><li>wow</li><li>incredible[/b]</li><li>yuy</li></ul>',

	# Smileys.
	':)': '<p><img src="/images/smileys/smile.gif"></p>',
	':):)': '<p>:):)</p>',
	':) :D': '<p><img src="/images/smileys/smile.gif"> ' \
		'<img src="/images/smileys/grin.gif"></p>',
}

# Define the tests wrapper, and define the classes.

_cnt = 0
_len = len(str(len(__test_cases)))
_templ = """\
  def test_html{n:0>{l}}(self):
    import textoutpc as _textoutpc
    self.assertEqual(_textoutpc.tohtml({i}), {r}, \\
    	"for the following text: " + {i})
"""

def _wrap_test(inp, res):
	global _cnt

	_cnt += 1
	return _templ.format(n = _cnt, l = _len, i = repr(inp), r = repr(res))

exec("class TextoutHTMLTest(_unittest.TestCase):\n  maxDiff = None\n" + \
	'\n'.join(map(lambda args: _wrap_test(*args), __test_cases.items())),
	globals())

# If run as main script, run the test function.

if __name__ == '__main__':
	_unittest.main()

# End of file.
