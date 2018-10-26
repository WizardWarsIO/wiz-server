from ..item import *

class Exploder(Item):
    def configure(self, params):
        self.type = 'exploder'
        super(Exploder, self).configure(params)
        self.name = params['name']
        self.pickup = False
        self.visible = False
        self.duration = params['duration']
        self.radius = params['radius']
        self.power = params['power']
        self.pwner = params['owner']
        self.maxSpreads = -1
        if 'maxSpreads' in params:
            self.maxSpreads = params['maxSpreads']