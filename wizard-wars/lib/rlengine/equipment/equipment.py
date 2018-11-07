from ..item import *
from random import randint

class Weapon(Item):
    def configure(self, params):
        super(Weapon, self).configure(params)
        self.type = 'weapon'

        self.powerModifiers = params['powerModifiers']
        self.defenseModifiers = params['defenseModifiers']

    def specialMeleeAttack(self):
        return None

    def getString(self):
        return self.name

    def handleMessage(self, name, value):
        if name == 'explodedacid':
            if self.name in ['long sword', 'short sword']:
                self.melt()
        elif name == 'collide-avatar':
            special = self.specialMeleeAttack()
            target = value
            if special:
                [specialName, specialParams] = special
                target.msg(specialName, specialParams)

class CorrosiveCutlass(Weapon):
    def specialMeleeAttack(self):
        return ['explodedacid', {'power': 7, 'owner': self.owner}]

class FangDagger(Weapon):
    def specialMeleeAttack(self):
        return ['venom', {'power': 4, 'owner': self.owner}]

class Armor(Item):
    def configure(self, params):
        super(Armor, self).configure(params)
        self.type = self.defaultType()
        self.powerModifiers = params['powerModifiers']
        self.defenseModifiers = params['defenseModifiers']

    def defaultType(self):
        return 'armor'

    def renderOffset(self):
        armorCodes = {'plate armor':5, 'faraday mesh':10, 'rubber armor':15, 'leather vest':20}
        if self.name in armorCodes.keys():
            return armorCodes[self.name]
        return 0

    def handleMessage(self, name, params):
        if name == 'explodedacid':
            if self.name in ['plate armor', 'faraday mesh', 'obsidian boots',
            'iron boots', 'combat boots']:
                self.melt()
        elif name == 'explodedfire':
            if self.name in ['leather vest', 'gas mask', 'x-ray goggles']:
                self.burn()
        elif name == 'boulder-impact':
            self.shatter()

class Boots(Armor):
    def defaultType(self):
        return 'boots'