from potion import *

class FirePotion(Potion):
  def name(self):
    return 'fire potion'

  def drank(self, value):
    self.pickup = False
    self.x = self.owner.x
    self.y = self.owner.y
    self.owner.logMessage ('You pour the fire potion')
    self.owner.events['explode'] = {'destroy':False, 'params':{'name': 'fire', 'owner':self.owner, 'power':8, 'radius':2, 'expansiontime':24, 'duration':6}}
    self.destruct()

  def land(self, value):
    super(FirePotion, self).land(value)
    self.events = {'explode':{'destroy':True, 'params':{'name': 'fire', 'owner':self.owner, 'power':10, 'radius':2, 'expansiontime':3, 'duration':4}}}


