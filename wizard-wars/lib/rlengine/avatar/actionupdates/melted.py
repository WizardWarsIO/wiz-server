from actionupdater import *

class MeltedUpdater(ActionUpdater):
  def topic(self):
    return 'explodedacid'

  def processEvent(self, name, details, avatar):
    power = details['power']
    damage = avatar.takeDamage('acid', power)
    owner = details['owner']
    if avatar != owner:
        owner.msg('score', damage)
    if damage > 0:
        avatar.delayedMessage('Your skin is melting! ' + str(damage) + 'dmg')
        avatar.lastDamage = 'acid from ' + owner.name 
    else:
        avatar.delayedMessage('The acid feels like a warm bath!')