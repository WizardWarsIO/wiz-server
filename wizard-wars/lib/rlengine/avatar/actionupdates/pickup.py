from actionupdater import *

class PickupUpdater(ActionUpdater):
  def topic(self):
    return 'pickup'

  def processEvent(self, name, details, avatar):
    item = details
    inventory = avatar.getComponent('Inventory')
    inventory.pickupItem(item)
    avatar.logMessage('Picked up ' + item.getString())
    item.owner = avatar
    item.msg('pickedup', 0)

    if item.type in inventory.equipped:
        if inventory.equipped[item.type] == None:
            avatar.delayedMessage(inventory.toggleEquip(item))
            
    avatar.getComponent('Knowledge').msg('updateKnowledge', {'type':'inventory', 'data':inventory})
