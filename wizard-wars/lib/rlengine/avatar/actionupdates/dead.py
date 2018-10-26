from actionupdater import *

class DeadUpdater(ActionUpdater):
  def topic(self):
    return 'die'

  def processEvent(self, name, details, avatar):
    avatar.status = 'dead'
    avatar.delayedMessage('You die!')