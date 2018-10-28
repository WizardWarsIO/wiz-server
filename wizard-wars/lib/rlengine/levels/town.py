from level import *

class Town(Level):
  def levelName(self):
    return "Tainted Town"

  def style(self):
    return {
      #Dirt:
      1: {'symbol': 127, 'color': "#D4AF37", 'bgcolor': '#b97a57', 'checker':None},
      #Grass:
      2: {'symbol': 127, 'color': "#D4AF37", 'bgcolor': '#22b14c','checker':8280},
      #Indoors
      3: {'symbol': 127, 'color': "#D4AF37", 'bgcolor': '#ff7f27', 'checker':9926},
      #Stone path:
      4: {'symbol': 127, 'color': "#D4AF37", 'bgcolor': '#c3c3c3', 'checker':0},

      #House Wall
      5: {'symbol': 127, 'color': "#D4AF37", 'bgcolor': '#880015', 'blocksight':True},
      #Symbol wall
      6: {'symbol': 9763, 'color': "#5cba37", 'bgcolor': '#880015', 'blocksight':True},
      #Water:
      7: {'symbol': 127, 'color': "#2cafc9", 'bgcolor': '#1f0faf', 'blocksight':False, 'checker':8767, 'checkercolor': "#2cafc9", 'name':'water'},
      #Fence on grass:
      8: {'symbol': 8917, 'color': "#7f4b10", 'bgcolor': '#22b14c', 'blocksight':False, 'name':'fence'},

      'occlusionFactor':.8
    }

  def items(self):
    return {'w': [3, 'stone wand'],
            'g': [3, 'gas mask'],
            'c': [7, 'melt mace'],
            'l': [4, 'leather vest'],
            'f': [4, 'fire potion'],
            's': [4, 'short sword'],
            'x': [4, 'x-ray goggles'],
            'p': [3, 'poison potion'],
            'o': [3, 'spark scepter'],
            'z': [7, 'fang dagger']
            }
            
  def monsters(self):
    return {'m': [1, 'orc']}

  def worldMapParams(self):
    return {'MAP_WIDTH':34, 'MAP_HEIGHT':40, 'DEPTH':5, 'MIN_SIZE':6, 'FULL_ROOMS':False, 'wall_peppering':0}


  def addSpecialRooms(self, game, worldMap):
    placing = random.choice(self.topStrip())
    self.placeRoom(game, worldMap, placing, [1, 0])
    placing = self.vflip(random.choice(self.topStrip()))
    self.placeRoom(game, worldMap, placing, [1, 32])
    placing = self.middleDirt()
    self.placeRoom(game, worldMap, placing, [3, 8])
    for i in range(3):
        for j in range(3):
            placing = random.choice(self.townPieces())
            placing = random.choice(self.permuteSquareRooms(placing))
            self.placeRoom(game, worldMap, placing, [3 + (i * 9), 8+ (j * 8)])

  def topStrip(self):
    return([
        [''],[''],
        ['55555555555555555555555555555555',
         '22222222222222222222222222222222',
         '22222222222222222222222222777777',
         '72277744777722222222222744777777',
         '77777744777c777722277777447     ',
         '77777    77777777777777         ',
         ' 77          777777777          ',
         '         mmmmmm                 ',
         ],

        ['55555555555555555555555555555555',
         '                                ',
         '         77777777777            ',
         '   7777777777777777777777777    ',
         '  7777777777777z77777777777     ',
         '    7777777777777777777mmm      ',
         '             777777777 mmm      ',
         '                                ',
         ]])

  def middleDirt(self):
    return(
        ['111111111111111111111111111' for i in range(25)
         ])

  def townPieces(self):
    return([
        [' 22 22  ',
         ' ##6### ',
         ' #p33p# ',
         ' #33333 ',
         ' #g#pp# ',
         ' ###### ',
         '        ',
         '        '
         ],

        ['888#####',
         '822#www#',
         '822#w3w#',
         '822##3##',
         '82222228',
         '888 8888',
         '        ',
         '        '
         ],     

        ['888#####',
         '822#ofo#',
         '822#o3o#',
         '822##3##',
         '82222228',
         '888 8888',
         '        ',
         '        '
         ],  

        ['  ####  ',
         ' ##xx## ',
         '##f44f##',
         '##f44f##',
         '2##44##2',
         '22222222',
         ' 22##22 ',
         '        '
         ], 

        ['#### 222',
         '# w# 222',
         '# ##  22',
         '        ',
         '2222 ###',
         '222  #  ',
         '222  #w#',
         '22   ###'
         ], 

        ['###2 222',
         '#2#2 222',
         '#2#2 222',
         '#2#2 222',
         '        ',
         '2222 222',
         '2222 222',
         '2222 222'
         ],  

        ['8882 888',
         '8222 228',
         '8882 888',
         '8222 228',
         '8882 888',
         '8222 228',
         '8882 888',
         '        '
         ], 

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
        'obsidian boots': 1,
        'warp wand': 1,
        'iron boots': 1},
        
     'STARTING_EQUIPMENT': {
        'leather vest': 2,
        'rubber armor': 1,
        'faraday mesh': 2,
        'trick wand': 3,
        'warp wand': 1},

      'STARTING_TOOLS': {
        'x-ray goggles': 0},

      'MINIMUM_TOOLS': {
        'x-ray goggles': 1},

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
            'ATTACK_ITEMS': 100,
            'MINIMUM_ARMOR': 200,
            'MINIMUM_WEAPONS': 200,
            'MINIMUM_TOOLS': 400,
            'BONUS_ATTACK_ITEMS': 1,
            'BONUS_EQUIPMENT': 200}

  def itemMakerDelayResets(self):
    return {
            'STARTING_EQUIPMENT': 1000,
            'STARTING_TOOLS': 10000,
            'ATTACK_ITEMS': 200,
            'MINIMUM_ARMOR': 600,
            'MINIMUM_WEAPONS': 400,
            'MINIMUM_TOOLS': 1000,
            'BONUS_ATTACK_ITEMS': 1000,
            'BONUS_EQUIPMENT': 1000}

  
  def defaultItemNames(self):
    names = []
    return names      

  def minimumMonsters(self):
    return 16

  def monsterWeights(self):
    return [
        ['orc', 30],
        ['ninja', 9],
        ['spider', 7]]