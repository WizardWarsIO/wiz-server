from potion import *

class AcidPotion(Potion):    
  def name(self):
    return 'acid potion'

  def drank(self, value):
    self.pickup = False
    coord = value.getLimitCoord([self.owner.x + self.owner.intent['direction'][0], self.owner.y + self.owner.intent['direction'][1]])
    self.x = coord[0]
    self.y = coord[1]
    self.owner.logMessage('You pour a puddle of acid')
    worldMap = value
    itemsOn = worldMap.itemsOn([self.x, self.y])
    for item in itemsOn:
      if item != self.owner:
        self.owner.logMessage(item.name + ' disintegrates')
        item.active = False
    self.owner.events['explode'] = {'destroy':False, 'params':{'name': 'acid', 'owner':self.owner, 'power':3, 'radius':1, 'expansiontime':0, 'duration':80}}
    self.destruct()

  def land(self, value):
    super(AcidPotion, self).land(value)
    self.events = {'explode':{'destroy':True, 'params':{'name': 'acid', 'owner':self.owner, 'power':30, 'radius':2, 'expansiontime':0, 'duration':0}}}