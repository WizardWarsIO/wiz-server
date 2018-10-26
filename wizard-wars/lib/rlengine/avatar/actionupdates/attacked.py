from actionupdater import *

class AttackedUpdater(ActionUpdater):
  def topic(self):
    return 'attacked'

  def processEvent(self, name, details, avatar):
    value = details
    power = value['power']
    assailant = value['assailant']
    meleeWeapon = assailant.meleeWeapon()
    attackType = value['type']
    hitFor = avatar.takeDamage(attackType, power)
    assailant.msg('score', hitFor)
    if attackType == 'direct':
        if hitFor > 0:
            attackWord = assailant.getAttackWord()
            avatar.logMessage(assailant.name + ' ' + attackWord + ' you with their ' + meleeWeapon + ' for ' + str(hitFor) + ' damage!')
            avatar.lastDamage = assailant.name + '\'s ' + meleeWeapon
        else:
            avatar.logMessage(assailant.name + '\'s puny ' + meleeWeapon + ' does not hurt you!')
    if attackType == 'swipe':
        if hitFor > 0:
            duckWord = avatar.getDuckWord()
            avatar.logMessage('You ' + duckWord + '! ' + assailant.name + 's ' + meleeWeapon + ' swipes you for ' + str(hitFor) + 'damage.')
            avatar.lastDamage = assailant.name + '\'s ' + meleeWeapon
        else:
            evadeWord = avatar.getEvadeWord()
            avatar.logMessage('You ' + evadeWord + ' '+ assailant.name)
