from actionupdater import *

class BonkUpdater(ActionUpdater):
  def topic(self):
    return 'bonk'

  def processEvent(self, name, details, avatar):
     otherAvatar = details
     avatar.logMessage('Bonk! You collide with ' + otherAvatar.name)