from actionupdater import *

class DropUpdater(ActionUpdater):
  def topic(self):
    return 'drop'

  def processEvent(self, name, details, avatar):
    item = details['item']
    inventory = avatar.getComponent('Inventory')
    inventory.drop(avatar.intent['item'])
    avatar.logMessage('You drop the ' + item.getString())
