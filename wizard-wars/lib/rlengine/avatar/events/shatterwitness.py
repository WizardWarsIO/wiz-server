from eventwitness import *

class ShatterWitness(EventWitness):
    def topic(self):
        return 'shatters'
        
    def processEvent(self, name, originator):
        return originator.name + '\'s ' + name + ' shatters!'