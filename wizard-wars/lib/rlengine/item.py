from entity import *
from random import randint

class Item(Entity):
    def configure(self, params):
        super(Item, self).configure(params)
        
        if 'name' in params:
            self.name = params['name']
        else:
            self.name = self.name()
        self.events = {}
        self.bounces = False
        self.powerModifiers = {}
        self.defenseModifiers = {}
        self.visible = True
        self.weight = self.defaultWeight()
        self.collide = False
        self.pickup = True 
        self.x = 0
        self.y = 0
        self.owner = None 
        self.type = 'item'
        self.attackable = False

    def defaultType(self):
        return 'item'

    def didCollide(self):
        self.momentum = [0,0]

    def throwPower(self):
        return 1

    def defaultWeight(self):
        return 5

    def fall(self):
        if self.owner:
            self.owner.logMessage('The ' + self.getString() + ' falls to the ground')
            self.owner.intent['intentType'] = 'drop'
            self.owner.intent['item'] = self.owner.getComponent('Inventory').itemIndex(self)

    def destruct(self):
        if self.owner:
            self.owner.getComponent('Inventory').destroy(self)
        else:
            self.active = False

    def melt(self):
        if self.owner:
            self.owner.logMessage('Your ' + self.getString() + ' melts away!')
            self.owner.events['melts'].append({'name':self.name})
        self.destruct()

    def burn(self):
        if self.owner:
            self.owner.logMessage('Your ' + self.getString() + ' burns away!')
            self.owner.events['burns'].append({'name':self.name})
        self.destruct()

    def shatter(self):
        if randint(0, 1) == 0:
            if self.owner: 
                self.owner.delayedMessage('The boulder shatters your ' + self.getString() + '!')
                self.owner.events['shatters'].append({'name': self.name})
            self.destruct()

    def name(self):
        return 'thingy'

    def getRenderCode(self):
        lookup = self.name
        return Item.styleMap[lookup]

    def itemType(self):
        return 'item'

    def getModifier(self):
        return ''

    def getString(self):
        string = self.name 
        if self.getModifier() != '':
            string = string + ' ' + self.getModifier()
        return string