from random import randint
from itemmaker import *

class ItemManager(Entity):
    def configure(self, params):
        super(ItemManager, self).configure(params)
        config = params['itemManagerConfig']
        
        self.itemMaps = config['item_maps']
        self.delays = config['item_delays']
        self.delayResets = config['item_delay_resets']
        self.minimumMonsters = config['minimum_monsters']
        self.monsterWeights = config['monster_weights']

    def determineSpawns0(self, items):
        allowedGroups = []

        for key in self.delays:
            self.delays[key] = self.delays[key] - 1
            if self.delays[key] < 1:
                allowedGroups.append(key)
                self.delays[key] = self.delayResets[key]

        spawns = []
        for key in allowedGroups:
            spawns = spawns + self.determineSpawns(items, key)
        return spawns

    def determineSpawns(self, items, groupName):
        totals = {}
        for item in items:
            name = item.name
            if name in totals.keys():
                totals[name] = totals[name] + 1
            else:
                totals[name] = 1

        toSpawn = []

        group = self.itemMaps[groupName]

        for key in group:
            keys = totals.keys()
            amount = 0

            if key in keys:
                amount = totals[key]

            if amount < group[key]:
                diff = group[key] - amount
                while diff > 0:
                    toSpawn.append(key)
                    diff = diff - 1

        return toSpawn

    def weightedBots(self):
        return self.monsterWeights

    def getRandomItemName(self, itemList):
        weightIndex = itemList
        totalWeight = 0
        for pair in weightIndex:
            totalWeight += pair[1]

        r = randint(0, totalWeight)

        acc = 0
        for pair in weightIndex:
            acc = acc + pair[1]
            if acc >= r:
                return pair[0]

    def defaultComponents(self, params):
        return [
        [ItemMaker, {}]]

    def shouldSpawn(self, items):
        total = 0
        for item in items:
            if item.name != 'boulder' and item.type != 'corpse':
            	total = total + 1

        return total < self.minimumItems()

    def shouldBirth(self, bots):
        return len(bots) < self.minimumBots()

    def minimumBots(self):
    	return self.minimumMonsters

    def minimumItems(self):
        return 8

    def handleMessage(self, name, value):
        if name == 'deliver':
            itemMaker = self.getComponent('ItemMaker')
            products = itemMaker.products
            itemMaker.products = []
            return products

        if name == 'spawn':
            spawns = []
            for [spawnName, x, y] in value:
                itemMaker = self.getComponent('ItemMaker')
                itemMaker.products = []
                spawn = itemMaker.handleMessage('make1', spawnName)
                spawn.x = x
                spawn.y = y
                spawns.append(spawn)
            return spawns


        if name == 'addStuff':
            bots = value['bots']
            targetWizards = value['targetWizards']
            itemMaker = self.getComponent('ItemMaker')
            itemMaker.products = []

            items = value['items'] #items that already exist
            leaderboard = value['leaderboard']

            newSpawns = self.determineSpawns0(items)
            for name in newSpawns:
                itemMaker.msg('make', name)
            if self.shouldBirth(bots):
                needed = self.minimumBots() - len(bots)
                while needed > 0:
                    needed = needed - 1
                    if randint(0,1) == 0:
                        needed = needed - 4
                    name = self.getRandomItemName(self.weightedBots())
             	    itemMaker.msg('make', name)

            if len(leaderboard) < targetWizards:
                itemMaker.msg('make', 'wizard')

            products = itemMaker.products
            itemMaker.products = []

            return products
