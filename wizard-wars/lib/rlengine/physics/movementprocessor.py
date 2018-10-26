from ..entity import *
import random

class MovementProcessor(Entity):
    def doPickup(self, worldMap, avatar, newCoord):

        pickupItems = worldMap.itemsOn(newCoord)
        deadItems = []
        for item in pickupItems:
            if item.pickup == True:
                if avatar.hasRoom():
                    deadItems.append(item)
                    avatar.msg('pickup', item) 
                else:
                    avatar.logMessage('You have no room for the ' + item.getString())
            elif item.pickup == False and item.visible == True:
                avatar.logMessage('You are standing on ' + item.getString())
        for item in deadItems:
            worldMap.removeItem(item)

    def handleMessage(self, name, value):
        if name == 'processMoves':
            self.events = {}
            self.addedItems = []
            avatars = value['avatars']
            random.shuffle(avatars) #Shuffle so that "Bonks" resolve like a coin toss
            worldMap = value['map']
            items = value['items']
            newCoords = {}

            def cancelMovement(avatar):
                newCoords[avatar] = [avatar.x, avatar.y]
                avatar.intent.update({'type':None})

            #Build dict of new positions
            for avatar in avatars:
                if avatar.intent['type'] == 'move' and avatar.intent['direction'] != [0, 0]:
                    [dx, dy] = avatar.intent['direction']
                    newCoords[avatar] = [avatar.x + dx, avatar.y + dy]

            for avatar in newCoords:
                newCoord = newCoords[avatar]
                if not worldMap.beyondBoundary(newCoord):
                    tileType = worldMap.tileType(newCoord)
                    blockedBy = worldMap.tileBlockedBy(newCoord)
                    if blockedBy:
                        if blockedBy.attackable:
                            avatar.intent.update({'type':'melee', 'target':blockedBy})
                        elif blockedBy.pushable and blockedBy.momentum == [0,0]:
                            [dx, dy] = avatar.intent['direction']
                            if worldMap.isBlocked([blockedBy.x + dx, blockedBy.y + dy]):
                                cancelMovement(avatar)
                                avatar.logMessage('Something is behind ' + blockedBy.name)
                            else: #Successful Push
                                blockedBy.msg('pushed', avatar)
                                worldMap.moveItem(blockedBy, [blockedBy.x + dx, blockedBy.y + dy])
                    else:
                        if tileType in avatar.movesThrough:   
                            bonk = False 
                            #resolve mutex moves
                            for otherAvatar in newCoords:
                                if otherAvatar != avatar and newCoords[otherAvatar] == newCoord:
                                    avatar.msg('bonk', otherAvatar)
                                    cancelMovement(avatar)
                                    bonk = True
                            if bonk == False:
                                self.doPickup(worldMap, avatar, newCoord)
                        else:
                            cancelMovement(avatar)
                            avatar.msg('collide', {'worldMap': worldMap, 'object':tileType, 'coordinate': newCoord})
                else:
                    cancelMovement(avatar)
                    avatar.msg('collide', {'worldMap': worldMap, 'object':'wall', 'coordinate': newCoord})

                    
            for avatar in newCoords:
                if avatar.intent['type'] == 'move':
                    worldMap.moveItem(avatar, newCoords[avatar])
                    avatar.moved = avatar.intent['direction']

                avatar.msg('after-move', {worldMap: worldMap})    
                    