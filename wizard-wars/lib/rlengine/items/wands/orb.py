from wand import *
from ..sparkorb import *
from random import randint

class OrbWand(Wand):
  def name(self):
    return 'spark scepter'

  def charges(self):
    return randint(1,7)

  def range(self, avatar):
    return 0

  def effect(self, avatar):
    return None

  def spawn(self, avatar):
    return [SparkOrb, {'owner':avatar, 'momentum':[2*avatar.intent['direction'][0], 2*avatar.intent['direction'][1]], 'power': 22 + (avatar.level() * 2)}]

  def spawnPattern(self):
    return 202