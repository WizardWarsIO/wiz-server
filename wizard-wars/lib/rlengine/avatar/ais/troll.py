from ai import *
from ... import libtcodpy as libtcod
from random import randint

class TrollAI(AIControls):
  def configure(self, params):
    super(TrollAI, self).configure(params)
    self.previousCoordinates = []
    self.lastDirection = [0, 0]

  def ignoresItems(self):
    return False

  def meleeWeapon(self):
    return 'claws'

  def aiaw(self):
    return 'slices'

  def aidw(self):
    return 'stumble away from'

  def aiew(self):
    return 'lurch away from'

  # def getIntent(self, x, y, visibleObjects):
  #   self.x = x
  #   self.y = y
    
  #   targets = self.filteredObjects(visibleObjects)

  #   [closestAvatar, closestDistance] = self.findClosest(x, y, targets)

  #   if closestAvatar != None and closestAvatar != self.owner:
  #     [dx, dy] = self.vectorTowards(closestAvatar)
  #     inventory = self.owner.getComponent('Inventory')
  #     throwable = []
  #     for key in inventory.items:
  #       if inventory.items[key] != None:
  #         item = inventory.items[key]
  #         if item.type != 'weapon' and item.type != 'armor':
  #           throwable.append(key)
            
  #     if len(throwable) > 0:
  #       ii = randint(0, len(throwable) -1)
  #       rd = [libtcod.random_get_int(0, -1, 1), libtcod.random_get_int(0, -1, 1)]
  #       return {'type': 'fire', 'item': ii, 'direction': rd}

  #     if [dx, dy] == [0, 0]:
  #       return {'type':'move', 'item':0, 'direction':[libtcod.random_get_int(0, -1, 1), libtcod.random_get_int(0, -1, 1)]}
    
  #     self.lastDirection = [dx, dy]
  #     return {'type':'move', 'item':0, 'direction': self.lastDirection}


    # if self.type == 'random':
    direction = [0, 0]
    if self.lastDirection:
      direction = self.lastDirection
      if randint(0, 5) == 1:
        self.lastDirection = None
    if direction == [0, 0]:
      direction = [libtcod.random_get_int(0, -1, 1), libtcod.random_get_int(0, -1, 1)]
    return {'type':'move', 'item':0, 'direction':direction}


  def defaultName(self):
    return 'The Troll'

  def health(self):
    return 40

  def race(self):
    return 'troll'

  def renderCode(self):
    return 131

  def basePower(self):
    return {'direct':8, 'swipe': 6}

  def baseDefense(self):
    return {'direct': 2, 'swipe': 2}