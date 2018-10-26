from entity import *
from renderer import *
from physics.physics import *
from itemmanager import *

class Game(Entity):
    def configure(self, params):
        self.gameID = params['gameID']
        self.playerList = []
        self.botList = []
        self.itemList = []
        self.leaderboard = []
        self.isFinished = False
        self.targetWizards = params['targetWizards']

    def preSetup(self, params):
        self.level = params['level']

    def defaultRenderer(self):
        return Renderer

    def defaultTurnProcessor(self):
        return TurnProcessor

    def defaultItemManager(self):
        return ItemManager

    def defaultComponents(self, params):
        return [
        [self.defaultRenderer(), {}],
        [self.defaultTurnProcessor(), {}],
        [self.defaultItemManager(), {'itemManagerConfig': self.level.itemManagerConfig()}],
        [self.level.winConditionComponent(), {'winConditionConfig': self.level.winConditionConfig(), 'levelName':self.level.levelName()}]
        ]

    def tallyItems(self):
        totalItemWeight = 0
        for item in self.itemList:
            totalItemWeight = totalItemWeight + item.weight 

        totalBotWeight = 0
        for bot in self.botList:
            totalBotWeight += 5

        return (totalItemWeight, totalBotWeight)

    def firstPlace(self):
        if len(self.leaderboard) == 0:
            return "Wizard"

        fp = self.leaderboard[0]
        return fp['name']

    def firstPlacePoints(self):
        if (len(self.leaderboard) == 0):
            return "<0>"

        fp = self.leaderboard[0]
        return "<" + str(fp['score']) +">" 

    def refreshLeaderboard(self):
        self.leaderboard = []
        scorelist = []
        for player in (self.playerList + self.botList):
            if player.race == 'human':
                scorelist.append((player.name, player.getScore()))
        scorelist = sorted(scorelist, key=lambda player: player[1])
        scorelist.reverse()
        n = min(5, len(scorelist))
        for i in range(n):
            self.leaderboard.append({'name':scorelist[i][0], 'score':scorelist[i][1]})

    def hello(self):
        return 'Howdy!'

    def createPlayer(self, params):
        self.setupNewComponents([[Avatar, params]])


    def addObjects(self, objectList):
        playerList = []
        botList = []
        itemList = []
        for obj in objectList:
            if type(obj).__name__ == 'Avatar':
                if obj.ai != None:
                    botList.append(obj)
                    obj.worldMap = self.getComponent('WorldMap')
                else:
                    playerList.append(obj)
            else:
                itemList.append(obj)

        self.addPlayers(playerList)
        self.addBots(botList)
        self.addItems(itemList)

    def addPlayers(self, avatarList):
        self.addComponents(avatarList)
        self.playerList += avatarList
    
    def addBots(self, botList):
        self.addComponents(botList)
        self.botList += botList

    def addItems(self, itemList):
        self.addComponents(itemList)
        self.itemList += itemList 
    
    def sendIn(self, items):
        self.addObjects(items)
        self.getComponent('WorldMap').msg('scatterItems', {'items':items, 'extantItems':self.itemList + self.playerList + self.botList})

    def getItems(self):
        itemList = self.getComponents(itemTypes)
        return itemList 

    def getVisibleObjects(self):
        return self.itemList + self.playerList + self.botList 

    def getAvatar(self, name):
        for item in self.components:
            if type(item).__name__ == 'Avatar':
                if item.pid == name:
                    return item 

    def getPlayerInfo(self, playerID):
        player = self.getAvatar(playerID)
        if player:
            know = player.getComponent('Knowledge')
            status = "playing"
            messages = know.msgs
            winner = ""
            if self.isFinished:
                messages.append(self.firstPlace() + ' is the Winning Wizard!')
                winner = self.firstPlace() + " " + self.firstPlacePoints()
                status = "finished"
            text = "LEVEL " + str(player.level()) + " " + player.name +  " <" + str(player.getScore()) + ">     in " + self.winCondition().currentStatus()
            info = {'map':know.mapView, 'msgs':messages, 'inventory':know.inventory, 'eqIndexes': know.eqIndexes, 'events':know.events, 'hp':know.hp, 
            'lb':self.leaderboard, 'moved':know.moved, 'win': text, 'status':status, 'winner': winner}
            if player.dead == True:
                player.active = False
                info.update({'status':"killed", 'killedBy':player.lastDamage})
            know.msg('wipe', 0)

            return info
        return {'error': 'noplayer'}

    def getPlayerView(self, playerName):
        viewer = self.getAvatar(playerName)
        if viewer:
            return viewer.getComponent('Knowledge').mapView

    def getPlayerInventory(self, playerName):
        player = self.getAvatar(playerName)
        know = player.getComponent('Knowledge')
        if player:
            return [know.inventory, know.eq]

    def getPlayerMsgs(self, playerName):
        player = self.getAvatar(playerName)
        if player:
            know = player.getComponent('Knowledge')
            return know.msgs

    def getTotalMap(self):
        renderer = self.getComponent('Renderer')
        return renderer.getTotalMap()

    def clearDead(self):
        worldMap = self.getComponent('WorldMap')

        deadAvatars = []
        for avatar in self.playerList:
            if avatar.active == False:
                deadAvatars.append(avatar)

        deadBots = []
        for avatar in self.botList:
            if avatar.active == False:
                deadBots.append(avatar)

        deadItems = []
        for item in self.itemList:
            if item.active == False:
                deadItems.append(item)
            elif item.owner != None:
                deadItems.append(item)

        for x in deadAvatars:
            if x.ai:
                x.ai.owner = None
                x.ai = None
            x.destruction()
            self.components.remove(x)
            self.playerList.remove(x)

        for x in deadBots:
            x.worldMap = None
            x.destruction()
            self.components.remove(x)
            self.botList.remove(x)

        for x in deadItems:
            x.destruction()
            worldMap.removeItem(x)
            self.components.remove(x)
            self.itemList.remove(x)

    def msg(self, name, value):
        if name == 'loop':
            if self.playerList == []:
                return

        self.handleMessage(name, value)
        for item in self.components:
            item.msg(name, value)

    def winCondition(self):
        return self.getComponent(self.level.winConditionComponent().__name__)

    def handleMessage(self, name, value):
        if name == 'placeItems':
            worldMap = self.getComponent('WorldMap')
            for item in value:
                self.itemList.append(item)
                self.components.append(item)
                worldMap.placeItem(item, [item.x, item.y])
        if name == 'placeMonster':
            worldMap = self.getComponent('WorldMap')
            for item in value:
                self.playerList.append(item)
                self.components.append(item)
                worldMap.placeItem(item, [item.x, item.y])
        elif name == 'loop':
            # refs = gc.get_referrers(self.getComponent('WorldMap'))
            # print(str(len(refs)))
            # nums = str(len(self.components))
            # print nums

            avatars = self.playerList + self.botList 
            items = self.itemList
             
            worldMap = self.getComponent('WorldMap')
            turnProcessor = self.getComponent('TurnProcessor')
            renderer = self.getComponent('Renderer')

            turnProcessor.msg('processIntents', {'map':worldMap, 'avatars':avatars, 'items':items})

            self.events = turnProcessor.events 
    
            self.components += turnProcessor.addedItems 
            self.itemList += turnProcessor.addedItems

            itemManager = self.getComponent('ItemManager')

            spawnList = turnProcessor.spawnList
            for spawnData in spawnList:
                spawns = itemManager.handleMessage('spawn', spawnList)
                self.addObjects(spawns)
                for s in spawns:
                    worldMap.placeItem(s, [s.x, s.y])
            
            newstuff = itemManager.handleMessage('addStuff', {'items':self.itemList, 'bots':self.botList, 'leaderboard':self.leaderboard, 'targetWizards':self.targetWizards})
            if newstuff != []:
                self.addObjects(newstuff)
                worldMap.msg('scatterItems', {'items': newstuff, 'extantItems': self.playerList})
                # for newitem in newstuff:
                            
            renderer.msg('updateWorld', {'worldMap':worldMap, 'objects':self.getVisibleObjects()})
            renderer.msg('updateViews', {'avatarList':self.playerList +self.botList, 'eventList':self.events})
            
            #Post-turn messages
            for avatar in self.playerList:
                avatar.releaseMessages()            

            self.refreshLeaderboard()

            if (self.winCondition().isFinished()):
                self.isFinished = True

            self.clearDead()
