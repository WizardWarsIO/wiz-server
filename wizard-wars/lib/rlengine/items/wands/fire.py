from wand import *
from random import randint

class FireWand(Wand):
  def name(self):
    return 'inferno wand'

  def charges(self):
    return randint(2,4)

  def effect(self, avatar):
    return {'type': 'fire', 'power': 10 + (avatar.level() * 3)}

  def explosion(self, avatar):
    return {'type': 'fire', 'name': 'fire', 'owner':avatar, 'power':20, 'radius':1, 'expansiontime':0, 'maxSpreads': 1, 'duration':10 + (3 * avatar.level())}

  def spawn(self, avatar):
    return None