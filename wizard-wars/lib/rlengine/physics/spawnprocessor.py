from ..entity import *
from .. import libtcodpy as libtcod

class SpawnProcessor(Entity):
    def handleMessage(self, name, value):
        if name == 'process':
            self.events = {'spawns':None}
            self.spawnList = []
            avatars = value['avatars']
            worldMap = value['map']
            items = value['items']

            for item in items + avatars:
                if item.type == 'corpse':
                    keys = item.events.keys()
                    if item.active == True and 'spawn' in keys:
                        event = item.events['spawn']
                        if event['destroy']:
                            item.active = False

                        self.spawnList.append([event['params']['name'], event['params']['x'], event['params']['y']])
