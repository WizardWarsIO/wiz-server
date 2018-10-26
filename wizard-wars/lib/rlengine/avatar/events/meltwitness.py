from eventwitness import *

class MeltWitness(EventWitness):
    def topic(self):
        return 'melts'
        
    def processEvent(self, name, originator):
        return originator.name + '\'s ' + name + ' melt away!'