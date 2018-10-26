from ..item import *
from random import randint

class Pickaxe(Item):
    def configure(self, params):
        super(Pickaxe, self).configure(params)
        self.type = 'pickaxe'
        self.lastHit = None

    def defaultWeight(self):
        return 5

    def itemType(self):
        return 'pickaxe'

    def getString(self):
        return 'pickaxe'

    def handleMessage(self, name, value):
        if name == 'attempt-break':
            breakage = randint(0, 10)
            if breakage == 1:
                if self.owner:
                    self.owner.logMessage('The pickaxe breaks apart!')
                self.destruct()
        if name == 'collide-wall':
            worldMap = value['worldmap']
            tile = value['tile']
            worldMap.destroyTile(tile)

class XrayGoggles(Item):
    def configure(self, params):
        super(XrayGoggles, self).configure(params)
        self.type = 'face'

    def defaultType(self):
        return 'face'

    def handleMessage(self, name, value):
        if name == 'explodedacid':
            self.melt()

        if name == 'equipped':
            if self.owner:
                self.owner.getComponent('Eyeballs').xray = True

        if name == 'dequipped':
            if self.owner:
                self.owner.getComponent('Eyeballs').xray = False

    def getString(self):
        return 'x-ray goggles'

class GasMask(Item):
    def configure(self, params):
        super(GasMask, self).configure(params)
        self.type = 'face'
        self.defenseModifiers = params['defenseModifiers']

    def defaultType(self):
        return 'face'

    def handleMessage(self, name, value):
        if name == 'explodedacid':
            self.melt()

        if name == 'equipped':
            if self.owner:
                self.owner.getComponent('Eyeballs').torch_radius = 4

        if name == 'dequipped':
            if self.owner:
                self.owner.getComponent('Eyeballs').torch_radius = 10

    def getString(self):
        return 'gas mask'

class RemoteBomb(Item):
    def configure(self, params):
        super(RemoteBomb, self).configure(params)
        self.pair = None 

    def getRenderCode(self):
        return 202

    def name(self):
        return 'remote bomb'

    def handleMessage(self, name, value):
        if name == 'pickedup':
            self.pair.msg('buzz', 0)
            if self.pair.owner != None and self.pair.owner != self.owner:
                self.owner.delayedMessage('You have a bad feeling.')

        if name == 'trigger':
            if self.owner:
                explosion = {'params':{'name':'fire', 'owner':self.pair.owner, 'power':20, 'radius':3, 'expansiontime':0, 'duration':0}}
                self.owner.events['explode'] = explosion
                self.destruct()
            else:
                explosion = {'explode':{'destroy':True, 'params':{'name':'fire', 'owner':self.pair.owner, 'power':20, 'radius':3, 'expansiontime':0, 'duration':0}}}
                self.events = explosion

    def getString(self):
        return 'remote bomb'

class RemoteControl(Item):
    def configure(self, params):
        super(RemoteControl, self).configure(params)
        self.pair = None 

    def getRenderCode(self):
        return 203

    def name(self):
        return 'remote control'

    def handleMessage(self, name, value):
        if name == 'buzz':
            if self.owner != None:
                self.owner.delayedMessage ('Your remote control buzzes in your pocket!')

        if name == 'use':
            self.pair.msg('trigger', 0)
            self.destruct()
            return 'You press the button!'

    def getString(self):
        return 'remote control'