from ai import *

class MinotaurAI(AIControls):
  def configure(self, params):
    super(MinotaurAI, self).configure(params)
    self.lockedDirection = None

  def aiaw(self):
    return 'gores'

  def meleeWeapon(self):
    return 'horns'

  def usesInventory(self):
    return False

  def getIntent(self, x, y, worldMap):
    if self.lockedDirection == None:
      target = self.updatePathToNearestTarget(x, y, worldMap, self.avatarTargets)

      if target != None:
          [dx, dy] = self.vectorTowards(target)
          if [dx, dy] == [0, 0]:
              return {'type':'move', 'item':0, 'direction':[libtcod.random_get_int(0, -1, 1), libtcod.random_get_int(0, -1, 1)]}
          
          self.lockedDirection = [dx, dy]
          return {'type':'move', 'item':0, 'direction': self.lockedDirection}
      self.lockedDirection = None
      return {'type':'move', 'item':0, 'direction':[0, 0]}
    else:
        return {'type':'move', 'item':0, 'direction': self.lockedDirection}

  def handleMessage(self, name, value):
    super(MinotaurAI, self).handleMessage(name, value)
    if name == 'collide':
      obj = value['object']
      if obj == 'wall':
        worldMap = value['worldMap']
        worldMap.destroyTile(value['coordinate'])
      self.lockedDirection = None

  def defaultName(self):
    return "The Minotaur"

  def health(self):
    return 140

  def race(self):
    return 'minotaur'

  def renderCode(self):
    return 132

  def basePower(self):
    return {'direct':30, 'swipe': 20}

  def baseDefense(self):
    return {'direct': 6, 'swipe': 6}













