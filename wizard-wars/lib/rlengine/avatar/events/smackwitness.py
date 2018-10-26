from eventwitness import *

class SmackWitness(EventWitness):
    def topic(self):
        return 'smacks'
        
    def processEvent(self, name, originator):
        return originator.name + ' ' + originator.getAttackWord() + ' ' + name.name + ' with their ' + originator.meleeWeapon()



