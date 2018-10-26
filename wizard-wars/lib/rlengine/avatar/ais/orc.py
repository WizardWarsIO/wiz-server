from ai import *
from ... import libtcodpy as libtcod
from random import randint

class OrcAI(AIControls):
  def defaultName(self):
    return 'The Orc'

  def friendlies(self):
    return ['imp']

  def health(self):
    return 25

  def race(self):
    return 'orc'

  def renderCode(self):
    return 130

  def basePower(self):
    return {'direct':5, 'swipe': 1}

  def baseDefense(self):
    return {'direct': 2, 'swipe': 0}