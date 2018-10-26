from wand import *
from ..boulder import *
from random import randint

class StoneWand(Wand):
  def name(self):
    return "stone wand"

  def range(self, avatar):
    return 0

  def charges(self):
    return randint(3,5)

  def effect(self, avatar):
    return None

  def spawn(self, avatar):
    return [Boulder, {'owner':avatar, 'momentum':[3*avatar.intent['direction'][0], 3*avatar.intent['direction'][1]], 'power': 10 + avatar.level()* 5}]

  def spawnPattern(self):
    return 14