from ..entity import *
from bounce import *

class BallisticProcessor(Entity):
    def handleMessage(self, name, value):
        if name == 'processBallistics':
            self.events = {'throws':None, 'collisions':None}
            throwList = []
            collisionList = []
            avatars = value['avatars']
            worldMap = value['map']
            items = value['items']
            self.addedItems = []

            throwOrigins = []
            for avatar in avatars:
                if avatar.intent['type'] == 'throw' and avatar.intent['direction'] != [0, 0]:
                    inv = avatar.getComponent('Inventory')
                    [item, itemType] = avatar.usingItemType()
                    if item != None and (item.type == 'weapon' or inv.isEquipped(item) == False):
                        itemIndex = avatar.intent['item']
                        
                        direction = avatar.intent['direction']
                        throwStrength = avatar.basePower['direct'] - item.weight
                        avatar.resetIntent()
                        momentum = [direction[0] * throwStrength, direction[1] * throwStrength]
                        throwOrigins.append({'source':avatar, 'item':item, 'momentum':momentum})
                        self.addedItems.append(item)
                        avatar.logMessage('You toss the ' + item.getString())
                    else:
                        avatar.logMessage('You can\'t throw an equipped item.')
                        avatar.resetIntent()
            
            #get non-avatar throws 
            for item in items:
                if item.active == True and item.momentum != [0, 0]:
                    newThrow = {'source':item, 'item':item, 'momentum':item.momentum}
                    throwOrigins.append(newThrow)

            def collide(item, hit, coord):
                item.msg('collide-avatar', hit)
                hit.msg('struck', item)
                collisionList.append({'affectedSpaces':[coord], 'name':None, 'originator':None})
                item.didCollide()

            def norm(n):
                if n != 0:
                    return n/abs(n)
                return 0
                
            #process projectile paths
            for throw in throwOrigins:
                [ox, oy] = [throw['source'].x, throw['source'].y]
                [mx, my] = throw['momentum']
                [dx, dy] = [norm(mx), norm(my)]
                totalRange = abs(max(abs(mx), abs(my)))

                if mx > 0 and my > 0 and abs(mx) != abs(my):
                    print('Encountered an invalid momentum')
                    break

                item = throw['item']
                affectedSpaces = []
                nextSpace = [ox, oy]
                hit = None

                for obj in worldMap.mapArray[ox][oy].items_on:
                    if obj != item and obj != throw['source'] and obj.collide == True:        
                        hit = obj
                        collide(item, obj, [ox, oy])
                        totalRange = 0
                        collided = True

                while totalRange > 0:
                    collided = False 
                    hit = None

                    nextCoord = worldMap.getLimitCoord([nextSpace[0] + dx, nextSpace[1] + dy])

                    for obj in worldMap.mapArray[nextCoord[0]][nextCoord[1]].items_on:
                        if obj.collide == True:
                            hit = obj
                            collide(item, obj, nextSpace)
                            totalRange = 0
                            collided = True
                    blocked = worldMap.blockSight([nextSpace[0] + dx, nextSpace[1] + dy])
                    if not blocked and collided == False:
                        affectedSpaces.append(nextSpace)
                        nextSpace = [nextSpace[0] + dx, nextSpace[1] + dy]

                    elif blocked:
                        if item.bounces:
                            [prevX, prevY] = item.momentum
                            affectedSpaces.append(nextSpace)
                            nextSpace = [nextSpace[0] + dx, nextSpace[1] + dy]
                            [space2, rx, ry] = Bounce.bounce(dx, dy, nextSpace, worldMap)
                            nextSpace = worldMap.getLimitCoord(space2)
                            dx = rx
                            dy = ry
                            item.msg('bounce', nextSpace)
                            item.momentum = [rx * abs(prevX), ry * abs(prevY)]
                        else:
                            item.momentum = [0,0]
                            item.msg('collide-wall', {'tile': [nextSpace[0] + dx, nextSpace[1] + dy], 'worldmap': worldMap})
                            totalRange = 0
                            collisionList.append({'affectedSpaces':[nextSpace], 'name':None, 'originator':None})
                    totalRange = totalRange - 1
                        
                #Special case for momentum objects:
                if item == throw['source']:
                    worldMap.removeItem(item)

                #Convey effects to avatars and items in path
                worldMap.placeItem(item, nextSpace)
                item.msg('land', {'space':nextSpace, 'hit':hit})
                if item.owner:
                    item.owner.getComponent('Inventory').dropItem(item)

                throwList.append ({'originator':throw['source'], 'name':item, 'rendercode':item.getRenderCode(), 'affectedSpaces':affectedSpaces})
            
            self.events['throws'] = throwList
            self.events['collisions'] = collisionList
