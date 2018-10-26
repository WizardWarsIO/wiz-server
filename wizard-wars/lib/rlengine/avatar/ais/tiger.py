from ai import *
from random import randint

class TigerAI(AIControls):
  def configure(self, params):
    super(TigerAI, self).configure(params)
    self.target = None
    self.timeout = 0

  def aiaw(self):
    return 'viciously shreds'

  def meleeWeapon(self):
    return 'claws'

  def aggressive(self):
    return True

  def greedy(self):
    return False

  def corpseCrave(self):
    return True

  def friendlies(self):
    return []

  def usesInventory(self):
    return False

  def aquatic(self):
    return True

  def retargets(self, targets):
    if not self.target:
      return True
    return self.timeout <= 0


  def pathfinding(self):
      return 0

  def getIntent(self, x, y, visibleObjects, worldMap):
    #tiger stalk