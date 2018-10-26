from actionupdater import *

class PoisonedUpdater(ActionUpdater):
  def topic(self):
    return 'explodedpoison'

  def processEvent(self, name, details, avatar):
    avatar.msg('poison', details['owner'])
    