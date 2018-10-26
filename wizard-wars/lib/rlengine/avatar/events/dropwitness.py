from eventwitness import *

class DropWitness(EventWitness):
    def topic(self):
        return 'drops'
        
    def processEvent(self, name, originator):
        return originator.name + ' tosses a ' + name + ' on the floor.'