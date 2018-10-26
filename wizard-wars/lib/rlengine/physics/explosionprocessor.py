from ..entity import *
from exploder import *
from .. import libtcodpy as libtcod

class ExplosionProcessor(Entity):
    def addExplosion(self, data, item, worldMap):
        newExplosion = data
        expParams = newExplosion['params']
        exploder = Exploder(expParams)
        position = [item.x, item.y]
        if 'position' in expParams:
            position = expParams['position']
        worldMap.placeItem(exploder, position)
        if 'destroy' in newExplosion:
            if newExplosion['destroy'] == True:
                item.active = False
                worldMap.removeItem(item)
        self.addedItems.append(exploder)

    def handleMessage(self, name, value):
        if name == 'processExplosions':
            self.events = {'explosions':None}
            explosionList = []
            avatars = value['avatars']
            worldMap = value['map']
            items = value['items']
            self.addedItems = []

            for item in items + avatars:
                keys = item.events.keys()
                if item.active == True and 'explode-multi' in keys:
                    for data in item.events['explode-multi']:
                        [x,y] = data['coord']
                        foo = Entity({})
                        foo.x = x
                        foo.y = y
                        self.addExplosion({'params': data}, foo, worldMap)
                    item.events['explode-multi'] = {}

                if item.active == True and 'explode' in item.events.keys():
                    details = item.events['explode']
                    if 'params' in details.keys():    
                        self.addExplosion(details, item, worldMap)
                    item.events['explode'] = {}

            for item in items + self.addedItems:
                if type(item).__name__ == 'Exploder' and item.active == True:
                    affectedSpaces = []
                    fov_map = libtcod.map_new(worldMap.MAP_WIDTH, worldMap.MAP_HEIGHT)
                    for y in range(item.y - item.radius, item.y + item.radius):
                        for x in range(item.x - item.radius, item.x + item.radius):
                            not_block_sight = not worldMap.mapArray[x][y].block_sight if (x>0 and x< worldMap.MAP_WIDTH - 1 and y > 0 and y < worldMap.MAP_HEIGHT - 1) else False
                            not_block = not worldMap.mapArray[x][y].blocked if (x>0 and x< worldMap.MAP_WIDTH - 1 and y > 0 and y < worldMap.MAP_HEIGHT - 1) else False
                            libtcod.map_set_properties(fov_map, x, y, not_block_sight, not_block)
                    libtcod.map_compute_fov(fov_map, item.x, item.y, item.radius, False, 0)
                    for y in range(item.y - item.radius, item.y + item.radius):
                        for x in range(item.x - item.radius, item.x + item.radius):
                            if libtcod.map_is_in_fov(fov_map, x, y):
                                affectedSpaces.append([x, y])
                                worldMap.mapArray[x][y].msg('create', {'duration':item.duration, 'type':item.name, 'power':item.power, 'owner':item.pwner, 'maxSpreads':item.maxSpreads, 'original':id(item)})
                        
                    explosionList.append({'originator':item, 'name':item.name, 'affectedSpaces':affectedSpaces})
                    item.active = False

            self.events = {'explosions':explosionList}
