from potion import *

class HealingPotion(Potion):
  def defaultPotency(self):
    return 4

  def name(self):
    return 'healing potion'

  def drank(self, value):
    self.owner.msg('heal', {'power':self.potency})
    super(HealingPotion, self).drank(value)

  def land(self, value):
    pass