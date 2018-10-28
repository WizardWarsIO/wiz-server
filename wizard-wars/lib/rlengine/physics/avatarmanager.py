from ..entity import *
import tcod as libtcod
from corpse import *
from random import randint

class AvatarManager(Entity):
    def handleMessage(self, name, value):
        if name == 'processAvatars':
            avatars = value['avatars']
            worldMap = value['map']
            items = value['items']
            self.addedItems = []

            self.events = {'deaths':[], 'drops':[], 'hurts':[], 'melts':[], 'fumbles':[], 'burns':[], 'shatters': []}

            def checkFor(avatar, eventType):
                if eventType in avatar.events.keys() and avatar.events[eventType] != []:
                    nameList = []
                    for event in avatar.events[eventType]:
                        nameList.append(event['name'])
                    self.events[eventType].append({'originator':avatar, 'name':", ".join(nameList), 'affectedSpaces':[[avatar.x, avatar.y]]})
                    avatar.events[eventType] = []

            for avatar in avatars:
                [item, itemType] = avatar.usingItemType()
                [dx, dy] = avatar.intent['direction']
                intentType = avatar.intent['type']

                #Hurt flash
                if 'hurts' in avatar.events.keys() and avatar.events['hurts']:
                    self.events['hurts'].append({'originator':None, 'name':None, 'affectedSpaces':[[avatar.x - avatar.moved[0], avatar.y - avatar.moved[1]]]})
                    avatar.events['hurts'] = False

                checkFor(avatar, 'melts')
                checkFor(avatar, 'burns')
                checkFor(avatar, 'shatters')

                #Checking for deadbois
                if avatar.getHealth() <= 0 and avatar.dead == False:
                    avatar.msg('die', {})
                    avatar.dead = True  
                    inventory = avatar.getComponent('Inventory')
                    myItems = inventory.components
                    
                    AI = avatar.ai
                    if AI:
                        avatar.active = False
                        worldMap.removeItem(avatar)
                    else:
                        corpse = Corpse({'name':avatar.name})
                        worldMap.replaceItem(avatar, corpse)
                        self.addedItems.append(corpse)
                    
                    #Scatter inventory
                    for item in myItems:
                        item.owner = None
                        [nx, ny] = [0, 0]
                        while [nx, ny] == [0, 0] or worldMap.isBlocked([nx, ny]):
                            [rndx, rndy] = [libtcod.random_get_int(None, -2, 2), libtcod.random_get_int(None, -2, 2)]
                            [nx, ny] = [avatar.x + rndx, avatar.y + rndy]
                        worldMap.placeItem(item, [nx, ny])

                    self.addedItems += myItems
                    self.events['deaths'].append({'originator':avatar, 'name':'', 'affectedSpaces':[[avatar.x, avatar.y]]})
                
                #Case-by-case checks for "unusual" intent types.

                #Chaos effect
                elif intentType == 'chaos':
                    inv = avatar.getComponent('Inventory')
                    scatterItems = []
                    for key in inv.items.keys():
                      item = inv.items[key]
                      if not item == None:
                        equipped = inv.equipped
                        isEquipped = False
                        for k in equipped.keys():
                          if equipped[k] == item:
                            isEquipped = True
                        if not isEquipped:
                          if randint(0,1) == 0:
                            scatterItems.append([item, key])
                             
                    for [item, invIndex] in scatterItems:
                      inv.items[invIndex] = None
                      item.owner = None
                      if item in inv.components:
                        inv.components.remove(item)
                      avatar.events['fumbles'].append({'name':item.getString()})
                      [nx, ny] = [0, 0]
                      while [nx, ny] == [0, 0] or worldMap.isBlocked([nx, ny]):
                          [rndx, rndy] = [libtcod.random_get_int(None, -2, 2), libtcod.random_get_int(None, -2, 2)]
                          [nx, ny] = [avatar.x + rndx, avatar.y + rndy]
                      
                      worldMap.placeItem(item, [nx, ny])
                      self.addedItems.append(item)
                    inv.reRack()
                    checkFor(avatar, 'fumbles')
                    avatar.resetIntent()

                #Item usage
                elif intentType == 'apply':
                    inv = avatar.getComponent('Inventory')
                    if item:
                        usemsg = inv.use(item)
                        avatar.logMessage(usemsg)
                    avatar.resetIntent()

                #Interactions with items
                elif intentType == 'switch':
                    for obj in worldMap.mapArray[avatar.x + dx][avatar.y + dy].items_on:
                        obj.msg('interact', {'source':avatar})

                #Drops
                elif intentType == 'drop':
                    if item != None:
                        targetCoord = [avatar.x + dx, avatar.y + dy]
                        [nx, ny] = worldMap.getLimitCoord(targetCoord)
                        while worldMap.isBlocked([nx, ny]):
                            [rndx, rndy] = [libtcod.random_get_int(None, -1, 1), libtcod.random_get_int(None, -1, 1)]
                            [nx, ny] = [avatar.x + rndx, avatar.y + rndy]
                        worldMap.placeItem(item, [nx, ny])
                        avatar.msg('drop', {'item':item})
                        self.addedItems.append(item)
                        self.events['drops'].append({'originator':avatar, 'name':item.getString(), 'affectedSpaces':[[avatar.x, avatar.y], [nx, ny]]})
                        avatar.resetIntent()

                #Digging
                elif intentType == 'dig':
                    if [dx, dy] != [0, 0]:
                        digSpot = [avatar.x + dx, avatar.y + dy]
                        [axe, itemType] = avatar.usingItemType()
                        if axe.lastHit != digSpot:
                            avatar.logMessage ('You swing the pickaxe')
                            axe.lastHit = digSpot
                        else:
                            result = worldMap.handleMessage('dig', digSpot)
                            avatar.logMessage(result)
                            axe.lastHit = None
                            axe.msg('attempt-break', True)
                    avatar.resetIntent()

                #Drinking
                elif intentType == 'drink':
                    item.msg('drank', worldMap)
                    avatar.resetIntent()


                