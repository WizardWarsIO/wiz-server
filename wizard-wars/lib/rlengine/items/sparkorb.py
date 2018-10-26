from ..item import *
    
class SparkOrb(Item):
    def configure(self, params):
        super(SparkOrb, self).configure(params)
        self.pushable = False
        self.collide = False
        self.weight = params['power']
        self.pickup = False
        self.pwner = params['owner']
        self.name = 'orb'
        self.bounces = True
        self.explode = False
        self.duration = 20 + (self.pwner.level() * 3)
        self.detonater = None

        if 'momentum' in params:
            self.momentum = params['momentum']

    def handleMessage(self, name, value):
        if name == 'bounce':
            if self.duration < 1:
                self.active = False
                self.events['throw'] = {}
        elif name == 'collide-avatar':
            self.active = False
        elif name == 'zapped':
            if value['wandEffect']['type'] == 'lightning':
                self.explode = True
                zapper = value['wandEffect']['assailant']
                if zapper.ai:
                    self.detonater = self.pwner;
                else:
                    self.detonater = zapper
                self.events['throw'] = {}
        elif name == 'loop':
            self.duration = self.duration - 1
            if self.duration > 0:
                if self.explode:
                    self.events['throw'] = {}
                    self.events['explode'] =  {'destroy':True, 'params':{'name': 'fire', 'owner':self.pwner, 'power':30, 'radius':3, 'expansiontime':0, 'duration':0}}

    def name(self):
        return 'orb'
        
    def getString(self):
        return 'orb'

    def getRenderCode(self):
        return 402