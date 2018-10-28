from ai import *
import tcod as libtcod
from random import randint

class WizardAI(AIControls):
  def configure(self, params):
    super(WizardAI, self).configure(params)
    self.wait = False
    self.divert = 0

  def wearsArmor(self):
    return True

  def randomNameList(self):
    return (['Dimbus', 'Dermbal', 'Drumbus', 'Droofus', 'Dringle', 'Doobie'])

  def ignoresItems(self):
    return False

  def meleeWeapon(self):
    return 'fists'

  def aiaw(self):
    return 'pummels'

  def aidw(self):
    return 'stumble away from'

  def aiew(self):
    return 'lurch away from'

  def validRaceTarget(self, race):
    return True

  def getIntent(self, x, y, worldMap):
    inv = self.owner.getComponent('Inventory')
    direction = [0, 0]
    throwable = self.getThrowables()
    
    if throwable != [] and randint(0, 1) == 0:
      for target in self.avatarTargets:
        if self.owner.aligned(target):
          direction = self.owner.vectorTowards(target)
          useItem = random.choice(throwable)
          attack = {'type': 'fire', 'item': useItem, 'direction': direction}
          itemName = inv.items[useItem].name
          if itemName in ['stone wand', 'spark scepter']:
            self.wait = True
          elif itemName in ['inferno wand', 'poison potion', 'fire potion', 'acid potion']:
            self.divert = 3
          return attack

    if not self.wait:
      intent = self.getStandardIntent(x, y, worldMap)
      if self.divert > 0:
        intent['direction'][0] = -intent['direction'][0]
        intent['direction'][1] = -intent['direction'][1]
        self.divert = self.divert - 1
      return intent
    else:
      self.wait = False 
      return {'type': 'move', 'item': 0, 'direction': [0, 0]}

  def defaultName(self):
    return random.choice(self.randomNameList())

  def health(self):
    return 50

  def race(self):
    return 'human'

  def basePower(self):
    return {'direct':10, 'swipe': 5}

  def baseDefense(self):
    return {'direct': 2, 'swipe': 2}