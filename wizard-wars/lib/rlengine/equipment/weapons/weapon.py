from ..item import *
from random import randint

class Weapon(Item):
    def configure(self, params):
        super(Weapon, self).configure(params)
        self.type = 'weapon'
        self.powerModifiers = self.defaultPowerModifiers()
        self.defenseModifiers = self.defaultDefenseModifiers()

    def defaultDefenseModifiers(self):
        return {}

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