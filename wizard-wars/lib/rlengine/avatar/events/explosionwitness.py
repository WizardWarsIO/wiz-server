from eventwitness import *

class ExplosionWitness(EventWitness):
    def topic(self):
        return 'explosions'
        
    def processEvent(self, name, originator):
        pass