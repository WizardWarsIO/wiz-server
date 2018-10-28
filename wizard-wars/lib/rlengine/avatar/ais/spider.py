from ai import *
from ... import libtcodpy as libtcod
from random import randint

class SpiderAI(AIControls):
    def configure(self, params):
        super(SpiderAI, self).configure(params)
        self.target = None
        
    def walksOn(self):
        return('fence', 'floor')

    def specialMeleeAttack(self):
        return ['venom-foot', {'power': 4, 'owner': self.owner}]

    def meleeWeapon(self):
        return "fangs'"

    def aiaw(self):
        return "bites"

    def aidw(self):
        return 'scuttles way'

    def aiew(self):
        return 'skitters away'

    def ignoresItems(self):
        return True

    def retargets(self, targets):
        if self.knowledge().path:
            return randint(0, 15) == 0
        return True

    def getIntent(self, x, y, worldMap):
        self.x = x
        self.y = y
        direction = None
        target = self.updatePathToNearestTarget(x, y, worldMap, self.avatarTargets)
        if target:
            if self.reachedEndOfPath():
                direction = None
                self.path = None
            else:
                direction = self.followPath()
            if randint(0,5) == 0 and direction:
                numDirection = self.numberDirection(direction)
                nearbyDirections = {1: [4, 2], 2: [1, 3], 3: [1, 6],
                6: [3, 9], 9: [6, 8], 8: [9, 7], 7: [8, 4], 4: [7, 1]}
                options = nearbyDirections[numDirection]
                newNum = options[randint(0, 1)]
                direction = self.vectorForNum(newNum)
        if direction == None:
            direction = [libtcod.random_get_int(0, -1, 1), libtcod.random_get_int(0, -1, 1)]
        return {'type':'move', 'item':0, 'direction':direction}
        
    def handleMessage(self, name, params):
        super(SpiderAI, self).handleMessage(name, params)
        if name == 'collide':
            self.target = None

    def defaultName(self):
        return 'The Hunter Spider'

    def health(self):
        return 5

    def race(self):
        return 'spider'

    def renderCode(self):
        return 139

    def basePower(self):
        return {'direct':1, 'swipe': 0}

    def baseDefense(self):
        return {'direct': 6, 'swipe': 8}