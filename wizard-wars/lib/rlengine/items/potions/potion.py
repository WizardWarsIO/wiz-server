from ...item import *

class Potion(Item):
    def configure(self, params):
        super(Potion, self).configure(params)
        self.type = 'potion'
        self.weight = 2
        self.potency = self.defaultPotency()

    def defaultPotency(self):
        return 20

    def land(self, value):
        self.pickup = False

    def drank(self, value):
        self.destruct()

    def handleMessage(self, name, value):
        if name == 'land':
            self.land(value)

        if name == 'drank':
            self.drank(value)

    def itemType(self):
        return 'potion'
        