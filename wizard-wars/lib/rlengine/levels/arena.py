from level import *

class Arena(Level):
  def levelName(self):
    return "Acrid Arena"

  def worldMapParams(self):
    return {'MAP_WIDTH':49, 'MAP_HEIGHT':40, 'DEPTH':2, 'MIN_SIZE':10, 'FULL_ROOMS':True, 'wall_peppering':0}

  def style(self):
    return {
      1: {'symbol': 127, 'color': "#D4AF37", 'bgcolor': '#c46d23', 'checker':0},
      2: {'symbol': 127, 'color': "#D4AF37", 'bgcolor': '#c57e33','checker':0},
      3: {'symbol': 127, 'color': "#D4AF37", 'bgcolor': '#778e5e', 'checker':0},
      4: {'symbol': 127, 'color': "#D4AF37", 'bgcolor': '#b7b27b', 'checker':None},

      #Wall
      5: {'symbol': 127, 'color': "#D4AF37", 'bgcolor': '#cecece', 'blocksight':True},
      #Torch
      6: {'symbol': 9798, 'color': "#ff9d1e", 'bgcolor': '#b25c1e', 'blocksight':False, 'name':'candelabra'},
      #Skull wall
      7: {'symbol': 9760, 'color': "#D4AF37", 'bgcolor': '#b25c1e', 'blocksight':True, 'name': 'skeleton'},
      8: {'symbol': 127, 'color': "#D4AF37", 'bgcolor': '#D4AF37', 'blocksight':True}, 'name': 'skeleton',
 
      'occlusionFactor':0.5
    }


  def addSpecialRooms(self, game, worldMap):
    self.placeRoom(game, worldMap, self.arena(), [0, 0])

  def items(self):
    return {
            'a': [8, 'warp wand'],
            'p': [1, 'plate mail'],
            'l': [1, 'long sword'],
            's': [8, 'stone wand'],
            't': [1, 'spinny turret'],
            'x': [1, 'x-ray goggles'],
            'p': [1, 'plate armor'],
            'f': [1, 'fang dagger']
            }
  def monsters(self):
    return {
            'g': [1, 'giant'],
            'w': [1, 'witch'],
            'i': [1, 'imp']}

# 48x35
  def arena(self):
    return [
            '555555555555555555555555555555555555555555555555',
            '555555555555555555888ffffff888555555555555555555',
            '55555555555555555568   66  f65555555555555555555',
            '555555555555555555afp5    5lfa555555555555555555',
            '555555555555555555wap5fwwf5law555555555555555555',
            '55556777777777777766666  66666777777777777765555',
            '55556777777777777766666  66666777777777777765555',
            '55556777777777777776666  66667777777777777765555',
            '55556777777777777777666  66677777777777777765555',
            '55556777777777777777766  66777777777777777765555',
            '55556777777777777777776  67777777777777777765555',
            '55555555555555555555555  55555555555555555555555',
            '5555                         6555555555555555555',
            '5555               t          55555ss55555555555',
            '5555  t                       55555ii55555555555',
            '5555                          555555555555555555',
            '5555                          555555555555555555',
            '5555                          555555555555555555',
            '5555       6666666666666      6555555555555555555',
            '5555       66666666666665555555555555555555555555',
            '5555                   6      6     655555555555',
            '5555                   6             55555555555',
            '5555       6           6   t     i   55555555555',
            '5555       6     t     6             55555555555',
            '5555       6           6             55555555555',
            '5555       6                         55555555555',
            '5555                                        5555',
            '5555                                 66     5555',
            '5555555566666666666666666666666      666    5555',
            '5555555566666666666666666666666      666    5555',
            '55555555   i             i 6         66     5555',
            '55555555          6        6                5555',
            '55555555          6    t   6i      t 55555555555',
            '5555a555          6        6         55555555555',
            '5555a555          6                  55555555555',
            '55555555                             55555555555',
            '55555555                             55555555555',
            '555555555555555555555555555555555555555555555555',
            '555555555555555555555555555555555555555555555555',
            '555555555555555555555555555555555555555555555555']

  def winConditionComponent(self):
    return Timed

  def winConditionConfig(self):
    return {'time': 555}

  def itemMakerMaps(self):
    return {
      'ATTACK_ITEMS': {
        'lightning wand': 8,
        'fire potion': 8,
        'acid potion': 1,
        'stone wand': 6,
        'spark scepter': 4,
        'inferno wand': 1},

     'STARTING_EQUIPMENT': {
        'leather vest': 4,
        'rubber armor': 2,
        'faraday mesh': 1,
        'short sword': 3,
        'trick wand': 2,
        'warp wand': 1,
        'obsidian boots': 2},
      'BONUS_EQUIPMENT': {
        'warp wand': 4,
        'fire potion': 4
      },

      'MINIMUM_TOOLS': {
        'pickaxe': 1},

      'MINIMUM_ARMOR': {
        'healing potion': 1,
        'plate armor': 1,
        'faraday mesh': 1,
        'rubber armor': 1,
        'leather vest': 2},

     'MINIMUM_WEAPONS': {
        'long sword': 1,
        'short sword': 3}
    }

  def itemMakerDelays(self):
    return {
            'STARTING_EQUIPMENT': 1,
            'ATTACK_ITEMS': 1,
            'MINIMUM_ARMOR': 30,
            'MINIMUM_WEAPONS': 30,
            'BONUS_EQUIPMENT': 300}

  def itemMakerDelayResets(self):
    return {
            'STARTING_EQUIPMENT': 1000,
            'ATTACK_ITEMS': 45,
            'MINIMUM_ARMOR': 600,
            'MINIMUM_WEAPONS': 400,
            'BONUS_EQUIPMENT': 300}

  def defaultItemNames(self):
    names = ['bomb pair', 'bomb pair', 'pickaxe']
    return names      

  def minimumMonsters(self):
    return 8

  def monsterWeights(self):
    return [
        ['imp', 7],
        ['witch', 2]]
