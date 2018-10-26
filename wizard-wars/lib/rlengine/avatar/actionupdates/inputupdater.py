from actionupdater import *

class InputUpdater(ActionUpdater):
  def topic(self):
    return 'input'

  def processEvent(self, name, details, avatar):
    if avatar.pid == details['name']:
      avatar.intent = details['intent']