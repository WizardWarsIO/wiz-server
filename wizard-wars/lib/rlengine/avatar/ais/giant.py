from ai import *
from ... import libtcodpy as libtcod
from random import randint
from ...items.wands.stone import *

class StoneGiantAI(AIControls):
    def configure(self, params):
        super(StoneGiantAI, self).configure(params)
        self.lastDirection = [0,1]
        self.collided = True

    def meleeWeapon(self):
        return "stone fists"

    def aiaw(self):
        return 'pounds'

    def aidw(self):
        return 'jumps away'

    def aiew(self):
        return 'jumps away'

    def ignoresItems(self):
        return True

    def getIntent(self, x, y, worldMap):
        self.x = x
        self.y = y
        if self.collided == True:
            self.collided = False
            if randint(0,2) == 0:
                wand = StoneWand({})
                wand.owner = self.owner
                num = range(1,10)[randint(0, 8)]
                wandDirection = self.vectorForNum(num)
                self.collided = False
                return {'type': 'castzap', 'zap': wand, 'direction': wandDirection, 'item': 0}
        rr = randint(0, 8)
        if rr == 0 and len(self.avatarTargets) > 0:
            [closestAvatar, closestDistance] = self.findClosest(x, y, self.avatarTargets)
            if closestDistance > 1.5 and randint(0, 2) == 0:
                wand = StoneWand({})
                wand.owner = self.owner
                wandDirection = self.vectorTowards(closestAvatar)
                if len(self.itemTargets) > 0:
                    [targetItem, itemDistance] = self.findClosest(closestAvatar.x, closestAvatar.y, self.itemTargets)
                    wandDirection = self.vectorTowards(targetItem)
                return {'type': 'castzap', 'zap': wand, 'direction': wandDirection, 'item': 0}
            else:
                self.lastDirection = self.vectorTowards(closestAvatar)
                return {'type': 'move', 'item': 0, 'direction': self.lastDirection}
        else:
            if self.lastDirection:
                if randint(0, 2) == 0:
                    return {'type': 'nothing', 'item': 0, 'direction': [0,0]}    
                return {'type': 'move', 'item': 0, 'direction': self.lastDirection}
                    
            num = range(1,10)[randint(0, 8)]
            self.lastDirection = self.vectorForNum(num)
            return {'type': 'move', 'item': 0, 'direction': self.lastDirection}

        return {'type': 'move', 'item': 0, 'direction': self.lastDirection}

    def handleMessage(self, name, params):
        super(StoneGiantAI, self).handleMessage(name, params)
        if name == 'collide':
            self.collided = True
            self.lastDirection = None

    def defaultName(self):
        return 'The Stone Giant'

    def health(self):
        return 200

    def race(self):
        return 'giant'

    def renderCode(self):
        return 138

    def basePower(self):
        return {'direct':32, 'swipe': 3}

    def baseDefense(self):
        return {'direct': 14, 'swipe': 3}