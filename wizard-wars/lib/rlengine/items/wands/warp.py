from wand import *
from random import randint 

class WarpWand(Wand):
  def name(self):
    return 'warp wand'

  def zapType(self):
    return "warp"

  def charges(self):
    return randint(2,5)

  def effect(self, avatar):
    return {'type': 'warp', 'newCoordinate': [avatar.x, avatar.y]}

  def spawnPattern(self):
    return 'line'

  def afterZap(self, affectedLines, worldMap):
    lastLine = affectedLines[-1]
    lastSpace = lastLine[-1]
    if self.owner:
      self.owner.msg('warp', {'wandEffect': {'newCoordinate': lastSpace}, 'worldMap' : worldMap})
    self.zap()
