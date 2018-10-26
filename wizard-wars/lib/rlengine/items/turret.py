from ..item import *
from random import randint

class Turret(Item):
    def configure(self, params): 
        super(Turret, self).configure(params)

        self.type = 'turret'
        self.collide = True
        self.pushable = True
        self.behavior = params['behavior']
        self.beam = params['beam']
        self.pickup = False
        self.counter = 0
        self.score = 0
        self.range = 5
        self.delayReset = randint(3, 12)
        self.delay = self.delayReset
        self.ai = True #zap hack

    def name(self):
        return 'the turret'

    def getRenderCode(self):
        return 400

    def afterZap(self, affected, worldMap):
        pass

    def zapType(self):
        return "zapped"

    def makeBeam(self, direction):
        return {'source':self, 'wand': self, 'spawn':None, 'zapType': 'zapped', 'effect':self.beamEffect(), 'range':self.range, 'originSpace':[self.x,self.y] , 'direction':direction}

    def beamEffect(self):
        return {'assailant': self, 'explosion': None, 'type': 'lightning', 'power': 20, 'zapType': 'zapped'}

    def explosion(self, avatar):
        return None

    def handleMessage(self, name, value):
        if name == 'loop':
            if self.behavior == 'alternate':
                if self.delay > 0:
                    self.delay = self.delay - 1
                    if self.delay == 0:
                        self.delay = self.delayReset
                        self.counter = (self.counter + 1) % 4
                
                if self.counter == 1:
                    self.events['zaps'] = [self.makeBeam([1,0]), self.makeBeam([0,1]), self.makeBeam([-1,0]), self.makeBeam([0, -1])]
                                        
                if self.counter == 3:
                    self.events['zaps'] = [self.makeBeam([1,1]), self.makeBeam([1,-1]), self.makeBeam([-1,1]), self.makeBeam([-1,-1])]

            if self.behavior == 'spin':
                if self.delay > 0:
                    self.delay = self.delay - 1
                    if self.delay == 0:
                        self.delay = self.delayReset
                        self.counter = (self.counter + 1) % 8
                self.setDirection()

            if self.behavior == 'constant':
                self.setDirection()

        if name == 'interact':
            self.counter = (self.counter + 1) % 8

    def setDirection(self):
        if self.counter == 0:
            self.events['zaps'] = [self.makeBeam([0, 1])]
        if self.counter == 1:
            self.events['zaps'] = [self.makeBeam([-1, 1])]
        if self.counter == 2:
            self.events['zaps'] = [self.makeBeam([-1, 0])]
        if self.counter == 3:
            self.events['zaps'] = [self.makeBeam([-1, -1])]
        if self.counter == 4:
            self.events['zaps'] = [self.makeBeam([0, -1])]
        if self.counter == 5:
            self.events['zaps'] = [self.makeBeam([1, -1])]
        if self.counter == 6:
            self.events['zaps'] = [self.makeBeam([1, 0])]
        if self.counter == 7:
            self.events['zaps'] = [self.makeBeam([1, 1])]
