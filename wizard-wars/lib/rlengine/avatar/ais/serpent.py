from ai import *
import tcod as libtcod
from random import randint

class SerpentAI(AIControls):
    def configure(self, params):
        super(SerpentAI, self).configure(params)
        self.lastDirection = [0, 1]

    def specialMeleeAttack(self):
        return ['venom-foot', {'power': 3, 'owner': self.owner}]

    def greedy(self):
        return False

    def usesInventory(self):
        return False

    def meleeWeapon(self):
        return "fangs"

    def friendlies(self):
        return ['witch']

    def getAttackWord(self):
        return "lunges"

    def aiaw(self):
        return "chomps"

    def aidw(self):
        return 'slithers away'

    def aiew(self):
        return 'slithers away'

    def ignoresItems(self):
        return False

    def getIntent(self, x, y, worldMap):
        self.x = x
        self.y = y

        target = self.updatePathToNearestTarget(x, y, worldMap, self.avatarTargets)
        if target and self.pathSize() < 3:
                r = randint(0, self.pathSize())
                if r == 0:
                    self.lastDirection = self.followPath()
                    return {'type': 'move', 'item': 0, 'direction': self.lastDirection}

        if self.lastDirection == None:
            # check for an orthogonal direction where they are adjacent to a wall
            c1 = worldMap.getTile([x, y - 1])
            c2 = worldMap.getTile([x + 1, y])
            c3 = worldMap.getTile([x, y + 1])
            c4 = worldMap.getTile([x - 1, y])
            avail = []
            for t in [c1, c2, c3, c4]:
                n1 = worldMap.getTile([c1.x, c1.y - 1])
                n2 = worldMap.getTile([c2.x + 1, c2.y])
                n3 = worldMap.getTile([c3.x, c3.y + 1])
                n4 = worldMap.getTile([c4.x - 1, c4.y])
                for n in [n1, n2, n3, n4]:
                    if n.blocked:
                        avail.append(t)
            if len(avail) == 0:
                nums = [2, 4, 6, 8]
                index = randint(0, len(nums) - 1)
                self.lastDirection = self.vectorForNum(nums[index])
                return {'type': 'move', 'item': 0, 'direction': self.lastDirection}
            else:
                index = randint(0, len(avail) - 1)
                self.lastDirection = self.vectorTowards(avail[index])
                return {'type': 'move', 'item': 0, 'direction': self.lastDirection}

        return {'type': 'move', 'item': 0, 'direction': self.lastDirection}
        
    def handleMessage(self, name, params):
        super(SerpentAI, self).handleMessage(name, params)
        if name == 'collide':
            self.lastDirection = None
            self.path = None            

    def defaultName(self):
        return 'The Serpent'

    def health(self):
        return 9

    def race(self):
        return 'serpent'

    def renderCode(self):
        return 137

    def basePower(self):
        return {'direct':1, 'swipe': 0}

    def baseDefense(self):
        return {'direct': 4, 'swipe': 3}