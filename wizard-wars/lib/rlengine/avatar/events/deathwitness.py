from eventwitness import *

class DeathWitness(EventWitness):
    def topic(self):
        return 'deaths'
        
    def processEvent(self, name, originator):
    	msgs = [' perishes!', ' keels over dead!', ' dies gruesomely!', ' dies!']
    	return originator.name + random.choice(msgs)