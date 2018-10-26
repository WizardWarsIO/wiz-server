from potion import *

class PoisonPotion(Potion):
  def name(self):
    return 'poison potion'

  def drank(self, value):
    self.pickup = False
    coord = value.getLimitCoord([self.owner.x + self.owner.intent['direction'][0], self.owner.y + self.owner.intent['direction'][1]])
    self.x = coord[0]
    self.y = coord[1]
    self.owner.logMessage('You pour the poison potion')
    self.owner.events['explode'] = {'destroy':False, 'params':{'name': 'poison', 'owner':self.owner, 'power':5,'maxSpreads': 8, 'radius':2, 'expansiontime':80, 'duration':40}}
    self.destruct()

  def land(self, value):
    super(PoisonPotion, self).land(value)
    self.events = {'explode':{'destroy':True, 'params':{'name': 'poison', 'owner':self.owner, 'power':5, 'radius':1, 'maxSpreads': 6, 'expansiontime':0, 'duration':40}}}