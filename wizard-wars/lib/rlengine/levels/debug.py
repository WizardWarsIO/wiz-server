from level import *

class Debug(Level):
  def levelName(self):
    return "Debug Domain"

  def mapDetails(self):
    return {'minWallRate': 4, 'maxWallRate': 12, 'brokenWalls': 30}

  def itemMakerMaps(self):
    return {
      'DEBUG_ITEMS': {
        'fang dagger': 4,
        'spark scepter': 14,
        'fire potion': 10,
        'inferno wand': 5,
        'plate armor': 13,
        'x-ray goggles': 13,
        'obsidian boots': 13,
        'long sword': 13}}

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
    return {'MAP_WIDTH':30, 'MAP_HEIGHT':30, 'DEPTH':5, 'MIN_SIZE':2, 'wall_peppering': 0, 'FULL_ROOMS':True}
