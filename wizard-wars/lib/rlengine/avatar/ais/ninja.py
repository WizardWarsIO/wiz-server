from ai import *
from ... import libtcodpy as libtcod
from random import randint

class NinjaAI(AIControls):
    def configure(self, params):
        super(NinjaAI, self).configure(params)
        self.lastDirection = [0,0]

    def meleeWeapon(self):
        return None

    def getAttackWord(self):
        return None

    def aiaw(self):
        return None

    def aidw(self):
        return 'flips away'

    def aiew(self):
        return 'flips away'

    def ignoresItems(self):
        return False

    def getIntent(self, x, y, worldMap):
        self.x = x
        self.y = y
        target = self.updatePathToNearestTarget(x, y, worldMap, self.allTargets())
        if target:
            [dx, dy] = self.vectorTowards(target)
            if randint(0,2) == 0:
                # move randomly
                numDirection = self.numberDirection([dx, dy])
                nearbyDirections = {1: [4, 2], 2: [1, 3], 3: [1, 6],
                6: [3, 9], 9: [6, 8], 8: [9, 7], 7: [8, 4], 4: [7, 1]}
                options = nearbyDirections[numDirection]
                newNum = options[randint(0, 1)]
                [dx2, dy2] = self.vectorForNum(newNum)
                dx = dx2
                dy = dy2
            if randint(0,4) == 0:
                dx = dx * 2
                dy = dy * 2
            if [dx, dy] == [0, 0]:
                return {'type':'move', 'item':0, 'direction':[libtcod.random_get_int(0, -1, 1), libtcod.random_get_int(0, -1, 1)]}
            self.lastDirection = [dx, dy]
            return {'type':'move', 'item':0, 'direction': self.lastDirection}

        # if self.type == 'random':
        direction = [0, 0]
        if self.lastDirection:
            direction = self.lastDirection
            if randint(0, 5) == 1:
                self.lastDirection = None
        if direction == [0, 0]:
            direction = [libtcod.random_get_int(0, -1, 1), libtcod.random_get_int(0, -1, 1)]
        return {'type':'move', 'item':0, 'direction':direction}

    def defaultName(self):
        return 'The Ninja'

    def health(self):
        return 50

    def race(self):
        return 'ninja'

    def renderCode(self):
        return 136

    def basePower(self):
        return {'direct':8, 'swipe': 7}

    def baseDefense(self):
        return {'direct': 4, 'swipe': 3}