from eventwitness import *

class ThrowWitness(EventWitness):
    def topic(self):
        return 'throws'
        
    def processEvent(self, name, originator):
      return ""