from entity import *
from items.items import *
from avatar.avatar import *
from avatar.ais.ais import *

class Factory(Entity):
    def specs(self):
        pass

    def handleMessage(self, name, value):
        if name == 'make':
            s = self.specs()
            hasSpec = value in s
            if hasSpec:
                specification = s[value]
                item = specification[0](specification[1])
                return item

class WandFactory(Factory):
    def specs(self):
        return {
            'lightning wand': [LightningWand, {}],
            'stone wand': [StoneWand, {}],
            'warp wand': [WarpWand, {}],
            'spark scepter': [OrbWand, {}],
            'trick wand': [ChaosWand, {}],
            'inferno wand': [FireWand, {}] 
        }

class PotionFactory(Factory):
    def specs(self):
        return {
            'fire potion': [FirePotion, {}],
            'poison potion': [PoisonPotion, {}],
            'healing potion': [HealingPotion, {}],
            'acid potion': [AcidPotion, {}]
        }

class ArmorFactory(Factory):
    def specs(self):
        return {
            'obsidian boots': [Boots, {'name': 'obsidian boots', 'powerModifiers': {},
                'defenseModifiers': {'fire': 60, 'venom-foot': 100}}],
            'leather vest': [Armor, {'name': 'leather vest', 'powerModifiers': {}, 
            'defenseModifiers': {'direct': 9, 'swipe': 4, 'acid': 4}}],
            'plate armor': [Armor, {'name': 'plate armor', 'powerModifiers': {}, 'defenseModifiers': 
            {'direct':22, 'swipe':6}}],
            'faraday mesh': [Armor, {'name': 'faraday mesh', 'powerModifiers': {}, 
            'defenseModifiers': {'direct':1, 'swipe':1, 'lightning':100}}],
            'rubber armor': [Armor, {'name': 'rubber armor', 'powerModifiers': {}, 'defenseModifiers': 
            {'direct':2, 'swipe':1, 'acid':36, 'water':10}}],
            'combat boots': [Boots, {'name': 'combat boots', 'powerModifiers': {'direct': 6, 'swipe': 1}, 
            'defenseModifiers': {'direct': 4, 'venom-foot': 100}}],
            'iron boots': [Boots, {'name': 'iron boots', 'powerModifiers': {}, 
            'defenseModifiers': {'direct': 7, 'swipe': 2, 'venom-foot': 100}}]
        }

class WeaponFactory(Factory):
    def specs(self):
        return {
            'long sword': [Weapon, {'name': 'long sword', 'powerModifiers': 
            {'direct':17, 'swipe':8}, 'defenseModifiers': {}}],
            'short sword': [Weapon, {'name': 'short sword', 'powerModifiers': 
            {'direct':10, 'swipe':3}, 'defenseModifiers': {}}],
            'melt mace': [CorrosiveCutlass, {'name': 'melt mace', 'powerModifiers': 
            {'direct':4, 'swipe':2}, 'defenseModifiers': {}}],
            'fang dagger': [FangDagger, {'name': 'fang dagger', 'powerModifiers': 
            {'direct':-8, 'swipe':-4}, 'defenseModifiers': {}}],
        }

class ToolFactory(Factory):
    def specs(self):
        return {
            'x-ray goggles': [XrayGoggles, {'name': 'x-ray goggles', 'defenseModifiers': {'acid': 15}}],
            'pickaxe': [Pickaxe, {'name': 'pickaxe'}],
            'gas mask': [GasMask, {'name': 'gas mask', 'defenseModifiers': {'swipe': 1, 'poison': 9999, 'acid': 30}}]
        }

class ExplosivesFactory(Factory):
    def specs(self):
        return {
            'remote bomb': [RemoteBomb, {}],
            'remote control': [RemoteControl, {}]
        }

class TurretFactory(Factory):
    def specs(self):
        return {
            'constant turret': [Turret, {'beam':'lightning', 'behavior':'constant'}],
            'spinny turret': [Turret, {'beam':'lightning', 'behavior':'spin'}]
        }

class MonsterFactory(Factory):
    def specs(self):
        return {
            'orc': OrcAI,
            'troll': TrollAI,
            'minotaur': MinotaurAI,
            'bat': BatAI,
            'imp': ImpAI,  
            'witch': WitchAI,
            'ninja': NinjaAI,
            'serpent': SerpentAI,
            'giant': StoneGiantAI,
            'spider': SpiderAI,
            'zombie': ZombieAI,
            'wizard': WizardAI,
            'priest': PriestAI,
        }

    def handleMessage(self, name, value):
        if name == 'make':
                s = self.specs()
                hasSpec = value in s
                if hasSpec:
                    aiclass = self.specs()[value]
                    ai = aiclass()
                    avatar = Avatar({'rendercode': ai.renderCode(), 'name': ai.name, 'race': ai.race(), 'HP': ai.health(), 'basePower': ai.basePower(), 'baseDefense': ai.baseDefense()})
                    avatar.installAI(ai)
                    return avatar

class ItemMaker(Entity):
      def configure(self, args):
        self.products = []

      def handleMessage(self, name, value):

        if name == 'make':
            itemName = value[0]
            location = value[1]
        
            if value == 'bomb pair':
                efactory = self.getComponent('ExplosivesFactory')
                item1 = efactory.handleMessage(name, 'remote bomb')
                item2 = efactory.handleMessage(name, 'remote control')
                item1.pair = item2
                item2.pair = item1
                self.products.append(item1)
                self.products.append(item2)
            else:
                for factory in self.components:
                    item = factory.handleMessage(name, value)
                    if item:
                        self.products.append(item)
        if name == 'make1':
            for factory in self.components:
                    item = factory.handleMessage('make', value)
                    if item:
                        return item



      def defaultComponents(self, params):
        return [
        [WandFactory, {}],
        [PotionFactory, {}],
        [ArmorFactory, {}],
        [WeaponFactory, {}],
        [ToolFactory, {}],
        [ExplosivesFactory, {}],
        [TurretFactory, {}],
        [MonsterFactory, {}]
        ]
