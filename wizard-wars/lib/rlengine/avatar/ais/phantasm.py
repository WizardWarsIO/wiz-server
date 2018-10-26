from ai import *
from random import randint
from ...items.wands.warp import *

class PhantasmAI(AIControls):
  def configure(self, params):
    super(PhantasmAI, self).configure(params)

  def aiaw(self):
    return 'taunts'

  def meleeWeapon(self):
    return 'ghostly whispers'

  def getIntent(self, x, y, visibleObjects):
    self.x = x
    self.y = y

    direction = [libtcod.random_get_int(0, -1, 1), libtcod.random_get_int(0, -1, 1)]
    return {'type':'nothing', 'item':0, 'direction': direction}

  







