from level import *

class Debug(Level):
  def levelName(self):
    return "Debug Domain"

  def mapDetails(self):
    return {'minWallRate': 4, 'maxWallRate': 12, 'brokenWalls': 30}

  def itemMakerMaps(self):
    return {
      'DEBUG_ITEMS': {
        'lightning wand': 4,
        'fire potion': 4,
        'plate armor': 3,
        'gas mask': 1,
        'long sword': 3}}

  def itemMakerDelays(self):
    return {'DEBUG_ITEMS': 1}

  def minimumMonsters(self):
    return 0

  def monsterWeights(self):
    return [['giant', 1],
            ['orc', 1]]

  def itemMakerDelayResets(self):
    return {'DEBUG_ITEMS': 10}

  def winConditionComponent(self):
    return Timed

  def winConditionConfig(self):
    return {'time': 300}  


  def worldMapParams(self):
    return {'MAP_WIDTH':15, 'MAP_HEIGHT':30, 'DEPTH':1, 'MIN_SIZE':2, 'wall_peppering': 0, 'FULL_ROOMS':True}
