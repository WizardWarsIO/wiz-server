from level import *

class Tower(Level):
  def levelName(self):
    return "Torment Tower"


# outer ring of procedural generation
# inner 2x2 grid of pieces
# spawn empty tiles at the border spaced apart from each other / access points

# 7 water # wall - fence
  def pieces(self):
    return([
        ['     ---    ',
         '     ---    ',
         '     ---    ',
         '     ---    ',
         '            ',
         '7# ##  ## #7',
         '7#  #  #  #7'
         '7#  #  #  #7'
         '7#        #7'
         '7#---  ---#7'
         '7          7',
         '            ',
         '###    #####',
         '  ##  ###  #',
         ' #    ###  #',
         ' ##  ####  #',
         ' ###       #',
         '        ####'
         ],

        ['            ',
         '###     ### ',
         '  ### ###   ',
         '     ###  --',
         ' #          ',
         ' ###  ##### ',
         '         #  '
         '  ----- ##  ',
         '        ##  '
         '####  ###  #'
         '   #      ##',
         '   #     ###',
         '#      #####',
         '#     ###  #',
         '##        ##',
         '#######  ###',
         ' ###        ',
         ' #  #  ## # ',
         ],

        ['888#####',
         '822#333#',
         '822#333#',
         '822##3##',
         '82222228',
         '888 8888',
         '        ',
         '           '
         ],     

        ['  ####  ',
         ' ##44## ',
         '##4444##',
         '##4444##',
         '2##44##2',
         '22222222',
         ' 22##22 ',
         '        '
         ], 

        ['#### 222',
         '#  # 222',
         '# ##  22',
         '        ',
         '2222 ###',
         '222  #  ',
         '222  # #',
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
    return {'time': 666}

  def itemMakerMaps(self):
    return {
      'ATTACK_ITEMS': {
        'lightning wand': 4,
        'fire potion': 2,
        'acid potion': 2,
        'poison potion': 2,
        'stone wand': 1,
        'spark scepter': 2,
        'warp wand': 2,
        'spark scepter': 2},

      'BONUS_ATTACK_ITEMS': {
        'trick wand': 1,
        },

      'BONUS_EQUIPMENT': {
        'leather vest': 2,
        'faraday mesh': 1,
        'short sword': 1,
        'rubber armor': 2,
        'x-ray goggles': 1,
        'gas mask': 1,
        'pickaxe': 2,
        'warp wand': 1,
        'combat boots': 1,
        'iron boots': 1},
        
     'STARTING_EQUIPMENT': {
        'healing potion': 3,
        'leather vest': 2,
        'rubber armor': 1,
        'faraday mesh': 1,
        'short sword': 3,
        'lightning wand': 5,
        'warp wand': 1},

      'STARTING_TOOLS': {
        'x-ray goggles': 2,
        'pickaxe': 4},

      'MINIMUM_TOOLS': {
        'x-ray goggles': 1,
        'pickaxe': 1},

      'MINIMUM_ARMOR': {
        'healing potion': 1,
        'plate armor': 2,
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

  def worldMapParams(self):
    return {'MAP_WIDTH':30, 'MAP_HEIGHT':30, 'DEPTH':7, 'MIN_SIZE':4, 'FULL_ROOMS':False}

  def defaultItemNames(self):
    names = ['spinny turret', 'spinny turret', 'spinny turret', 'spinny turret', 'spinny turret']
    return names      

  def minimumMonsters(self):
    return 20

  def monsterWeights(self):
    return [
        ['orc', 44],
        ['giant', 12],
        ['ninja', 6]]