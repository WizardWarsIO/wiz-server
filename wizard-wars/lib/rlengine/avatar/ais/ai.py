import tcod as libtcod
from ...entity import *
import random
from random import randint

class AIControls(Entity):
    def configure(self, params):
        self.visibleObjects = []
        self.avatarTargets = []
        self.itemTargets = []
        self.FOV = []
        self.path = None
        self.newPath = False
        self.lastDirection = [0,0]
        self.assignName()

    def wearsArmor(self):
        return False

    def aggressive(self):
        return True

    def greedy(self):
        return True

    def corpseCrave(self):
        return False

    def friendlies(self):
        return []

    def ignoredItemTypes(self):
        return ['corpse']

    def usesInventory(self):
        return True

    def aquatic(self):
        return False

    def retargets(self, targets):
        return True

    def movementProfile(self): #collides with walls, fences etc. Renderer should use this for determining pathing
        return 1

    def pathfinding(self):
        return 0

    def getIntent(self, x, y, worldMap):
        return self.getStandardIntent(x, y, worldMap)

    def specialMeleeAttack(self):
        return None

    def meleeWeapon(self):
        return None

    def getAttackWord(self):
        return None

    def aiaw(self):
        return None

    def aidw(self):
        return None

    def aiew(self):
        return None

    def getDuckWord(self):
        return None

    def getEvadeWord(self):
        return None

    def walksOn(self):
        return None

    ############
    def validRaceTarget(self, race):
        return not race in [self.owner.race] + self.friendlies()

    def validAggressionTarget(self, target):
        return True

    def validAvatarTarget(self, target):
        if type(target).__name__ == 'Avatar' and target != self.owner:
            if self.aggressive():
                return self.validRaceTarget(target.race) and self.validAggressionTarget(target)
        return False

    def validItemTarget(self, target):
        if self.greedy():
            if target.pickup == True and not self.owner.getComponent('Inventory').isFull():
                return True
        if self.corpseCrave() and target.type == 'corpse':
            return True
        return False

    def filterTargets(self):
        self.avatarTargets = []
        self.itemTargets = []
        for target in self.visibleObjects:
            if self.validAvatarTarget(target):
                self.avatarTargets.append(target)
            elif self.validItemTarget(target):
                self.itemTargets.append(target)

    def followPath(self):
        direction = [0, 0]

        if self.path != None:
            if self.reachedEndOfPath():
                self.path = None
                return direction
            j = 0
            if not self.newPath:
                for i in range (libtcod.path_size(self.path)) :
                    pathx, pathy = libtcod.path_get(self.path, i)
                    if [self.owner.x, self.owner.y] == [pathx, pathy]:
                        j = i + 1
            if j == 0 and not self.newPath:
                self.path = None
            else:
                self.newPath = False
                tx, ty = libtcod.path_get(self.path, j)
                direction = [tx - self.owner.x, ty - self.owner.y]

        return direction

    def updatePathToNearestTarget(self, x, y, worldMap, targets):
        if self.FOV < 3:
            return None
        shortestPathLength = 100
        targetObject = None
        for item in targets:
            path = libtcod.path_new_using_map(self.FOV, 1)
            libtcod.path_compute(path, x, y, item.x, item.y)
            if not libtcod.path_is_empty(path):
                length = libtcod.path_size(path)
                if length < shortestPathLength:
                    shortestPathLength = length
                    self.path = path
                    self.newPath = True
                    targetObject = item
        return targetObject

    def defaultExploration(self, x, y, worldMap):
        longestPathLength = 0
        if self.FOV < 3:
            return False
        for i in range(4):
            path = libtcod.path_new_using_map(self.FOV, 1)
            libtcod.path_compute(path, x, y, randint(0, worldMap.MAP_WIDTH), randint(0, worldMap.MAP_HEIGHT))
            if not libtcod.path_is_empty(path):
                length = libtcod.path_size(path)
                if length > longestPathLength:
                    longestPathLength = length
                    self.path = path
                    self.newPath = True 
        return True

    def allTargets(self):
        return self.avatarTargets + self.itemTargets

    def getStandardIntent(self, x, y, worldMap):
        direction = [0, 0]
        target = self.updatePathToNearestTarget(x, y, worldMap, self.allTargets())
        if not self.path:
            self.defaultExploration(x, y, worldMap)
            
        direction = self.followPath()
        
        return {'type':'move', 'item':0, 'direction':direction}
    
    def getIntentW(self, x, y, visibleObjects, worldMap):
        return self.getIntent(x, y, visibleObjects, worldMap)

    def knowledge(self):
        return self.owner.getComponent('Knowledge')

    def path(self):
        return self.owner.getComponent('Knowledge').path

    def pathSize(self):
        if self.path == None:
            return 0
        return libtcod.path_size(self.path)

    def getThrowables(self):
        throwable = []
        inventory = self.owner.getComponent('Inventory')
        for key in inventory.items:
            if inventory.items[key] != None:
                item = inventory.items[key]
                if item.type != 'weapon' and item.type != 'armor':
                    throwable.append(key)
        return throwable

    def reachedEndOfPath(self):
        pathx, pathy = libtcod.path_get(self.path, libtcod.path_size(self.path) - 1)
        return [self.owner.x, self.owner.y] == [pathx, pathy]
      
    def handleMessage(self, name, value):
        if name == 'setIntent':
            players = value['players']
            items = value['items']

        if name == 'updateKnowledge':       
            if value['type'] == 'FOV':
                self.FOV = value['data']

            if value['type'] == 'visibleObjects':
                self.x = self.owner.x
                self.y = self.owner.y
                self.visibleObjects = value['data']
                self.filterTargets()
               
    def destruction(self):
        super(AIControls, self).destruction()
        self.path = None
        self.FOV = None

    def assignName(self):
        self.name = self.defaultName()

    def defaultName(self):
        return 'Dingus'

    def health(self):
        return 10

    def race(self):
        return 'wizard'

    def renderCode(self):
        return None

    def basePower(self):
        return {'direct': 5, 'swipe': 1}

    def baseDefense(self):
        return {'direct': 2, 'swipe': 0}