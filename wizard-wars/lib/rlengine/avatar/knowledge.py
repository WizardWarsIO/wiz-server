from ..entity import *
from events.witness import *

class Knowledge(Entity):
    def configure(self, params):
        self.owner = params['owner']
        self.clear()

    def defaultComponents(self, params):
        return [[Witness, {'owner': params['owner']}]]

    def clear(self):
        self.msgs = []
        self.events = {}
        self.mapView = []
        self.inventory = []
        self.eqIndexes = {'face': 0, 'armor': 0, 'boots': 0, 'weapon': 0}
        self.eq = []
        self.hp = {'hp':0, 'max':0}
        self.moved = [0,0]
        self.path = None
        self.targetObject = None
        self.newPath = False
   
    def handleMessage(self, name, value):    
        if name == 'wipe':
            self.msgs = []

        if name == 'updateKnowledge':
            knowledgeType = value['type']
            data = value['data']

            if knowledgeType == 'hp':
                self.hp = {'hp':self.owner.getHealth(), 'max':self.owner.getMaxHealth()}

            if knowledgeType == 'view':
                self.mapView = data
                self.moved = self.owner.moved

            if knowledgeType == 'inventory':
                self.inventory = []
                inventory = self.owner.getComponent('Inventory')
                self.eqIndexes = inventory.eqIndexes
                inv = inventory.items 
                for index in inv:
                    if inv[index]:
                        equipped = False
                        if inv[index].type in inventory.equipped.keys():
                            if inv[index] == inventory.equipped[inv[index].type]:
                                equipped = True
                        self.inventory.append([inv[index].getString(), equipped, inv[index].getRenderCode()])
            
            if knowledgeType == 'equipped':                
                inv = data.items

            if knowledgeType == 'events':
                self.events = data
                witness = self.getComponent('Witness')
                witness.msg('witness', data)

            if knowledgeType == 'path':
                self.path = data['path']
                self.targetObject = data['object']
                self.newPath = True