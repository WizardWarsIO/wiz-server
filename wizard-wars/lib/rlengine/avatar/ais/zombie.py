from ai import *
from ... import libtcodpy as libtcod
from random import randint

class ZombieAI(AIControls):
    def configure(self, params):
        super(ZombieAI, self).configure(params)
        self.target = None

    def meleeWeapon(self):
        return 'rotting hand'

    def greedy(self):
        return False

    def usesInventory(self):
        return False

    def friendlies(self):
        return ['priest', 'spider', 'witch', 'serpent']

    def validAggressionTarget(self, target):
        return target.intent['direction'] != [0, 0]

    def getAttackWord(self):
        return 'scratches'

    def aiaw(self):
        return None

    def aidw(self):
        return 'shambles away'

    def aiew(self):
        return 'trudges away'

    def ignoresItems(self):
        return True

    def getIntent(self, x, y, worldMap):
        target = self.updatePathToNearestTarget(x, y, worldMap, self.avatarTargets)
        direction = None

        if self.target:
            if self.x == self.target.x and self.y == self.target.y:
                direction = None
                self.target = None
            else:
                [dx, dy] = self.orthoTowards(self.target)
                targetCoord = [self.x + dx, self.y + dy]
                direction = [dx, dy]
                if targetCoord != [self.target.x, self.target.y]:
                    if worldMap.isBlocked(targetCoord):
                        if randint(0, 5) == 0:
                            direction = [0, 0]
        else:
            if target:
                obj = Entity({})
                obj.x = target.x
                obj.y = target.y
                self.target = obj
                direction = self.orthoTowards(self.target)

        if direction == None:
            direction = [0, 0]

        return {'type':'move', 'item':0, 'direction':direction}

    def handleMessage(self, name, value):
        super(ZombieAI, self).handleMessage(name, value)
        if name == 'collide':
            self.target = None

    def defaultName(self):
        return 'The Zombie'

    def health(self):
        return 80

    def race(self):
        return 'zombie'

    def renderCode(self):
        return 140

    def basePower(self):
        return {'direct': 13, 'swipe': 3}

    def baseDefense(self):
        return {'direct': 4, 'swipe': 6}