from actionupdater import *

class AttackUpdater(ActionUpdater):
  def topic(self):
    return 'attack'

  def processEvent(self, name, details, avatar):
    value = details
    attackType = value['type']
    target = value['target']
    meleeWeapon = avatar.meleeWeapon()
    if attackType == 'direct':
        avatar.logMessage('You hit ' + target.name + ' with your ' + meleeWeapon)
    if attackType == 'swipe':
        avatar.logMessage(target.name + ' ducks out of the way and gets swiped by your ' + meleeWeapon)
