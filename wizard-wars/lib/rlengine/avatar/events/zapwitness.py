from eventwitness import *

class ZapWitness(EventWitness):
    def topic(self):
        return 'zaps'

    def processEvent(self, name, originator):
        return None
        return originator.name + ' zaps a bolt of ' + name + '!'