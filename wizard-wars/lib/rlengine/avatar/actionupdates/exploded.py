from actionupdater import *

class ExplodedUpdater(ActionUpdater):
  def topic(self):
    return 'explodedfire'

  def processEvent(self, name, details, avatar):
    expType = details['type']
    power = details['power']
    damage = avatar.takeDamage(expType, power)
    owner = details['owner']

    if damage:
        avatar.delayedMessage('You are enveloped by a blast of fire for ' + str(damage) + 'dmg')
        avatar.lastDamage = "a blast of fire from " + owner.name
        if avatar != owner:
            owner.msg('score', damage)
        else:
            avatar.lastDamage = "fire of your own making!"
    else:
        avatar.delayedMessage('The fire doesn\'t hurt!')
