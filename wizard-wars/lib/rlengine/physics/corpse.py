from ..item import *
from ..avatar.avatar import *

class Corpse(Item):
    def configure(self, params):
        super(Corpse, self).configure(params)
        self.active = True
        self.type = 'corpse'
        self.pickup = False 
        self.weight = 0

    def getRenderCode(self):
        return 123

    def getString(self):
        return self.name + '\'s corpse'

    def handleMessage(self, name, details):
        if name == 'chaos':
            self.events['explode'] = {'destroy':False, 'params':{'name': 'poison', 'owner': details['assailant'], 'power':5, 'radius':5, 'expansiontime':10, 'duration':30}}
        elif name == 'zombify':
            self.events['spawn'] = {'destroy': True, 'params': {'name': 'zombie', 'x': self.x, 'y': self.y}}