from actionupdater import *

class EquipUpdater(ActionUpdater):
  def topic(self):
    return 'toggleEquip'

  def processEvent(self, name, details, avatar):
    item = details['item']
    inventory = avatar.getComponent('Inventory')            
    inventory.toggleEquip(item)
    avatar.msg('updateKnowledge', {'type':'equipped', 'data':inventory})
