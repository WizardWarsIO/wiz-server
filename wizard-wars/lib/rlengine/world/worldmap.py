from ..entity import *
from .. import libtcodpy as libtcod
from tile import *

class WorldMap(Entity):
    def configure(self, params):
        self.MAP_WIDTH = params['MAP_WIDTH']
        self.MAP_HEIGHT = params['MAP_HEIGHT']
        self.DEPTH = params['DEPTH']
        self.MIN_SIZE = params['MIN_SIZE']
        self.FULL_ROOMS = params['FULL_ROOMS']
        self.mapArray = [[Tile({'x': x, 'y': y, 'blocked':True, 'block_sight':True}) for y in range(self.MAP_HEIGHT)] for x in range(self.MAP_WIDTH)]
        self.wall_peppering = params['wall_peppering']
        self.spreadList = []

    def getLimitCoord(self, space):
        x = space[0]
        y = space[1]
        if x < 1:
            x = 1
        elif x > self.MAP_WIDTH - 1:
            x = self.MAP_WIDTH - 1

        if y < 1:
            y = 1
        elif y > self.MAP_HEIGHT - 1:
            y = self.MAP_HEIGHT - 1
        
        return [x, y]

    def scatter(self, toScatter, extantItems):
        # get coordinates of all existing things
        # get new coordinates for each toScatter item
        # place new scatter at their new coordinate
        placedItems = list(extantItems)
        for item in toScatter:
            #Come up with 10 random candidates 
            candidateCoords = []
            while len(candidateCoords) < 10:
                cx = 0
                cy = 0
                while self.isBlocked([cx, cy]):
                    cx = libtcod.random_get_int(None, 1, self.MAP_WIDTH - 1)
                    cy = libtcod.random_get_int(None, 1, self.MAP_HEIGHT - 1)
                candidateCoords.append([cx, cy])

            #Loop through all the candidates and choose the one furthest from all the placed items
            furthestCandidate = None
            furthestDistance = None  
            for candidate in candidateCoords:
                [closest, closestDistance] = item.findClosest(candidate[0], candidate[1], placedItems)
                if furthestCandidate == None or closestDistance > furthestDistance:
                    furthestCandidate = candidate 
                    furthestDistance = closestDistance 

            self.placeItem(item, furthestCandidate)
            placedItems.append(item)

    def handleMessage(self, name, value):

        if name == 'loop':
            for element in self.mapArray:
                for tile in element:
                    tile.msg('loop', self)

            for spread in self.spreadList:
                spread['to'].msg('create', spread['create'])
            self.spreadList = []

        if name == 'scatterItems':
            toScatter = value['items']
            self.scatter(value['items'], value['extantItems'])

        if name == 'clearspace':
            x = value[0]
            y = value[1]
            tile = self.mapArray[x][y]
            tile.blocked = False
            tile.block_sight = False
            tile.rendercode = 1
            tile.name = 'floor'

        if name == 'blockoff':
            x = value[0]
            y = value[1]
            tile = self.mapArray[x][y]
            tile.blocked = True
            tile.block_sight = True 
            tile.rendercode = 6          
            tile.name = 'wall'

        if name == 'dig':
            x = value[0]
            y = value[1]
            if x < self.MAP_WIDTH - 2 and y < self.MAP_HEIGHT - 2: 
                if not self.beyondBoundary([x,y]):
                    if self.mapArray[x][y].blocked == True and self.mapArray[x][y].block_sight == True:
                        self.destroyTile([x,y])
                        return 'The wall crumbles!'
                return 'The wall glows and fades.'
            else:
                'The wall glows and fades.'

        if name == 'spread':
            self.spreadList.append(value)

    def makeFloor(self, x, y, rendercode):
        tile = self.mapArray[x][y]
        tile.blocked = False
        tile.block_sight = False  
        tile.rendercode = rendercode 
        tile.name = "floor"

    def makeWall(self, x, y, rendercode, blocksight, name="wall"):
        self.mapArray[x][y].blocked = True
        self.mapArray[x][y].block_sight = blocksight
        self.mapArray[x][y].rendercode = rendercode
        self.mapArray[x][y].name = name
        
    def makeHole(self, x, y):
        self.mapArray[x][y].blocked = True
        self.mapArray[x][y].block_sight = False 

    def destroyTile(self, tile):
        if self.beyondBoundary(tile):
            return
        t = self.getLimitCoord(tile)
            
        x = t[0]
        y = t[1]
        if self.isWall(t):
            self.makeFloor(x, y, 1)

    def isWall(self, tile):
        if self.beyondBoundary(tile):
            return True

        x = tile[0]
        y = tile[1]
        return self.mapArray[x][y].blocked == True and self.mapArray[x][y].block_sight == True

    def placeItem(self, item, coords):
        t = self.getLimitCoord(coords)
        px = t[0]
        py = t[1]
        item.x = px
        item.y = py

        self.mapArray[px][py].items_on.append(item)

    def replaceItem(self, old, new):
        self.placeItem(new, [old.x, old.y])
        self.removeItem(old)

    def removeItem(self, item):
        if item in self.mapArray[item.x][item.y].items_on:
            self.mapArray[item.x][item.y].items_on.remove(item)

    def moveItem(self, item, newcoords):    
        newx = newcoords[0]
        newy = newcoords[1]

        if item in self.mapArray[item.x][item.y].items_on:
            self.mapArray[item.x][item.y].items_on.remove(item)
            self.mapArray[newx][newy].items_on.append(item)
            item.x = newx
            item.y = newy
    
    def visible_items_on(self, coords):
        px = coords[0]
        py = coords[1]
        items = self.mapArray[px][py].items_on
        items = [item for item in items if item.visible == True]
        return items 

    def getTile(self, coords):
        t = self.getLimitCoord(coords)
        px = t[0]
        py = t[1]
        return self.mapArray[px][py]

    def itemsOn(self, coords):
        if self.beyondBoundary(coords):
            return []
        px = t[0]
        py = t[1]
        items = self.mapArray[px][py].items_on
        return items 

    def beyondBoundary(self, coords):
        px = coords[0]
        py = coords[1]
        return px < 1 or px > self.MAP_WIDTH - 2 or py < 1 or py > self.MAP_HEIGHT - 2

    def tileType(self, coords):
        px = coords[0]
        py = coords[1]
        if px < 0 or px > self.MAP_WIDTH - 1 or py < 0 or py > self.MAP_HEIGHT - 1:
            return 'wall'
        return self.mapArray[px][py].name

    def itemsOn(self, coords):
        px = coords[0]
        py = coords[1]
        return self.mapArray[px][py].items_on

    def tileBlockedBy(self, coords):
        px = coords[0]
        py = coords[1]
        items = self.mapArray[px][py].items_on
        for item in items:
            if item.collide == True:
                return item
        return False 

    def isBlocked(self, coords):
        if self.beyondBoundary(coords):
            return True
        px = coords[0]
        py = coords[1]
        tile = self.mapArray[px][py]
        blocked = not (tile.name == 'floor')
        return blocked

    def blockSight(self, coords):
        if self.beyondBoundary(coords):
            return True
        px = coords[0]
        py = coords[1]
        tile = self.mapArray[px][py]
        blocked = tile.block_sight
        return blocked