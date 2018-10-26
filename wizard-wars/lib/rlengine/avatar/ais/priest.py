from ai import *
from random import randint
from ...items.wands.lightning import *

class PriestAI(AIControls):
  def configure(self, params):
    super(PriestAI, self).configure(params)
    self.collided = False
    self.lastDirection = [0, -1]

  def friendlies(self):
    return ['zombie']

  def corpseCrave(self):
    return True

  def greedy(self):
    return False

  def randomNameList(self):
    return (['Dimbus', 'Dermbal', 'Drumbus', 'Droofus', 'Dringle', 'Doobie', 'Dubba', 'Dambus'])

  def aiaw(self):
    return 'righteously punches'

  def meleeWeapon(self):
    return 'fist'

  def getIntent(self, x, y, worldMap):
    direction = [0, 0]
    target = self.updatePathToNearestTarget(x, y, worldMap, self.allTargets())
    if target:
      if target.type == 'corpse':
        target.msg('zombify', True)
        # event for players in LOS to observe?
        return {'type': 'move', 'direction': self.lastDirection}
      if randint(0,1) == 0 and self.owner.aligned(target) and target.type != 'corpse' and self.distanceTo(x, y, target) < 5:
        wand = LightningWand({})
        wand.owner = self.owner
        self.wand = wand
        wandDirection = self.vectorTowards(target)        
        return {'type': 'castzap', 'zap': wand, 'direction': wandDirection, 'item': 0}
    if self.collided:
      [dx, dy] = self.rotateDirection(self.lastDirection, -2)
      if not worldMap.isBlocked([x + dx, y + dy]): #canmove.. using new movement rules
        self.lastDirection = [dx, dy]
    return {'type': 'move', 'direction': self.lastDirection}

  def handleMessage(self, name, value):
    super(PriestAI, self).handleMessage(name, value)
    if name == 'collide':
      self.collided = True
      self.lastDirection = self.rotateDirection(self.lastDirection, 1)  

  def defaultName(self):
    return 'Priest'

  def health(self):
    return 77

  def race(self):
    return 'priest'

  def basePower(self):
    return {'direct':10, 'swipe': 5}

  def baseDefense(self):
    return {'direct': 2, 'swipe': 2, 'lightning': 2}

  def renderCode(self):
    return 141

