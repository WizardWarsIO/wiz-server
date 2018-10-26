from entity import *
import tcod as libtcod

class Renderer(Entity):
    def configure(self, params):
        self.FOV_ALGO = 0  #default FOV algorithm
        self.FOV_LIGHT_WALLS = True  #light walls or not
        self.CAMERA_WIDTH = 21
        self.CAMERA_HEIGHT = 21

    def updateFOVmap(self):
        self.fov_map = libtcod.map_new(self.worldMap.MAP_WIDTH, self.worldMap.MAP_HEIGHT)
        for y in range(self.worldMap.MAP_HEIGHT):
            for x in range(self.worldMap.MAP_WIDTH):
                libtcod.map_set_properties(self.fov_map, x, y, not self.mapArray[x][y].block_sight, not self.mapArray[x][y].blocked)

    def handleMessage(self, name, value):
        if name == 'updateWorld':
            self.worldMap = value['worldMap']
            self.mapArray = self.worldMap.mapArray
            self.objectList = value['objects']
            self.updateFOVmap()
        
        if name == 'updateViews':
            self.updateFOVmap()
            avatarList = value['avatarList']
            events = value['eventList']
            
            for avatar in avatarList:
                eyeballs = avatar.getComponent('Eyeballs')
                visibleObjects = []                
                viewArray = [[[0, 0] for y in range(self.CAMERA_HEIGHT)] for x in range(self.CAMERA_WIDTH)]
                px = avatar.x 
                py = avatar.y
                libtcod.map_compute_fov(self.fov_map, px, py, eyeballs.torch_radius, self.FOV_LIGHT_WALLS, self.FOV_ALGO)

                camerax = px - 10
                cameray = py - 10
                
                for y in range(py - 10, py + 11):
                    for x in range(px - 10, px + 11):

                        visible = (eyeballs.xray or libtcod.map_is_in_fov(self.fov_map, x, y))
                        placex = x - camerax 
                        placey = y - cameray

                        if (x < 0 or y < 0 or x > self.worldMap.MAP_WIDTH - 1 or y > self.worldMap.MAP_HEIGHT - 1):
                            pass
                        else:
                            tile = self.mapArray[x][y]            
                            floorspot = tile.getRendercode(visible)
                            itemspot = 0
                            if visible:
                                itemsThere = self.worldMap.itemsOn([x, y])
                                visibleObjects += itemsThere 
                                for item in itemsThere:
                                    if item.visible:
                                        itemspot = item.getRenderCode()
                                        itemname = type(item).__name__
                                        if itemname in ['Avatar', 'Turret']:
                                            break
                            #Checkering
                            if (px + py + placex + placey) % 2 == 0:
                                floorspot += 10
                            #Out of view Darkening:
                            if not visible:
                                floorspot += 20
                            viewArray[placex][placey] = [floorspot, itemspot] 

                seenEvents = {'zaps':[], 'smacks':[], 'deaths':[], 'throws':[], 'drops':[], 'explosions':[], 'collisions':[], 'hurts':[], 'melts':[], 'fumbles':[], 'burns':[], 'shatters':[]}
                for eventType in events:
                    if events[eventType]:
                        for event in events[eventType]:      
                            for coords in event['affectedSpaces']:
                                if libtcod.map_is_in_fov(self.fov_map, coords[0], coords[1]):
                                    affectedSpaces = event['affectedSpaces']
                                    adjustedSpaces = [{'x':space[0] - camerax, 'y':space[1] - cameray} for space in affectedSpaces]
                                    newEvent = {'originator':event['originator'], 'name':event['name'], 'affectedSpaces':adjustedSpaces}
                                    seenEvents[eventType].append(newEvent)
                                    break

                
                avatar.msg('updateKnowledge', {'type':'FOV', 'data':self.fov_map})
                avatar.msg('updateKnowledge', {'type':'events', 'data':seenEvents})
                avatar.msg('updateKnowledge', {'type':'view', 'data':viewArray})
                avatar.msg('updateKnowledge', {'type':'visibleObjects', 'data':visibleObjects})
