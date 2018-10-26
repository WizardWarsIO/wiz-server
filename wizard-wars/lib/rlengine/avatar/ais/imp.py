from ai import *
from random import randint

class ImpAI(AIControls):
  def configure(self, params):
    super(ImpAI, self).configure(params)
    self.lockedDirection = None

  def aiaw(self):
    return 'feverishly slices'

  def ignoresItems(self):
    return True

  def meleeWeapon(self):
    return 'claws'

  def getIntent(self, x, y, worldMap):
    self.x = x
    self.y = y

    if self.lockedDirection == None:
      rx = randint(0,1)
      if rx == 0:
        rx = -1
      ry = randint(0,1)
      if ry == 0:
        ry = -1
      self.lockedDirection = [rx, ry] 
      return {'type':'move', 'item':0, 'direction': self.lockedDirection}
    
    position = [self.x - self.lockedDirection[0], self.y - self.lockedDirection[1]]
    if randint(0, 3) == 0:
      self.owner.events['explode'] = {'destroy':False, 'params':{'position': [self.x, self.y], 'name': 'fire', 'owner':self.owner, 'power':10, 'radius':1, 'expansiontime':1, 'duration':3}} 
    return {'type':'move', 'item':0, 'direction': self.lockedDirection}
    
  def handleMessage(self, name, value):
    super(ImpAI, self).handleMessage(name, value)
    if name == 'collide':
      obj = value['object']
      self.lockedDirection = None

  def defaultName(self):
    return "The Imp"

  def health(self):
    return 40

  def race(self):
    return 'imp'

  def renderCode(self):
    return 134

  def basePower(self):
    return {'direct':14, 'swipe': 7}

  def baseDefense(self):
    return {'direct': 0, 'swipe': 2, 'fire': 999, 'acid': 999}













