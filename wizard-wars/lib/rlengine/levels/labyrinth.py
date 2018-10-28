from level import *

class Labyrinth(Level):
  def levelName(self):
    return "Lewd Labyrinth"

  def style(self):
    return {
      1: {'symbol': 127, 'color': "#277AB6", 'bgcolor': '#277AB6', 'checker':0},
      2: {'symbol': 127, 'color': "#D4AF37", 'bgcolor': '#7fb5e8','checker':9926},
      3: {'symbol': 127, 'color': "#D4AF37", 'bgcolor': '#778e5e', 'checker':0},
      4: {'symbol': 127, 'color': "#D4AF37", 'bgcolor': '#b7b27b', 'checker':None},

      #Walls
      5: {'symbol': 127, 'color': "#D4AF37", 'bgcolor': '#052959', 'blocksight':True},
      #Stalagmites
      6: {'symbol': 9968, 'color': "#80ABE2", 'bgcolor': '#673301', 'blocksight':True},
      7: {'symbol': 9840, 'color': "#80ABE2", 'bgcolor': '#0f5434', 'blocksight':True},
      8: {'symbol': 127, 'color': "#80ABE2", 'bgcolor': '#4e5653', 'blocksight':True},

      'occlusionFactor': 0
    }


  def winConditionComponent(self):
    return Timed

  def winConditionConfig(self):
    return {'time': 777}

  def itemMakerMaps(self):
    return {
      'ATTACK_ITEMS': {
        'lightning wand': 3,
        'fire potion': 4,
        'acid potion': 3,
        'poison potion': 3,
        'warp wand': 2,
        'spark scepter': 4,
        'inferno wand': 2},

      'BONUS_ATTACK_ITEMS': {
        'trick wand': 1,
        'lightning wand': 3,
        'fire potion': 3,
        'acid potion': 3,
        'poison potion': 3,
        'warp wand': 3,
        'spark scepter': 1,
        'inferno wand': 1},

      'BONUS_EQUIPMENT': {
        'trick wand': 5,
        'leather vest': 2,
        'faraday mesh': 2,
        'short sword': 5,
        'rubber armor': 2,
        'x-ray goggles': 4,
        'gas mask': 1,
        'pickaxe': 2,
        'obsidian boots': 2,
        'warp wand': 3,
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
        'leather vest': 2,
        'bat': 30},

    'BATS': {
        'bat': 40,
    },

    'TROLLS': {
        'troll': 20
    },

     'MINIMUM_WEAPONS': {
        'long sword': 1,
        'short sword': 3}
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
            'BONUS_EQUIPMENT': 200,
            'BATS': 120,
            'TROLLS': 200}

  def itemMakerDelayResets(self):
    return {
            'STARTING_EQUIPMENT': 1000,
            'STARTING_TOOLS': 10000,
            'ATTACK_ITEMS': 150,
            'BATS': 800,
            'MINIMUM_ARMOR': 600,
            'MINIMUM_WEAPONS': 400,
            'MINIMUM_TOOLS': 1000,
            'BONUS_ATTACK_ITEMS': 1000,
            'BONUS_EQUIPMENT': 1000,
            'TROLLS': 400}

  def worldMapParams(self):
    return {'MAP_WIDTH':40, 'MAP_HEIGHT':40, 'DEPTH':14, 'wall_peppering':0, 'MIN_SIZE':2, 'FULL_ROOMS':True}

  def defaultItemNames(self):
    names = ['bomb pair', 'bomb pair', 'bomb pair', 'bomb pair', 
    'spinny turret', 'spinny turret', 'spinny turret']
    return names      

  def minimumMonsters(self):
    return 30

  def monsterWeights(self):
    return [
        ['witch', 7],
        ['orc', 16],
        ['minotaur', 12]]
