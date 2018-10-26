from ..item import *
    
class Boulder(Item):
    def configure(self, params):
        super(Boulder, self).configure(params)
        self.pushable = False
        self.collide = False
        self.weight = params['power']
        self.pickup = False
        self.pwner = params['owner']
        self.name = 'boulder'

        if 'momentum' in params:
            self.momentum = params['momentum']

    def handleMessage(self, name, value):
        if name == 'collide-avatar':
            value.msg('boulder-impact', self)
            self.active = False
        elif name == 'collide-wall':
            worldMap = value['worldmap']
            tile = value['tile']
            self.active = False
            if not worldMap.beyondBoundary(tile):
                worldMap.destroyTile(tile)
                
    def name(self):
        return 'boulder'
        
    def getString(self):
        return 'boulder'

    def getRenderCode(self):
        return 401

    def shouldCollide(self, other):
        return other.getString() != self.getString()

    def didCollide(self):
        pass