from level import *

class Temple(Level):
  def levelName(self):
    return "Tortured Temple"

  def style(self):
    return {
      #Stone floor
      1: {'symbol': 127, 'color': "#D4AF37", 'bgcolor': '#778899', 'checker':0},
      #Carpet
      2: {'symbol': 127, 'color': "#a30d50", 'bgcolor': '#a30d50','checker':9926},
      3: {'symbol': 127, 'color': "#D4AF37", 'bgcolor': '#778e5e', 'checker':0},
      4: {'symbol': 127, 'color': "#D4AF37", 'bgcolor': '#b7b27b', 'checker':None},

      #Wall
      5: {'symbol': 127, 'color': "#D4AF37", 'bgcolor': '#0f5434', 'blocksight':True},
      #Torch
      6: {'symbol': 9798, 'color': "#ff9d1e", 'bgcolor': '#778899', 'blocksight':False, 'name':'candelabra'},
      #Rune wall
      7: {'symbol': 9772, 'color': "#D4AF37", 'bgcolor': '#0f5434', 'blocksight':True},
      #Bench
      8: {'symbol': 294, 'color': "#705e0d", 'bgcolor': '#778899', 'blocksight':False, 'name':'bench', 'checker':0},

      'occlusionFactor':.7
    }

  def worldMapParams(self):
    return {'MAP_WIDTH':60, 'MAP_HEIGHT':40, 'DEPTH':6, 'MIN_SIZE':3, 'FULL_ROOMS':True, 'wall_peppering':0}

  def addSpecialRooms(self, game, worldMap):
    outerEdge = random.choice(self.outerEdge())
    self.placeRoom(game, worldMap, outerEdge, [5, 5])

    secondLayer = random.choice(self.secondLayer())
    self.placeRoom(game, worldMap, secondLayer, [10, 10])

    innerLayer = random.choice(self.innerLayer())
    innerLayer = random.choice(self.permuteSquareRooms(innerLayer))
           
    self.placeRoom(game, worldMap, innerLayer, [20, 10])    

  def items(self):
    return {
            'g': [1, 'gas mask'],
            'c': [1, 'melt mace'],
            'l': [1, 'leather vest'],
            'c': [1, 'acid potion'],
            's': [1, 'short sword'],
            'x': [1, 'x-ray goggles'],
            'p': [1, 'poison potion'],
            'o': [1, 'spark scepter'],
            't': [1, 'faraday mesh'],
            'f': [1, 'fire potion'],
            'u': [1, 'fang dagger']
            }
  def monsters(self):
    return {
            'r': [1, 'serpent'],
            'w': [1, 'witch'],
            'z': [1, 'zombie']}

  def outerEdge(self): #50 by 30
    return([
        ['                                                  ',
         '  c# # # # # # # # # # # # # # # # # # # # # #c   ',
         '  l# # # # # # # # # # # # # # # # # # # # # #l   ',
         ' ### # # # # # # # # # # # # # # # # # # # # ###  ',
         '                                                  ',
         ' ###  /////////////////////////////////////  ###  ',
         '                                          /       ',
         ' ###                                      /  ###  ',
         '                                          /       ',
         ' ###                                      /  ###  ',
         '                                          /       ',
         ' ###                                      /  ###  ',
         '                                                  ',
         ' ###                                         ###  ',
         '                                                  ',
         ' ###                                         ###  ',
         '                                                  ',
         ' ###                                         ###  ',
         '                                                  ',
         ' ###                                         ###  ',
         '                                                  ',
         ' ###  /                                      ###  ',
         '      /                                           ',
         ' ###  /                                      ###  ',
         '      /                                           ',
         ' ###  //////////////////////                 ###  ',
         '                                                  ',
         ' ### # # # # # # # # # # # # # # # # # # # # ###  ',
         '   # # # # # # # # # # # # # # # # # # # # # #    ',
         '   # # # # # # # # # # # # # # # # # # # # # #    ',
         ],

        ['  ##zz##zz##  ##  ##  ##  ##  ##  ##  ##  ##      ',
         '  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##      ',
         '   ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##     ',
         '#   ##zz##zz##  ##  ##  ##  ##  ##  ##  ##  ##    ',
         '##                            z           z       ',
         ' ##   ///////////////////////////////////// ##    ',
         '  ##                                      /  ##   ',
         '#  ##                                     /   ####',
         '##                                        /    ###',
         ' ##                                       / ##    ',
         '  ##                                      /  ##   ',
         '#  ##                                     /   ####',
         '##                                          z  ###',
         ' ##                                         ##    ',
         '  ##                                         ##   ',
         '#  ##                                         ####',
         '##                                             ###',
         ' ##                                         ##    ',
         '  ##                                         ##   ',
         '#  ##                                         ####',
         '##                                          z  ###',
         ' ##   /                                     ##    ',
         '  ##  /                                      ##   ',
         '   ## /                                       ####',
         '      /                                        ###',
         ' ##   //////////////////////                ##    ',
         '  ##             z  z  z  z  z  z  z  z      ##   ',
         '   ####zz##  ##  ##  ##  ##  ##zz##  ##  ##   ####',
         '      ##  ##  ##  ##  ##  ##  ##  ##  ##  ##   ###',
         '       ##zz##  ##  ##  ##  ##  ##zz##  ##  ##     ',
         ],

         ])

  def secondLayer(self): #40 by 20
    return([
        ['          ////////////////////          ',
         '#7####7###/                   #7#####7##',
         ' 68o#o68  /                    68fo#o68 ',
         '    #     /                       f#ff  ',
         '          /                             ',
         '          /                             ',
         '          /                             ',
         '  ff#ff                          ff#ff  ',
         ' 68o#o68                        68o#o68 ',
         '##########                    ##7####7##',
         ' zzz#zzzz                     # 68 # 68 ',
         '    #zzzz                    /#    #    ',
         '                             /          ',
         '                             /          ',
         '                             /          ',
         '   c#c                       /    c#c   ',
         ' 68c#c68                     /  68c#c68 ',
         '#7####7###                   /##7####7##',
         '                //////////////          ',
         ],
         
        ['   ###     ///////////////////    ###   ',
         '  ##f##   /                  /   ##f##  ',
         ' ##fff##  /                     ##fff## ',
         ' #6 r     /                        r 6# ',
         ' ##fff##  /                     ##fff## ',
         '  ##f##   /                      ##f##  ',
         '   ###    /                       ###   ',
         '    #                              #    ',
         '    #                              #    ',
         '                                        ',
         '    #                              #    ',
         '    #                        /     #    ',
         '   ###                       /    ###   ',
         '  ##w##                      /   ##w##  ',
         ' ##   ##                     /  ##   ## ',
         ' #6                          /       6# ',
         ' ##   ##  /                  /  ##   ## ',
         '  ##t##   /                  /   ##t##  ',
         '   ###    ////////////////////    ###   ',
         ],

         ])


  def innerLayer(self): #20 by 20
    return([
        ['                    ',
         ' ####7########7#### ',
         ' #cccr   ff   rccc# ',
         ' #  ##r  ww  r##  # ',
         ' # ####      #### # ',
         ' #r####6 22 6####r# ',
         ' #  ##   22   ##  # ',
         ' #       22       # ',
         ' # 88888 22 88888 # ',
         '         22         ',
         '   88888 22 88888   ',
         ' #       22       # ',
         ' # 88888 22 88888 # ',
         ' #       22       # ',
         ' # 88888 22 88888 # ',
         ' #                # ',
         ' #ro  o  o  o  o r# ',
         ' ################## ',
         '                    ',
         ],

        ['####            ####',
         '###      ##      ###',
         '##      #77#      ##',
         '#      ##ww##      #',
         '      ##z  z##      ',
         '             ##     ',
         '    #    66   ##    ',
         '   ##          ##   ',
         '  ## zzzzzzzzzz ##  ',
         ' ##t 2222222222 c## ',
         ' ##u 2222222222 c## ',
         '  ## zzzzzzzzzz ##  ',
         '   ##          ##   ',
         ' z   ##zz 66zz      ',
         '  z   ##      #   z ',
         '#  z   ##z  z##z   #',
         '##  z   ##  ##  z ##',
         '###  z  #77#  z  ###',
         '####     ##     ####',
         ],

         ])

  def winConditionComponent(self):
    return Timed

  def winConditionConfig(self):
    return {'time': 888}

  def itemMakerMaps(self):
    return {
      'ATTACK_ITEMS': {
        'lightning wand': 20,
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
        'gas mask': 2},

      'MINIMUM_TOOLS': {
        'x-ray goggles': 1,
        'gas mask': 1},

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
    return 60

  def monsterWeights(self):
    return [
        ['orc', 7],
        ['witch', 9],
        ['serpent', 15],
        ['ninja', 9],
        ['priest', 4]
        ]


