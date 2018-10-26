from wand import *
from random import randint

class LightningWand(Wand):
  def name(self):
    return 'lightning wand'

  def charges(self):
  	return randint(2,4)

  def effect(self, avatar):
    return {'assailant': avatar, 'type': 'lightning', 'power': 20 + (avatar.level() * 4)}

  def spawn(self, avatar):
    return None