from ..entity import *

class Inventory(Entity):
    def configure(self, params):
        self.items = {1:None, 2:None, 3:None, 4:None, 5:None, 6:None, 7:None, 8:None, 9:None}
        self.equipped = {'weapon':None, 'armor':None, 'face':None, 'boots': None}
        self.eqIndexes = {'weapon':0, 'armor':0, 'face':0, 'boots': 0}
        self.owner = params['owner']
        self.faceIndex = 0
        self.armorIndex = 0
        self.bootsIndex = 0
        self.weaponIndex = 0

    def use(self, item):
        msg = self.toggleEquip(item)
        if msg:
            return msg
        msg = item.handleMessage('use', 0)
        if msg:
            return msg
        return 'I dont know how to use that!'

    def itemIndex(self, item):
        for key in self.items:
            if self.items[key] == item:
                return key
        return 0

    def getArmorCode(self):
        if self.equipped['armor']:
            return self.equipped['armor'].renderOffset()
        return 0

    def reRack(self):
        itemList = self.components
        self.items = {1:None, 2:None, 3:None, 4:None, 5:None, 6:None, 7:None, 8:None, 9:None}
        for item in itemList:
            if (item.type not in self.equipped.keys()) or (item.type in self.equipped.keys() and self.equipped[item.type] != item):
                self.addItem(item)
        for itemtype in ['face', 'weapon', 'armor', 'boots']:
            if itemtype in self.equipped.keys() and self.equipped[itemtype]:
                self.addItem(self.equipped[itemtype])
        self.updateEqIndexes()
        self.owner.msg('updateKnowledge', {'type':'inventory', 'data':self})

    def destroy(self, clearItem):
        clearItem.active = False
        for index in self.items:
            if self.items[index] == clearItem:
                self.items[index] = None
        self.dequip(clearItem)
        clearItem.owner = None
        self.clearInactive()
        self.reRack()

    def pickupItem(self, newItem):
        self.addItem(newItem)
        self.reRack()

    def addItem(self, newItem):
        for key in self.items:
            if self.items[key] == None:
                self.items[key] = newItem
                if newItem not in self.components:
                    self.components.append(newItem)
                return True 
        return False  

    def isFull(self):
        for key in self.items:
            if self.items[key] == None:
                return False 
        return True

    def isEquipped(self, item):
        if item == None: return False 
        if item.type in self.equipped.keys():
            if self.equipped[item.type] == item:
                return True
        return False 

    def dropItem(self, item):
        index = self.itemIndex(item)
        self.drop(index)

    def drop(self, itemIndex):
        item = self.items[itemIndex]
        if item == None: return 
        if self.dequip(item):
            self.owner.logMessage('Dequipped ' + item.getString())
            self.owner.msg('updateKnowledge', {'type':'equipped', 'data':self})
        self.components.remove(item)
        self.items[itemIndex] = None
        item.owner = None
        self.reRack()

    def getItem(self, index):
        return self.items[index]

    def equip(self, item):
        if item == None: return 
        if self.equipped[item.type] == None:
            self.equipped[item.type] = item 
            item.msg('equipped', 0)
            return True
        return False

    def dequip(self, item):
        if item == None: return 
        itemType = item.type
        if itemType in self.equipped.keys():
            if self.equipped[itemType] == item:
                self.equipped[itemType] = None
                item.msg('dequipped', 0)
                return True
                self.reRack()
                self.owner.msg('updateKnowledge', {'type':'inventory', 'data':self})
        return False

    def updateEqIndexes(self):
        self.eqIndexes = {'weapon':0, 'armor':0, 'face':0, 'boots': 0}
        for index, item in self.items.iteritems():
            if item and item.type in self.equipped.keys() and self.equipped[item.type] == item:
                self.eqIndexes[item.type] = index

    def toggleEquip(self, item):
        if item.type not in self.equipped.keys():
            return False
        if self.dequip(item):
            msg = 'Dequipped ' + item.getString()
        else:
            if self.equip(item):
                msg = 'Equipped ' + item.getString()
            else:
                replacing = self.equipped[item.type]
                msg  = 'Dequipped ' + replacing.getString()
                self.dequip(replacing)
                self.equip(item)
                msg = msg + ', equipped ' + item.getString()
        self.reRack()
        self.owner.msg('updateKnowledge', {'type':'inventory', 'data':self})
        return msg
        