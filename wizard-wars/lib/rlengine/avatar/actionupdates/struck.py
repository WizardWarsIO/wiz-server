from actionupdater import *

class StrikeUpdater(ActionUpdater):
  def topic(self):
    return 'struck'

  def processEvent(self, name, details, avatar):
    power = details.weight
    dmg = avatar.takeDamage('direct', power)
    owner = details.owner
    if owner == None:
        owner = details.pwner
    if owner != avatar:
        owner.msg('score', dmg)
    if dmg:
        avatar.delayedMessage('The ' + details.getString() + ' crashes into you for ' + str(dmg) + ' dmg!')
        avatar.lastDamage = 'a flying ' + details.getString() + ' from ' + owner.name
    else:
        avatar.delayedMessage('The ' + details.getString() + ' doesn\'t hurt!')