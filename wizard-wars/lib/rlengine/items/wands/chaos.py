from wand import *
from random import randint

class ChaosWand(Wand):
  def name(self):
    return 'trick wand'

  def zapType(self):
    return "chaos"

  def charges(self):
    return randint(1,2)

  def effect(self, avatar):
    return {'type': 'chaos', 'assailant': avatar}

  def spawn(self, avatar):
    return None