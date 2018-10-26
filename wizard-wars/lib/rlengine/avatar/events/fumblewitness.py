from eventwitness import *

class FumbleWitness(EventWitness):
    def topic(self):
        return 'fumbles'
        
    def processEvent(self, name, originator):
        return originator.name + ' fumbles his ' + name + '!'