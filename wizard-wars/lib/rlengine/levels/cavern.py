from level import *

class Cavern(Level):
  def levelName(self):
    return "Crud Cavern"

  def worldMapParams(self):
    return {'MAP_WIDTH':40, 'MAP_HEIGHT':40, 'DEPTH':4, 'MIN_SIZE':5, 'FULL_ROOMS':False, 'wall_peppering':8}

  def style(self):
    return {
      #Dirt floor
      1: {'symbol': 127, 'color': "#D4AF37", 'bgcolor': '#673301', 'checker':8278},
      2: {'symbol': 127, 'color': "#D4AF37", 'bgcolor': '#7fb5e8','checker':9926},
      3: {'symbol': 127, 'color': "#D4AF37", 'bgcolor': '#778e5e', 'checker':0},
      4: {'symbol': 127, 'color': "#D4AF37", 'bgcolor': '#b7b27b', 'checker':None},

      #Walls
      5: {'symbol': 127, 'color': "#D4AF37", 'bgcolor': '#8f9396', 'blocksight':True},
      #Stalagmites
      6: {'symbol': 9968, 'color': "#8f9396", 'bgcolor': '#673301', 'blocksight':True, 'name':'stalagmite'},
      7: {'symbol': 9840, 'color': "#D4AF37", 'bgcolor': '#0f5434', 'blocksight':True},
      8: {'symbol': 127, 'color': "#D4AF37", 'bgcolor': '#4e5653', 'blocksight':True},

      'occlusionFactor':.2
    }

  def itemMakerMaps(self):
    return {
      'ATTACK_ITEMS': {
        'lightning wand': 1,
        'fire potion': 1,
        'acid potion': 1,
        'poison potion': 1,
        'stone wand': 1,
        'warp wand': 2,
        'spark scepter': 2,
        'inferno wand': 1},

      'BONUS_ATTACK_ITEMS': {
        'trick wand': 1,
        'lightning wand': 2,
        'fire potion': 2,
        'acid potion': 2,
        'poison potion': 2,
        'warp wand': 2,
        'spark scepter': 1,
        'inferno wand': 1},

      'BONUS_EQUIPMENT': {
        'trick wand': 3,
        'leather vest': 1,
        'faraday mesh': 1,
        'short sword': 3,
        'rubber armor': 2,
        'x-ray goggles': 1,
        'gas mask': 1,
        'pickaxe': 2,
        'obsidian boots': 1,
        'warp wand': 1,
        'combat boots': 1,
        'iron boots': 1},
        
     'STARTING_EQUIPMENT': {
        'leather vest': 2,
        'rubber armor': 1,
        'faraday mesh': 1,
        'short sword': 3,
        'trick wand': 5,
        'warp wand': 1},

      'STARTING_TOOLS': {
        'x-ray goggles': 2,
        'gas mask': 2,
        'pickaxe': 8},

      'MINIMUM_TOOLS': {
        'x-ray goggles': 1,
        'gas mask': 1,
        'pickaxe': 1},

      'MINIMUM_ARMOR': {
        'healing potion': 1,
        'plate armor': 1,
        'faraday mesh': 1,
        'rubber armor': 1,
        'leather vest': 2},

     'MINIMUM_WEAPONS': {
        'long sword': 1,
        'short sword': 3,
        'minotaur': 10}
    }

  def itemMakerDelays(self):
    return {
            'STARTING_EQUIPMENT': 1,
            'STARTING_TOOLS': 1,
            'ATTACK_ITEMS': 1,
            'MINIMUM_ARMOR': 200,
            'MINIMUM_WEAPONS': 200,
            'MINIMUM_TOOLS': 400,
            'BONUS_ATTACK_ITEMS': 1,
            'BONUS_EQUIPMENT': 200}

  def itemMakerDelayResets(self):
    return {
            'STARTING_EQUIPMENT': 1000,
            'STARTING_TOOLS': 10000,
            'ATTACK_ITEMS': 150,
            'MINIMUM_ARMOR': 600,
            'MINIMUM_WEAPONS': 400,
            'MINIMUM_TOOLS': 1000,
            'BONUS_ATTACK_ITEMS': 1000,
            'BONUS_EQUIPMENT': 1000}

  
  def defaultItemNames(self):
    names = ['bomb pair', 'bomb pair', 'bomb pair', 'bomb pair', 
    'spinny turret', 'spinny turret', 'spinny turret', 'pickaxe',
    'pickaxe']
    return names      

  def minimumMonsters(self):
    return 16

  def monsterWeights(self):
    return [
        ['orc', 18],
        ['serpent', 3],
        ['troll', 8],
        ['minotaur', 1]]



  def winConditionComponent(self):
    return Timed

  def winConditionConfig(self):
    return {'time': 666}