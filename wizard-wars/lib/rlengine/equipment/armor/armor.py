from ..item import *
from random import randint

class Armor(Item):
    def configure(self, params):
        super(Armor, self).configure(params)
        self.type = self.defaultType()
        self.powerModifiers = params['powerModifiers']
        self.defenseModifiers = params['defenseModifiers']

    def defaultType(self):
        return 'armor'

    def renderCodeOffset(self):
        return 0

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