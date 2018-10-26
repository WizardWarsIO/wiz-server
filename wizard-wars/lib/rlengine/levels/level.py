from timed import *
from mapmaker import *
import random

class Level(object):
  def __init__(self):
    self.resetExtras()

  def resetExtras(self):
    self.extraItems = []
    self.extraMonsters = []

  def prepare(self):
    pass

  def uniqueBspRooms(self):
    return [
    # where row1 = "    XXXX    "
      # [row1, row2, row3],
      # room2..
    ]

  def makeMap(self, game, worldMap):
    MapMaker(game, worldMap, self.style())
    self.resetExtras()
    self.addSpecialRooms(game, worldMap)
    self.buildPerimeter(game, worldMap)


  def addSpecialRooms(self, game, worldMap):
    pass 

  def buildPerimeter(self, game, worldMap):
    for i in range(worldMap.MAP_WIDTH - 1):
      worldMap.makeWall(i, 0, 5, True)
      worldMap.makeWall(i, worldMap.MAP_HEIGHT - 1, 5, True)

    for j in range(worldMap.MAP_HEIGHT - 1):
      worldMap.makeWall(0, j, 5, True)
      worldMap.makeWall(worldMap.MAP_WIDTH - 1, j, 5, True)

  def style(self):
    return {
      1: {'symbol': 127, 'color': "#D4AF37", 'bgcolor': '#778899', 'checker':0},
      2: {'symbol': 127, 'color': "#D4AF37", 'bgcolor': '#7fb5e8','checker':9926},
      3: {'symbol': 127, 'color': "#D4AF37", 'bgcolor': '#778e5e', 'checker':0},
      4: {'symbol': 127, 'color': "#D4AF37", 'bgcolor': '#b7b27b', 'checker':None},

      #Wall
      5: {'symbol': 127, 'color': "#D4AF37", 'bgcolor': '#0f5434', 'blocksight':True},
      6: {'symbol': 127, 'color': "#D4AF37", 'bgcolor': '#31473d', 'blocksight':True},
      7: {'symbol': 9840, 'color': "#D4AF37", 'bgcolor': '#0f5434', 'blocksight':True},
      8: {'symbol': 127, 'color': "#D4AF37", 'bgcolor': '#4e5653', 'blocksight':True},

      'occlusionFactor':.7
    }

  def reverse(self, s):
    str = ""
    for i in s:
      str = i + str
    return str

  def vflip(self, room):
    r = list(room)
    r.reverse()
    return r

  def hflip(self, room):
    r = list(room)
    for row in r:
      row = self.reverse(row)
    return r

  def permuteSquareRooms(self, room):
    permutations = [room, self.vflip(room), self.hflip(room), self.vflip(self.hflip(room))]
    return permutations


  def placeRoom(self, game, worldMap, placing, coords):
    x = coords[0]
    y = coords[1]
    for j in range(len(placing)):
      for i in range(len(placing[0])):
        char = placing[j][i]
        if char == "#":
          worldMap.makeWall(x + i, y + j, 5, True)
        elif char == " ":
          worldMap.makeFloor(x + i, y + j, 1)
        elif char.isdigit():
          char = int(char)          
          if char < 5:
            worldMap.makeFloor(x + i, y + j, char)
          else:
            tile = self.style()[char]
            blocksight = tile['blocksight']
            name = 'wall'
            if 'name' in tile.keys():
              name = tile['name']
            worldMap.makeWall(x + i, y + j, char, blocksight, name)
        else:
          if char in self.items().keys():
            [tileChar, name] = self.items()[char]
            worldMap.makeFloor(x + i, y + j, tileChar)
            self.extraItems.append([[x+i, y+j], name])
          elif char in self.monsters().keys():
            [tileChar, name] = self.monsters()[char]
            worldMap.makeFloor(x + i, y + j, tileChar)
            self.extraMonsters.append([[x+i, y+j], name])

  def mapDetails(self):
    return {'uniqueRooms': self.uniqueBspRooms(), 'minWallRate': 0, 'maxWallRate': 8, 'brokenWalls': 0}

  def winConditionComponent(self):
    return Timed

  def winConditionConfig(self):
    return {'winConditionConfig': {'time': 777}}

  def itemManagerConfig(self):
    return {'item_maps': self.itemMakerMaps(),
            'item_delays': self.itemMakerDelays(),
            'item_delay_resets': self.itemMakerDelayResets(),
            'monster_weights': self.monsterWeights(),
            'minimum_monsters': self.minimumMonsters()}

  def items(self):
    return {}

  def monsters(self):
    return {}

  def itemMakerMaps(self):
    return {}

  def itemMakerDelays(self):
    return {}

  def itemMakerDelayResets(self):
    return {}

  def worldMapParams(self):
    return {'MAP_WIDTH':40, 'MAP_HEIGHT':40, 'DEPTH':4, 'MIN_SIZE':6, 'FULL_ROOMS':True, 'wall_peppering':0}

  def defaultItemNames(self):
    return []

  def minimumMonsters(self):
    return 0

  def monsterWeights(self):
    return []
