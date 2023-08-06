#!/usr/bin/env python3
#******************************************************************************
# Copyright (C) 2018 Thomas "Cakeisalie5" Touhey <thomas@touhey.fr>
# This file is part of the textoutpc project, which is MIT-licensed.
#******************************************************************************

from .. import Smiley as _Smiley

__all__ = ["TwistedSmiley", "EvilSmiley", "SmileSmiley", "WinkSmiley",
	"SadSmiley", "GrinSmiley", "HeheSmiley", "CoolSmiley", "Cool2Smiley",
	"MadSmiley", "EekSmiley", "MrGreenSmiley", "ShockedSmiley",
	"ConfusedSmiley", "EyebrowsSmiley", "CrySmiley", "LolSmiley",
	"SorrySmiley", "RollEyesSmiley", "WazaSmiley", "HereSmiley",
	"BowSmiley", "GoodSmiley", "LoveSmiley", "OuchSmiley", "FacepalmSmiley",
	"InsultsSmiley", "WhatSmiley", "ExclSmiley"]

_prefix = '/images/smileys/'


class TwistedSmiley(_Smiley):
	aliases = ('>:)',)
	url = _prefix + 'twisted.gif'


class EvilSmiley(_Smiley):
	aliases = ('>:(', ':grr:')
	url = _prefix + 'evil.gif'


class SmileSmiley(_Smiley):
	aliases = (':)',)
	url = _prefix + 'smile.gif'


class WinkSmiley(_Smiley):
	aliases = (';)',)
	url = _prefix + 'wink.gif'


class SadSmiley(_Smiley):
	aliases = (':(',)
	url = _prefix + 'sad.gif'


class GrinSmiley(_Smiley):
	aliases = (':D', ':grin:')
	url = _prefix + 'grin.gif'


class HeheSmiley(_Smiley):
	aliases = (':p',)
	url = _prefix + 'hehe.gif'


class CoolSmiley(_Smiley):
	aliases = (':cool:',)
	url = _prefix + 'cool.gif'


class Cool2Smiley(_Smiley):
	aliases = ('8-)',)
	url = _prefix + 'cool2.gif'


class MadSmiley(_Smiley):
	aliases = (':@',)
	url = _prefix + 'mad.gif'


class EekSmiley(_Smiley):
	aliases = ('0_0',)
	url = _prefix + 'eek.gif'


class MrGreenSmiley(_Smiley):
	aliases = (':E', ':mrgreen:')
	url = _prefix + 'mrgreen.gif'


class ShockedSmiley(_Smiley):
	aliases = (':O',)
	url = _prefix + 'shocked.gif'


class ConfusedSmiley(_Smiley):
	aliases = (':s', ':oops:')
	url = _prefix + 'confused2.gif'


class EyebrowsSmiley(_Smiley):
	aliases = ('^^',)
	url = _prefix + 'eyebrows.gif'


class CrySmiley(_Smiley):
	aliases = (":'(", ":cry:")
	url = _prefix + 'cry.gif'


# FIXME
#class WhistleSmiley(_Smiley):
#	aliases = (":-°", ':whistle:')
#	url = _prefix + 'whistle.gif'
#	height = '15px'


class LolSmiley(_Smiley):
	aliases = (":lol:",)
	url = _prefix + 'lol.gif'


class SorrySmiley(_Smiley):
	aliases = (":sry:",)
	url = _prefix + 'redface.gif'


class RollEyesSmiley(_Smiley):
	aliases = (":mmm:",)
	url = _prefix + 'rolleyes.gif'


class WazaSmiley(_Smiley):
	aliases = (":waza:",)
	url = _prefix + 'waza.gif'


class HereSmiley(_Smiley):
	aliases = (":here:", ":arrow:")
	url = _prefix + 'pointer.gif'


class BowSmiley(_Smiley):
	aliases = (":bow:",)
	url = _prefix + 'bow.gif'


class GoodSmiley(_Smiley):
	aliases = (":good:",)
	url = _prefix + 'welldone.gif'


class LoveSmiley(_Smiley):
	aliases = (":love:",)
	url = _prefix + 'love.gif'


class OuchSmiley(_Smiley):
	aliases = (":aie:",)
	url = _prefix + 'banghead2.gif'


class FacepalmSmiley(_Smiley):
	aliases = (":facepalm:",)
	url = _prefix + 'facepalm.gif'


class InsultsSmiley(_Smiley):
	aliases = (":argh:",)
	url = _prefix + 'insults.gif'


class WhatSmiley(_Smiley):
	aliases = (":?:",)
	url = _prefix + 'what.gif'


class ExclSmiley(_Smiley):
	aliases = (":!:",)
	url = _prefix + 'excl.gif'

# End of file.
