from actionupdater import *

class HealUpdater(ActionUpdater):
  def topic(self):
    return 'heal'

  def processEvent(self, name, details, avatar):
    hp = details['power']
    if hp < 1:
    	return
    avatar.logMessage('You are healing for ' + str(hp) + ' turns.')
