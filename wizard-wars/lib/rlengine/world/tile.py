from ..entity import *
from effects.effects import *

class Tile(Entity):
    def configure(self, params):
        self.events = {}
        self.blocked = params['blocked']
        self.block_sight = params['block_sight']
        self.items_on = []
        self.name = 'wall'
        self.rendercode = 5 # default wall
        self.x = params['x']
        self.y = params['y']

    def getRendercode(self, visible):
    	if not visible or (self.components == []):
    		return self.rendercode
    	return self.rendercode + self.components[-1].getRendercode()

    def effectMap(self):
        return {
                'fire':FireEffect,
                'poison':PoisonEffect,
                'acid':AcidEffect
                }

    def handleMessage(self, name, value):
        if name == 'loop':
            worldMap = value
            self.clearInactive()
            self.msg('maploop', [self, worldMap])
            self.msg('processEntities', self.items_on)
            if self.name != 'floor':
                for item in self.items_on:
                    item.msg('standingon' + self.name, 0)

        if name == 'create':
            if 'original' in value.keys():
                for comp in self.components:
                    if hasattr(comp, 'original'):
                        if comp.original == value['original']:
                            return
            newComponent = self.effectMap()[value['type']]
            self.setupNewComponents([[newComponent, value]])