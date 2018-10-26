from actionupdater import *

class CollidedUpdater(ActionUpdater):
  def topic(self):
    return 'collide'

  def processEvent(self, name, details, avatar):
    hitObject = details['object']
    if hitObject == None:
    	return
    avatar.intent['direction'] = [0, 0]
    avatar.logMessage('Oof! That is a ' + hitObject)
