from actionupdater import *

class ZappedUpdater(ActionUpdater):
  def topic(self):
    return 'zapped'

  def processEvent(self, name, details, avatar):
    wandEffect = details['wandEffect']
    attackType = wandEffect['type']
    if attackType == 'none':
        return

    assailant = details['assailant']
    
    power = wandEffect['power']
    
    word = "zapped"
    if 'word' in wandEffect.keys():
        word = wandEffect['word']
    hitFor = avatar.takeDamage(attackType, power)
    if hitFor == 0:
        return
    if assailant != self.owner:
        avatar.delayedMessage('You are ' + word + ' by ' + attackType + ' from ' + assailant.name + ' and lose ' + str(hitFor) + 'HP')
        assailant.msg('score', hitFor)
        avatar.lastDamage = attackType + ' from ' + assailant.name 
    else:
        avatar.delayedMessage('You are ' + word + ' by ' + attackType + ' from your OWN WAND!')
        avatar.lastDamage = attackType + ' from your OWN WAND!'
