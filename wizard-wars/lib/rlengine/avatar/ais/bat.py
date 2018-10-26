from ai import *

class BatAI(AIControls):
  def configure(self, params):
    super(BatAI, self).configure(params)
    self.previousCoordinates = []
    self.lastDirection = [0, 0]

  def meleeWeapon(self):
    return 'claws'

  def aiaw(self):
    return 'shreds'

  def aidw(self):
    return 'spin away from'

  def aiew(self):
    return 'flitter out from'

  def greedy(self):
    return False

  def usesInventory(self):
    return True

  def getIntent(self, x, y, worldMap):
    self.x = x
    self.y = y

    validDirection = 0
    direction = self.lastDirection
    while validDirection < 2:
      direction = [libtcod.random_get_int(0, -1, 1), libtcod.random_get_int(0, -1, 1)]
      newPosition = [self.x + direction[0], self.y + direction[1]]
      if newPosition in self.previousCoordinates == False:
        validDirection = 2
      else:
        validDirection = validDirection + 1


    self.previousCoordinates.append([self.x, self.y])
    if len(self.previousCoordinates) > 3:
      self.previousCoordinates.pop(0)

    return {'type':'move', 'item':0, 'direction': direction}

  def defaultName(self):
    return 'The Bat'

  def health(self):
    return 6

  def race(self):
    return 'bat'

  def renderCode(self):
    return 133

  def basePower(self):
    return {'direct':4, 'swipe': 1}

  def baseDefense(self):
    return {'direct': 0, 'swipe': 19, 'poison': 999, 'venom': 999}









