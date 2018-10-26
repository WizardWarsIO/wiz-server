from actionupdater import *
from random import randint

class BoulderUpdater(ActionUpdater):
  def topic(self):
    return 'boulder-impact'

  def processEvent(self, name, details, avatar):
    if avatar.intent['type'] != 'chaos' and randint(0,1) == 0:
      avatar.intent['type'] = 'chaos'
      avatar.logMessage('The boulder knocks you on your ass')
