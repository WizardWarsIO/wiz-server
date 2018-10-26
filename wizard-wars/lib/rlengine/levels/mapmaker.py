from .. import libtcodpy as libtcod
from random import randint

itemTypes = ['Wand', 'Weapon', 'Corpse']

class MapMaker():
    def __init__(self, game, worldMap, style):
        self.style = style
        self.game = game
        self.worldMap = worldMap
        self.mapArray = worldMap.mapArray
        self.MAP_WIDTH = worldMap.MAP_WIDTH
        self.MAP_HEIGHT = worldMap.MAP_HEIGHT
        self.DEPTH = worldMap.DEPTH
        self.MIN_SIZE = worldMap.MIN_SIZE
        self.FULL_ROOMS = worldMap.FULL_ROOMS
        self.wall_peppering = worldMap.wall_peppering
        self.make_bsp()
        
    def make_bsp(self):
        bsp_rooms = []
     
        bsp = libtcod.bsp_new_with_size(0, 0, self.MAP_WIDTH, self.MAP_HEIGHT)
        libtcod.bsp_split_recursive(bsp, 0, self.DEPTH, self.MIN_SIZE + 1, self.MIN_SIZE + 1, 1.5, 1.5)
                                 
        libtcod.bsp_traverse_inverted_level_order(bsp, self.traverse_node)
        self.game = None
     
    def traverse_node(self, node, dat):
        #Create rooms
        if libtcod.bsp_is_leaf(node):
            minx = node.x + 1
            maxx = node.x + node.w - 1
            miny = node.y + 1
            maxy = node.y + node.h - 1
     
            if maxx == self.MAP_WIDTH - 1:
                maxx -= 1
            if maxy == self.MAP_HEIGHT - 1:
                maxy -= 1
            
            if self.FULL_ROOMS == False:
                minx = libtcod.random_get_int(None, minx, maxx - self.MIN_SIZE + 1)
                miny = libtcod.random_get_int(None, miny, maxy - self.MIN_SIZE + 1)
                maxx = libtcod.random_get_int(None, minx + self.MIN_SIZE - 2, maxx)
                maxy = libtcod.random_get_int(None, miny + self.MIN_SIZE - 2, maxy)

            node.x = minx
            node.y = miny
            node.w = maxx-minx + 1
            node.h = maxy-miny + 1
     
            #Dig room
            coords = []
            for x in range(minx, maxx + 1):
                # random 0-10 spaces, if > minx and < maxx + 1
                # > miny and < maxy + 1
                for y in range(miny, maxy + 1):
                    if (x > minx and x < maxx + 1 and y > miny and y < maxy + 1):
                        coords.append([x,y])
                    self.game.msg('clearspace', [x, y])
            numWalls = randint(0, self.wall_peppering)
            wallCoords = []
            for n in range(0, numWalls):
                randCoord = coords[randint(0, len(coords) - 1)]
                wallCoords.append(randCoord)
            for wallCoord in wallCoords:
                #self.game.msg('blockoff', wallCoord)
                tile = self.style[6]
                blocksight = tile['blocksight']
                name = 'wall'
                if 'name' in tile.keys():
                  name = tile['name']
                self.worldMap.makeWall(wallCoord[0], wallCoord[1], 6, blocksight, name)
    
        else:
            for i in range(randint(1,3)):
                left = libtcod.bsp_left(node)
                right = libtcod.bsp_right(node)
                node.x = min(left.x, right.x)
                node.y = min(left.y, right.y)
                node.w = max(left.x + left.w, right.x + right.w) - node.x
                node.h = max(left.y + left.h, right.y + right.h) - node.y
                if node.horizontal:
                    if left.x + left.w - 1 < right.x or right.x + right.w - 1 < left.x:
                        x1 = libtcod.random_get_int(None, left.x, left.x + left.w - 1)
                        x2 = libtcod.random_get_int(None, right.x, right.x + right.w - 1)
                        y = libtcod.random_get_int(None, left.y + left.h, right.y)
                        self.vline_up(x1, y - 1)
                        self.hline(x1, y, x2)
                        self.vline_down(x2, y + 1)
         
                    else:
                        minx = max(left.x, right.x)
                        maxx = min(left.x + left.w - 1, right.x + right.w - 1)
                        x = libtcod.random_get_int(None, minx, maxx)
         
                        # catch out-of-bounds attempts
                        while x > self.MAP_WIDTH - 3:
                                x -= 1
         
                        self.vline_down(x, right.y)
                        self.vline_up(x, right.y - 1)
         
                else:
                    if left.y + left.h - 1 < right.y or right.y + right.h - 1 < left.y:
                        y1 = libtcod.random_get_int(None, left.y, left.y + left.h - 1)
                        y2 = libtcod.random_get_int(None, right.y, right.y + right.h - 1)
                        x = libtcod.random_get_int(None, left.x + left.w, right.x)
                        self.hline_left(x - 1, y1)
                        self.vline(x, y1, y2)
                        self.hline_right(x + 1, y2)
                    else:
                        miny = max(left.y, right.y)
                        maxy = min(left.y + left.h - 1, right.y + right.h - 1)
                        y = libtcod.random_get_int(None, miny, maxy)
         
                        # catch out-of-bounds attempts
                        while y > self.MAP_HEIGHT - 2:
                                 y -= 1
         
                        self.hline_left(right.x - 1, y)
                        self.hline_right(right.x, y)
     
        return True

    def vline(self, x, y1, y2):
        if y1 > y2:
            y1,y2 = y2,y1
     
        for y in range(y1,y2+1):
            self.game.msg('clearspace', [x, y])
    def vline_up(self, x, y):
        while y >= 0 and self.mapArray[x][y].blocked == True:
            self.game.msg('clearspace', [x, y])
            y -= 1
    def vline_down(self, x, y):
        while y < self.MAP_HEIGHT and self.mapArray[x][y].blocked == True:
            self.game.msg('clearspace', [x, y])
            y += 1
    def hline(self, x1, y, x2):
        if x1 > x2:
            x1,x2 = x2,x1
        for x in range(x1,x2+1):
            self.game.msg('clearspace', [x, y])
    def hline_left(self, x, y):
        while x >= 0 and self.mapArray[x][y].blocked == True:
            self.game.msg('clearspace', [x, y])
            x -= 1
    def hline_right(self, x, y):
        while x < self.MAP_WIDTH and self.mapArray[x][y].blocked == True:
            self.game.msg('clearspace', [x, y])
            x += 1

