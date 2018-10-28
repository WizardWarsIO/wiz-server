from actionupdater import *

class ChaosUpdater(ActionUpdater):
  def topic(self):
    return 'chaos'

  def processEvent(self, name, details, avatar):
    avatar.intent['type'] = 'chaos'
    avatar.logMessage('You seize up and lose all bodily control!')













