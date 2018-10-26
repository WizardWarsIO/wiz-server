from wand import *
# from enviornmental import ice

class IceWand(Wand):
  def name(self):
    return "Frost"

  def effect(self, avatar):
    return {'type': 'frost', 'power': 1}

  def spawn(self, avatar):
    return [Ice, {}]

  def spawnPattern(self):
    return 'line'