from ..entity import *
from random import randint
from bounce import *
from exploder import *

class ZapProcessor(Entity):
    def addAvatarZapOrigins(self, zapOrigins, avatars):
        for avatar in avatars:
            wand = None
            itemType = None
            if avatar.intent['type'] == 'zap' and avatar.intent['direction'] != [0, 0]:
                [wand, itemType] = avatar.usingItemType()
            if avatar.intent['type'] == 'castzap' and avatar.intent['direction'] != [0, 0]:
                wand = avatar.intent['zap']
                itemType = 'wand'

            if wand and itemType:
                self.zappers.append(avatar)
                wandEffect = wand.effect(avatar)
                if not wandEffect:
                  wandEffect = {'type': 'none', 'name': 'none'}
                wandSpawn = wand.spawn(avatar)
                wandExplosion = wand.explosion(avatar)
                if wandSpawn:
                    wandSpawn = [wand.spawnPattern(), wandSpawn]
                totalRange = wand.range(avatar)
                direction = avatar.intent['direction']
                zapOrigins.append({'source':avatar, 
                    'zapType': wand.zapType(), 
                    'wand': wand, 
                    'spawn':wandSpawn, 
                    'effect':wandEffect, 
                    'explosion': wandExplosion,
                    'range':totalRange, 
                    'originSpace':[avatar.x,avatar.y], 
                    'direction':direction}) 
        return zapOrigins

    def addItemZapOrigins(self, zapOrigins, items):
        for item in items:
            if 'zaps' in item.events.keys():
                zapOrigins += item.events['zaps']
                item.events['zaps'] = []
        return zapOrigins

    def precalculateZaps(self, objects):
        self.zappers = []
        avatars = objects['avatars']
        zapOrigins = self.addAvatarZapOrigins([], avatars)

        items = objects['items']        
        zapOrigins = self.addItemZapOrigins(zapOrigins, items)

        worldMap = objects['map']
        for zap in zapOrigins:
            zap['affectedSpaces'] = self.buildAffectedSpaces(zap, worldMap)
            for segment in zap['affectedSpaces']:
                name = 'nullzap'
                if zap['effect']:
                  name = zap['effect']['type']
                self.events['zaps'].append({'originator':zap['source'],
                 'assailant': zap['source'], 
                 'name': name, 
                 'affectedSpaces': segment})
                
        self.zapSources = zapOrigins

    def buildAffectedSpaces(self, zap, worldMap):
        space = zap['originSpace']
        [dx, dy] = zap['direction']
        totalRange = zap['range']
        
        lineList = []
        line = []
        while totalRange > 0:
            nextSpace = [space[0] + dx, space[1] + dy]
            if not worldMap.blockSight(nextSpace):
                line.append(nextSpace)
                space = nextSpace
            else:
                [space, rx, ry] = Bounce.bounce(dx, dy, space, worldMap)   
                dx = rx
                dy = ry
                line.append(space)
                if len(line) > 0:
                    lineList.append(list(line))
                    line = []

            totalRange = totalRange - 1
        if line not in lineList and len(line) > 0:
            lineList.append(line)

        return lineList

    def findTargets(self, objects, iteration):
        targets = []
        avatars = objects['avatars']
        items = objects['items']

        availableTargets = avatars + items

        worldMap = objects['map']
        for zap in self.zapSources:
            zap[iteration] = []
            affectedSegments = zap['affectedSpaces']
            for line in affectedSegments:
                for target in availableTargets:
                    if [target.x, target.y] in line:
                        zap[iteration].append(target)

    def finishAssigningZaps(self):
        for zap in self.zapSources:
            zap[2] = []
            removal = []
            for target in zap[0]:
                if target in zap[1]:
                    zap[2].append(target)
                    removal.append(target)
            for r in removal:
                if r in zap[0]:
                    zap[0].remove(r)
                if r in zap[1]:
                    zap[1].remove(r)

    def conveyEffects(self, worldMap):
        rates = [0.5, 0.8, 1]
        words = ['singed', 'zapped', 'scorched']

        multiExplosion = []
        for zap in self.zapSources:
            for i in range(len(rates)):
                rate = rates[i]
                for target in zap[i]:
                    effect = zap['effect']
                    if 'power' in effect:
                        effect['power'] = int(effect['power'] * rate)
                    effect['word'] = words[i]
                    target.msg(zap['zapType'], 
                        {
                        'worldMap': worldMap, 
                        'assailant': zap['source'], 
                        'wandEffect': effect})
            if 'explosion' in zap.keys():
                wandExplosion = zap['explosion']
                if wandExplosion != None:
                    for segment in zap['affectedSpaces']:
                        for coord in segment:
                            x = coord[0]
                            y = coord[1]
                            worldMap.mapArray[x][y].msg('create', wandExplosion)
        
    def spawnObject(self, spawnClass, spawnParams, space, worldMap):
      tile = worldMap.getTile(space)
      if tile.block_sight:  
        return None
      newObject = spawnClass(spawnParams)
      worldMap.placeItem(newObject, space)
      self.addedItems.append(newObject)

    def createSpawns(self, worldMap):
        for zap in self.zapSources:
            if zap['spawn']:
                [spawnPattern, spawnData] = zap['spawn']
                spawnClass = spawnData[0]
                spawnParams = spawnData[1]
                spaces = []
                if spawnPattern == 1:
                    spaces = [[zap['originSpace'][0] + zap['direction'][0],
                              zap['originSpace'][1] + zap['direction'][1]]]
                elif spawnPattern == 11:
                    spaces = [[zap['originSpace'][0] + zap['direction'][0],
                              zap['originSpace'][1] + zap['direction'][1]],
                              [zap['originSpace'][0] + (2 * zap['direction'][0]),
                              zap['originSpace'][1] + (2 * zap['direction'][1])]
                              ]
                elif spawnPattern == 14:
                    spaces = [[zap['originSpace'][0] + zap['direction'][0],
                              zap['originSpace'][1] + zap['direction'][1]],
                              [zap['originSpace'][0] + (2 * zap['direction'][0]),
                              zap['originSpace'][1] + (2 * zap['direction'][1])],
                              [zap['originSpace'][0] + (3 * zap['direction'][0]),
                              zap['originSpace'][1] + (3 * zap['direction'][1])],
                              [zap['originSpace'][0] + (4 * zap['direction'][0]),
                              zap['originSpace'][1] + (4 * zap['direction'][1])]]
                elif spawnPattern == 202:
                    direction = zap['direction']
                    num = self.numberDirection(direction)
                    # spaces.append([zap['originSpace'][0] + zap['direction'][0],
                              # zap['originSpace'][1] + zap['direction'][1]])

                    if num == 8 or num == 2:
                      spaces.append([zap['originSpace'][0] - 1,
                      zap['originSpace'][1] + zap['direction'][1]])
                      spaces.append([zap['originSpace'][0] + 1,
                      zap['originSpace'][1] + zap['direction'][1]])
                      spaces.append([zap['originSpace'][0] - 2,
                      zap['originSpace'][1] + zap['direction'][1]])
                      spaces.append([zap['originSpace'][0] + 2,
                      zap['originSpace'][1] + zap['direction'][1]])
                    elif num == 4 or num == 6:
                      spaces.append([zap['originSpace'][0] + zap['direction'][0],
                      zap['originSpace'][1] - 1])
                      spaces.append([zap['originSpace'][0] + zap['direction'][0],
                      zap['originSpace'][1] + 1])
                      spaces.append([zap['originSpace'][0] + zap['direction'][0],
                      zap['originSpace'][1] - 2])
                      spaces.append([zap['originSpace'][0] + zap['direction'][0],
                      zap['originSpace'][1] + 2])
                    else:
                      spaces.append([zap['originSpace'][0] + zap['direction'][0],
                      zap['originSpace'][1]])
                      spaces.append([zap['originSpace'][0],
                      zap['originSpace'][1] + zap['direction'][1]])
                      spaces.append([zap['originSpace'][0] + 2 * zap['direction'][0],
                      zap['originSpace'][1]])
                      spaces.append([zap['originSpace'][0],
                      zap['originSpace'][1] + 2 * zap['direction'][1]])
                elif spawnPattern == 3:
                    direction = zap['direction']
                    num = self.numberDirection(direction)
                    spaces.append([zap['originSpace'][0] + zap['direction'][0],
                              zap['originSpace'][1] + zap['direction'][1]])

                    if num == 8 or num == 2:
                      spaces.append([zap['originSpace'][0] - 1,
                      zap['originSpace'][1] + zap['direction'][1]])
                      spaces.append([zap['originSpace'][0] + 1,
                      zap['originSpace'][1] + zap['direction'][1]])
                    elif num == 4 or num == 6:
                      spaces.append([zap['originSpace'][0] + zap['direction'][0],
                      zap['originSpace'][1] - 1])
                      spaces.append([zap['originSpace'][0] + zap['direction'][0],
                      zap['originSpace'][1] + 1])
                    else:
                      spaces.append([zap['originSpace'][0] + zap['direction'][0],
                      zap['originSpace'][1]])
                      spaces.append([zap['originSpace'][0],
                      zap['originSpace'][1] + zap['direction'][1]])
                for space in spaces:
                  self.spawnObject(spawnClass, spawnParams, space, worldMap)

                  


    def resetIntents(self):
        for avatar in self.zappers:
            avatar.resetIntent()

    def dischargeZappers(self, worldMap):
        for zap in self.zapSources:
            wand = zap['wand']
            wand.afterZap(zap['affectedSpaces'], worldMap)

    def handleMessage(self, name, value):
        if name == 'endProcess':
            worldMap = value['map']
            self.findTargets(value, 1)
            self.finishAssigningZaps()
            self.conveyEffects(worldMap)
            self.createSpawns(worldMap)
            self.resetIntents()
            self.dischargeZappers(worldMap)
            sources = []
            for zapEvent in self.events['zaps']:
                originator = zapEvent['originator']


        if name == 'startProcess':
            self.events = {'zaps':[]}
            self.addedItems = []
            self.precalculateZaps(value)
            self.findTargets(value, 0)

