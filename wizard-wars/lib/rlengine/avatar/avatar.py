from ..item import *
from ..entity import *
from actionupdates.nerves import *
from eyeballs import *
from knowledge import *
from inventory import *
from experience import *
from health import *
from ais.ais import *

from random import randint

class Avatar(Entity):
    def defaultComponents(self, params):
        components = [
        [Eyeballs, {'owner':self}], 
        [Knowledge, {'owner':self}], 
        [Inventory, {'owner':self}],
        [Nerves, {'owner': self}],
        [Experience, {'owner': self}],
        [Health, {'owner': self, 'HP': params['HP']}]
        ]
        return components

    def installAI(self, ai):
        self.components.append(ai)
        self.ai = ai
        self.ai.owner = self

        inv = self.getComponent('Inventory')
        if not self.ai.wearsArmor():
            inv.equipped = {'weapon':None, 'face':None, 'boots': None}

        if self.ai.renderCode():
            self.rendercode = self.ai.renderCode()
        if self.ai.walksOn():
            self.movesThrough = self.ai.walksOn()
        self.name = self.ai.name

    def configure(self, params):
        if 'name' in params:
            self.name = params['name'] 
        self.race = params['race']  #Used to determine friendly / nonfriendly 
        self.ai = None    
        self.x = 0
        self.y = 0
        self.worldMap = None
        self.intent = {'type':'move', 'item':0, 'direction':[0, 0], 'target':None}
        self.status = 'alive'
        self.messageBacklog = []
        self.collide = True #Projectiles will hit characters 
        self.attackable = True
        self.visible = True
        self.log = []
        self.basePower = params['basePower']
        self.baseDefense = params['baseDefense']
        self.pid = 0
        if 'pid' in params:
            self.pid = params['pid']
        self.rendercode = None
        if 'rendercode' in params:
            if params['rendercode'] != None:
                self.rendercode = params['rendercode']
        self.dead = False
        self.moved = [0,0] #Used for rendering zaps pre-move
        self.events = {'hurts':False, 'melts': [], 'fumbles': [], 'burns': [], 'shatters': [], 'explode': {}} #Used in case items in inventory blow up
        self.getComponent('Knowledge').msg('updateKnowledge', {'type':'hp', 'data':None})
        self.movesThrough = self.movementRules()
        self.lastDamage = ""

    def movementRules(self):
        moveable = ['floor', 'water']
        return (moveable)

    def level(self):
        exp = self.getComponent('Experience')
        if exp:
            return exp.level
        return 1

    def getScore(self):
        return self.getComponent('Experience').exp

    def getRenderCode(self):
        if self.rendercode:
            return self.rendercode

        healthCode = self.getComponent('Health').getHealthCode()
        armorCode = self.getComponent('Inventory').getArmorCode()
        return 50 + healthCode + armorCode

    def getString(self):
        return self.name

    def getHealth(self):
        return self.getComponent('Health').hp

    def getMaxHealth(self):
        return self.getComponent('Health').maxHp

    def delayedMessage(self, message):
        if not message:
            return 
        self.messageBacklog.append(message)

    def releaseMessages(self):
        for message in self.messageBacklog:
            self.logMessage(message)
        self.messageBacklog = []

    def logMessage(self, message):
        if not message:
            return 
        know = self.getComponent('Knowledge')
        know.msgs.append(message)

    def hasRoom(self):
        if self.ai:
            if not self.ai.usesInventory():
                return False

        inventory = self.getComponent('Inventory')
        return not inventory.isFull()

    def usingItemType(self):
        if not 'item' in self.intent.keys():
            return [None, None]
        itemNum = self.intent['item']
        if itemNum == 0:
            return [None, None]
        inventory = self.getComponent('Inventory')
        item = inventory.getItem(itemNum)
        itemType = None
        if item != None:
            itemType = item.itemType()
        return [item, itemType]
        
    def adjustIntent(self):
        #Input is transformed from the standard ASDF set to more context-specific action
        [item, itemType] = self.usingItemType()
        inventory = self.getComponent('Inventory')
        
        if self.intent['type'] == 'apply':
            if itemType == 'potion':
                self.intent['type'] = 'drink'
            if itemType == 'pickaxe':
                self.intent['type'] = 'dig'

        if self.intent['type'] == 'spell':
            self.intent['type'] = 'switch'

        if self.intent['type'] == 'drop':
            if inventory.isEquipped(item):
                self.intent['type'] = 'apply'

        if self.intent['type'] == 'fire':
            if itemType == 'wand':
                self.intent['type'] = 'zap'
            else:
                self.intent['type'] = 'throw'

        
    def resetIntent(self):
        self.intent = {'type':'move', 'item':0, 'direction':[0, 0], 'target':None}

    def getAttackWord(self):
        if self.ai:
            aiaw = self.ai.aiaw()
            if aiaw:
                return aiaw
        return 'smacks'

    def getDuckWord(self):
        if self.ai:
            aidw = self.ai.aidw()
            if aidw:
                return aidw
        return "duck"

    def getEvadeWord(self):
        if self.ai:
            aiew = self.ai.aiew()
            if aiew:
                return aiew
        l = self.level()
        if l == 1:
            return "stumble away from"
        elif l == 2:
            return "flee from"
        elif l == 3:
            return "crouch away from"
        else:
            return "roll away from"

    def meleeWeapon(self):
        #Returns a string
        if self.ai:
            aimw = self.ai.meleeWeapon()
            if aimw:
                return aimw
        inventory = self.getComponent('Inventory')
        if inventory.equipped['weapon']:
            return inventory.equipped['weapon'].name
        else:
            return ('bare fists')

    def specialMeleeAttack(self):
        if self.ai:
            return self.ai.specialMeleeAttack()
        equipped = self.getComponent('Inventory').equipped
        if equipped['weapon']:
            return equipped['weapon'].specialMeleeAttack()
        return None

    def getPower(self, attackType):
        equipment = self.getComponent('Inventory').equipped 
        if attackType in self.basePower.keys():
            power = self.basePower[attackType]
        for slot in equipment:
            if equipment[slot] != None:
                if attackType in equipment[slot].powerModifiers.keys():
                    power = power + equipment[slot].powerModifiers[attackType]
        if power < 1:
            power = 1
        return power

    def defenseForType(self, attackType):
        defense = 0
        if attackType in self.baseDefense.keys():
            defense = self.baseDefense[attackType]
        equipment = self.getComponent('Inventory').equipped 
        for slot in equipment:
            if equipment[slot] != None:
                keys = equipment[slot].defenseModifiers.keys()
                if attackType in equipment[slot].defenseModifiers.keys():
                    defense = defense + equipment[slot].defenseModifiers[attackType]
        return defense

    def takeDamage(self, attackType, power):
        defense = 0
        if attackType in self.baseDefense.keys():
            defense = self.baseDefense[attackType]
        defense = defense + self.defenseForType(attackType)
        defense = randint(0, defense)
        power = power - defense
        if power < 0:
            power = 0
        health = self.getHealth()
        if power > health:
            power = health
        if power != 0:
            self.msg('take-damage', power)
        self.getComponent('Knowledge').msg('updateKnowledge', {'type':'hp', 'data':None})
        return power

    def specialMeleeHit(self, target):
        return randint(0,4) == 0
