from level import *

class Bash(Level):
  def levelName(self):
    return "Boulder Bash"

  def itemMakerMaps(self):
    return {
        'DEBUG_ITEMS': {
          'fire potion': 6,
          'stone wand': 7,
          'spark scepter': 3,
          'warp wand': 1}
          }

  def itemMakerDelays(self):
    return {
            'DEBUG_ITEMS': 10}

  def minimumMonsters(self):
    return 8

  def monsterWeights(self):
    return [['priest', 1],
            ['minotaur', 2],
            ['serpent', 5]]

  def itemMakerDelayResets(self):
    return {'DEBUG_ITEMS': 80}

  def winConditionComponent(self):
    return Timed

  def winConditionConfig(self):
    return {'time': 300}

  def worldMapParams(self):
    return {'MAP_WIDTH':30, 'MAP_HEIGHT':30, 'DEPTH':5, 'MIN_SIZE':2, 'wall_peppering': 0, 'FULL_ROOMS':True}
