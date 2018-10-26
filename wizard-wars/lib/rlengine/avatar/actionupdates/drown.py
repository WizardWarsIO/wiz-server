from actionupdater import *

class DrownUpdater(ActionUpdater):
	def topic(self):
	    return 'standingonwater'

	def processEvent(self, name, details, avatar):	    
	    damage = avatar.takeDamage('water', 8)

	    if damage:
	        avatar.delayedMessage('You choke on the water. You\'re drowning!')
	        avatar.lastDamage = 'drowning'
	    else:
	    	avatar.delayedMessage('You float peacefully on the water\'s surface.')