from ai import *
from random import randint
from ...items.wands.warp import *

class WitchAI(AIControls):
  def configure(self, params):
    super(WitchAI, self).configure(params)
    self.target = None
    self.action = 'poison'
    self.teleport = False
    self.lastHp = self.health()

  def greedy(self):
    return False

  def aiaw(self):
    return 'viciously swipes'

  def meleeWeapon(self):
    return 'cane'

  def getIntent(self, x, y, worldMap):
    self.x = x
    self.y = y

    target = self.updatePathToNearestTarget(x, y, worldMap, self.allTargets())

    if self.teleport:
      wand = WarpWand({})
      wand.owner = self.owner
      self.wand = wand
      self.teleport = False
      wandDirection = None
      if target:
        wandDirection = self.vectorTowards(target)

      if not wandDirection:
        num = randint(1,9)
        wandDirection = self.vectorForNum(num)
          
      return {'type': 'castzap', 'zap': wand, 'direction': wandDirection, 'item': 0}

    if self.target != None:
      position = self.target

      if self.action == 'poison':
        self.owner.events['explode'] = {'destroy':False, 'params':{'position': position, 'name': 'poison', 'maxSpreads': 4, 'owner':self.owner, 'power':10, 'radius':1, 'expansiontime':32, 'duration':6}} 
        self.target = None
      elif self.action == 'chaos' and target:
        target.msg('chaos', {})
        target.logMessage('The witch cackles as you fumble')
        self.target = None
   
    if target != None: 
      r = randint(0,5)
      self.target = [target.x, target.y]
      if r == 0:
        self.action = 'poison'
      elif r == 2:
        self.action = 'chaos'
      else:
        self.action = 'cackle'

    return {'type':'nothing', 'item':0, 'direction':[0, 0]}

  def handleMessage(self, name, value):
    super(WitchAI, self).handleMessage(name, value)
    if name == 'attacked':
      self.teleport = True
    elif name == 'loop':
      hp = self.owner.getHealth()
      if hp < self.lastHp:
        self.teleport = True
        self.lastHp = hp

  def defaultName(self):
    return 'The Witch'

  def health(self):
    return 30

  def race(self):
    return 'witch'

  def renderCode(self):
    return 135

  def basePower(self):
    return {'direct':10, 'swipe': 0}

  def baseDefense(self):
    return {'direct': 0, 'swipe': 0, 'poison': 100, 'venom': 100}








