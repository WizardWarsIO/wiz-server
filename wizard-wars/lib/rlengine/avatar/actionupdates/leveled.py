from actionupdater import *

class LevelUpdater(ActionUpdater):
  def topic(self):
    return 'levelup'

  def processEvent(self, name, details, avatar):
    avatar.delayedMessage ('You feel stronger! Level ' + str(details))
