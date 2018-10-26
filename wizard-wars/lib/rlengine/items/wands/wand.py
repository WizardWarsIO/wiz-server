from ...item import *

class Wand(Item):
    def configure(self, params):
        super(Wand, self).configure(params)
        self.type = 'wand'
        self.charges = self.charges()
        self.power = 5

    def charges(self):
        return 5

    def range(self, avatar):
        return 7 + avatar.level();

    def zapType(self):
        return "zapped"

    def effect(self, avatar):
        return {}

    def spawn(self, avatar):
        return None

    def itemType(self):
        return 'wand'
    
    def getModifier(self):
        return '(' + str(self.charges) + ')'

    def zap(self):
        self.charges = self.charges - 1
        if self.owner:
            self.owner.msg('updateKnowledge', {'type':'inventory', 'data':0})
        if self.charges <= 0:
            self.destruct()

    def explosion(self, avatar):
        return None

    def afterZap(self, affectedLines, worldMap):
        self.zap()

    def handleMessage(self, name, value):
        super(Wand, self).handleMessage(name, value)
        
        if name == "zap":
            self.zap()