from level import *

class Maze(Level):
  def levelName(self):
    return "Marble Maze"

  # Some false walls

  def addSpecialRooms(self, game, worldMap):
    for i in range(3):
        for j in range(10):
            placing = random.choice(self.pieces())
            self.placeRoom(game, worldMap, placing, [5 + (i * 8), 5 + (j * 3)])

  def pieces(self):
    return([
        ['        ',
         ' ### # #'
         '  #   # '],

        [' ## ##  ',
         '#  # # #',
         '    ### '],

        [' # ## #  ',
         '   ##  ##',
         ' # ## #  '],

        [' #   #   ',
         '  #   ## ',
         '   #   # '],

        ['   #   # ',
         '  #   ## ',
         ' ##  #   '],

        [' # ##### ',
         ' #     # ',
         ' ##### # '],

        ['  # # #  ',
         ' ### ### ',
         '  # # #  '],

        ['  # # #  ',
         ' # # # # ',
         '  # # #  '],

        ['  ### #  ',
         '  #   #  ',
         '  # ###  '],

        [' # # # # ',
         ' # # # # ',
         ' # # # # '],

        [' ####### ',
         '         ',
         ' ####### '],

        [' # ### # ',
         ' # ### # ',
         ' # ### # '],

        ['         ',
         ' ####### ',
         '         ']
        ])

  def winConditionComponent(self):
    return Timed

  def winConditionConfig(self):
    return {'time': 888}

  def itemMakerMaps(self):
    return {
      'ATTACK_ITEMS': {
        'lightning wand': 4,
        'fire potion': 3,
        'acid potion': 1,
        'poison potion': 1,
        'stone wand': 8,
        'warp wand': 2,
        'spark scepter': 6,
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
        # 'stone wand': 2,
        'leather vest': 1,
        'faraday mesh': 1,
        'short sword': 3,
        'x-ray goggles': 1,
        'pickaxe': 2,
        'obsidian boots': 1,
        'warp wand': 1,
        'iron boots': 1},
        
     'STARTING_EQUIPMENT': {
        'leather vest': 2,
        'rubber armor': 1,
        'faraday mesh': 2,
        'short sword': 3,
        'trick wand': 3,
        'warp wand': 1},

      'STARTING_TOOLS': {
        'x-ray goggles': 2,
        'gas mask': 2,
        'pickaxe': 4},

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
        'short sword': 3}
    }

  def mapDetails(self):
    return {'minWallRate': 4, 'maxWallRate': 12, 'brokenWalls': 30}

  def itemMakerDelays(self):
    return {
            'STARTING_EQUIPMENT': 1,
            'STARTING_TOOLS': 1,
            'ATTACK_ITEMS': 1,
            'MINIMUM_ARMOR': 1,
            'MINIMUM_WEAPONS': 200,
            'MINIMUM_TOOLS': 1,
            'BONUS_ATTACK_ITEMS': 1,
            'BONUS_EQUIPMENT': 200}

  def itemMakerDelayResets(self):
    return {
            'STARTING_EQUIPMENT': 1000,
            'STARTING_TOOLS': 10000,
            'ATTACK_ITEMS': 160,
            'MINIMUM_ARMOR': 600,
            'MINIMUM_WEAPONS': 400,
            'MINIMUM_TOOLS': 1000,
            'BONUS_ATTACK_ITEMS': 1000,
            'BONUS_EQUIPMENT': 1000}

  def worldMapParams(self):
    return {'MAP_WIDTH':34, 'MAP_HEIGHT':40, 'DEPTH':5, 'MIN_SIZE':3, 'FULL_ROOMS':False}

  def defaultItemNames(self):
    names = []
    return names      

  def minimumMonsters(self):
    return 25

  def monsterWeights(self):
    return [
        ['orc', 30],
        ['giant', 4],
        ['minotaur', 1],
        ['spider', 10]]