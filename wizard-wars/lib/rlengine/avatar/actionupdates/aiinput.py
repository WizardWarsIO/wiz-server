from actionupdater import *

class AIInput(ActionUpdater):
  def topic(self):
    return 'loop'

  def processEvent(self, name, details, avatar):
    ai = avatar.ai
    if ai:
      avatar.intent = ai.getIntent(avatar.x, avatar.y, avatar.worldMap)