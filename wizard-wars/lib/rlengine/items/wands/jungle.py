from wand import *
# from enviornmental import thorns

class JungleWand(Wand):
  def name(self):
    return 'Jungle'

  def spawn(self, avatar):
    return [Thorn, {'direction': avatar.intent['direction'], 'duration': 10 + avatar.level}]
    # The Thorn class will, on loop, create another Thorn in the same direction with duration of -1

  def spawnPattern(self):
    return 1