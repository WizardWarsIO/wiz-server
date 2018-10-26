from eventwitness import *

class BurnWitness(EventWitness):
    def topic(self):
        return 'burns'
        
    def processEvent(self, name, originator):
        msgs = [' burns to a crisp!', ' turns to ash!', ' is consumed by fire!']
        return originator.name + '\'s ' + name + random.choice(msgs)