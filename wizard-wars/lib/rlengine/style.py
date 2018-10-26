def darken(color, ratio):
  color = color.strip('#')
  r, g, b = int(color[:2], 16), int(color[2:4], 16), int(color[4:], 16)

  r = clamp(r * ratio)
  g = clamp(g * ratio)
  b = clamp(b * ratio)
  newcolor = "#%02x%02x%02x" % (r, g, b)
  
  return newcolor

def greenify(color, ratio):
  color = color.strip('#')
  r, g, b = int(color[:2], 16), int(color[2:4], 16), int(color[4:], 16)

  g = ratio * 255
  r = clamp(r * ratio)
  b = clamp(b * ratio)

  newcolor = "#%02x%02x%02x" % (r, g, b)
  
  return newcolor

def clamp(val, minimum=0, maximum=255):
  if val < minimum:
      return minimum
  if val > maximum:
      return maximum
  return val

def checker(oldtile):
  tile = dict(oldtile)
  if 'checker' in tile.keys():
    style = tile['checker']
  else:
    style = None
  if style == None:
    return tile
  elif style == 0:
    if 'checkerbg' in tile.keys():
      tile['bgcolor'] = tile['checkerbg']
    else:
      tile['bgcolor'] = darken(tile['bgcolor'], .95)
    return tile
  else:
    tile['symbol'] = style
    if 'checkercolor' in tile.keys():
      tile['color'] = tile['checkercolor']
    else:
      tile['color'] = darken(tile['bgcolor'], .9)
    return tile

def occlude(oldtile, ratio):
  tile = dict(oldtile)
  tile['bgcolor'] = darken(tile['bgcolor'], ratio)
  tile['color'] = darken(tile['color'], ratio)
  return tile

def fire(tile):
  new = dict(tile)
  new['bgcolor'] = '#ff1100'
  new['checker'] = 0
  new['checkerbg'] = "#ff4200"
  return new

def poison(tile):
  new = dict(tile)
  new['bgcolor'] = greenify(new['bgcolor'], .9)
  return new

def acid(tile):
  new = dict(tile)
  new['bgcolor'] = '#ffff00'
  return new

class Style():
  @staticmethod
  def itemMap():
   return {
      'fire potion':150, 'poison potion':151, 'acid potion':152, 'healing potion':153,
      'lightning wand':160,
      'stone wand':161, 'warp wand': 162, 'spark scepter': 163, 'trick wand': 164,
      'inferno wand': 165,
      'short sword':170, 'long sword':171, 'melt mace': 172, 'fang dagger': 173,
      'plate armor':180, 'faraday mesh':181, 'rubber armor':182, 'leather vest':183,
      'obsidian boots': 184, 'combat boots': 185, 'iron boots': 186,
      'x-ray goggles':190, 'gas mask':191,
      'pickaxe':201,
      'poison': 'poison',
      'fire': 'fire',
      'acid': 'acid'
      }

  @staticmethod
  def guide(params):
    at = 0x40
    asterisk = 0x2A

    scheme = params['scheme']
    metal = 'AliceBlue'
        
    style = {
      0: {'symbol': 127, 'color': "gold", 'bgcolor': "black"},
      
      #Default health colors, no armor
      50: {'symbol': at, 'color': 'white', 'bgcolor': 'darkgreen'},
      51: {'symbol': at, 'color': 'white', 'bgcolor': 'darkorange'},
      52: {'symbol': at, 'color': 'white', 'bgcolor': 'darkred'},

      #Metal armor
      55: {'symbol': at, 'color': 'darkgreen', 'bgcolor': 'grey'},
      56: {'symbol': at, 'color': 'darkorange', 'bgcolor': 'grey'},
      57: {'symbol': at, 'color': 'darkred', 'bgcolor': 'grey'},

      #Faraday armor
      60: {'symbol': at, 'color': 'darkgreen', 'bgcolor': 'LightSkyBlue'},
      61: {'symbol': at, 'color': 'darkorange', 'bgcolor': 'LightSkyBlue'},
      62: {'symbol': at, 'color': 'darkred', 'bgcolor': 'LightSkyBlue'},

      #Rubber armor
      65: {'symbol': at, 'color': 'darkgreen', 'bgcolor': 'yellow'},
      66: {'symbol': at, 'color': 'darkorange', 'bgcolor': 'yellow'},
      67: {'symbol': at, 'color': 'darkred', 'bgcolor': 'yellow'},

      #Leather armor
      70: {'symbol': at, 'color': 'darkgreen', 'bgcolor': 'brown'},
      71: {'symbol': at, 'color': 'darkorange', 'bgcolor': 'brown'},
      72: {'symbol': at, 'color': 'darkred', 'bgcolor': 'brown'},

      #Corpses
      123:   {'symbol': 9760, 'color': "white", 'bgcolor': None},

      # Monsters
      #orc
      130: {'symbol': ord('o'), 'color': 'black', 'bgcolor': 'lawngreen'},
      #troll
      131: {'symbol': ord('T'), 'color': 'black', 'bgcolor': 'lawngreen'},
      #Minotaur
      132: {'symbol': 547, 'color': 'black', 'bgcolor': 'lawngreen'},
      #Bat
      133: {'symbol': 612, 'color': 'black', 'bgcolor': 'lawngreen'},
      #Imp
      134: {'symbol': 502, 'color': 'red', 'bgcolor': 'black'},
      #Witch - 9446?
      135: {'symbol': 9446, 'color': 'black', 'bgcolor': 'lawngreen'},
      #Ninja
      136: {'symbol': 8523, 'color': 'black', 'bgcolor': None},
      #Serpent
      137: {'symbol': 8375, 'color': 'lawngreen', 'bgcolor': None},
      #Giant
      138: {'symbol': ord('G'), 'color': 'black', 'bgcolor': 'brown'},
      #Spider
      139: {'symbol': 8903, 'color': 'black', 'bgcolor': None},
      #Zombie
      140: {'symbol': ord('Z'), 'color': 'black', 'bgcolor': 'lawngreen'},
      #Priest
      141: {'symbol': ord('@'), 'color': 'gold', 'bgcolor': 'black'},

      #Potions
      150: {'symbol': 9905, 'color': "orange", 'bgcolor': None},
      151: {'symbol': 9905, 'color': "greenyellow", 'bgcolor': None},
      152: {'symbol': 9905, 'color': "yellow", 'bgcolor': None},
      153: {'symbol': 9905, 'color': "royalblue", 'bgcolor': None},

      #Wands
      160: {'symbol': 47, 'color': "yellow", 'bgcolor': None},
      161: {'symbol': 47, 'color': "brown", 'bgcolor': None},
      162: {'symbol': 47, 'color': "pink", 'bgcolor': None},
      163: {'symbol': 47, 'color': 'blue', 'bgcolor': None},
      164: {'symbol': 47, 'color': 'orange', 'bgcolor': None},
      165: {'symbol': 47, 'color': 'red', 'bgcolor': None},
      #Weapons
      170: {'symbol': 8601, 'color': metal, 'bgcolor': None},
      171: {'symbol': 8600, 'color': metal, 'bgcolor': None},
      172: {'symbol': 8601, 'color': 'gold', 'bgcolor': None},
      173: {'symbol': 8601, 'color': 'lawngreen', 'bgcolor': None},

      #Armor
      180: {'symbol': 920, 'color': "black", 'bgcolor': 'grey'},
      181: {'symbol': 920, 'color': "black", 'bgcolor': 'LightSkyBlue'},
      182: {'symbol': 920, 'color': "black", 'bgcolor': 'yellow'},
      183: {'symbol': 920, 'color': "black", 'bgcolor': 'brown'},
      
      # Boots
      184: {'symbol': 8372, 'color': "red", 'bgcolor': 'black'},
      185: {'symbol': 8372, 'color': "green", 'bgcolor': None},
      186: {'symbol': 8372, 'color': metal, 'bgcolor': 'grey'},

      #Goggles
      190: {'symbol': 8734, 'color': "red", 'bgcolor': None},
      191: {'symbol': 8734, 'color': metal, 'bgcolor': None},

      #Pickaxe:
      201: {'symbol': 9935, 'color': metal, 'bgcolor': None},

      #Remote bomb, control
      202: {'symbol': 9864, 'color': metal, 'bgcolor': None},
      203: {'symbol': 8268, 'color': metal, 'bgcolor': None},

      #Bots
      300:  {'symbol': 84, 'color': "orange", 'bgcolor': None},
      301:  {'symbol': 111, 'color': "green", 'bgcolor': None},


      #Turret
      400:  {'symbol': 8916, 'color': metal, 'bgcolor': None},

      #Boulder
      401:  {'symbol': 8857, 'color': 'brown', 'bgcolor': None},
      #Spark Orb
      402:  {'symbol': 8277, 'color': 'blue', 'bgcolor': None},

      #Hole
      33: {'symbol': 8718, 'color': "black", 'bgcolor': None},


      "lightning": {'symbol': 991, 'color': "gold"},
      "chaos": {'symbol': 63, 'color': "green"},
      "warp": {'symbol': 8258, 'color': "gold"},
       

      "poison": {'bgcolor': 'green'},
      "acid": {'bgcolor': 'yellow'},
      "fire": {'bgcolor': 'orange'}}


    style.update(scheme)
         

    #Checkering
    for i in range(1, 10):
      if i in style.keys():
        new = style[i]
        style[i+10] = checker(new)
        style[i+500] = poison(new)
        style[i+520] = fire(new)
        style[i+540] = acid(new)

    for i in range(1, 10):  #2nd pass for Explosion checkering
      if i in style.keys():
        new = style[i]
        style[i+510] = checker(poison(new))
        style[i+530] = checker(fire(new))
        style[i+550] = checker(acid(new))
        

    #Occluding
    for j in range(1, 20):
      if j in style.keys():
        new = dict(style[j])
        style[j+20] = occlude(new, style['occlusionFactor'])


    return(style)
