from bonk import *
from collided import *
from inputupdater import *
from aiinput import *
from attack import *
from attacked import *
from equip import *
from zapped import *
from dead import *
from pickup import *
from drop import *
from exploded import *
from poisoned import *
from struck import *
from leveled import *
from melted import *
from heal import *
from warp import *
from chaos import *
from chaosexplode import *
from drown import *
from boulder import *

class Nerves(Entity):
  def defaultComponents(self, params):
    return [
      [BonkUpdater, params],
      [CollidedUpdater, params],
      [InputUpdater, params],
      [AIInput, params],
      [AttackUpdater, params],
      [AttackedUpdater, params],
      [EquipUpdater, params],
      [ZappedUpdater, params],
      [DeadUpdater, params],
      [PickupUpdater, params],
      [DropUpdater, params],
      [ExplodedUpdater, params],
      [PoisonedUpdater, params],
      [StrikeUpdater, params],
      [LevelUpdater, params],
      [MeltedUpdater, params],
      [HealUpdater, params],
      [WarpUpdater, params],
      [ChaosUpdater, params],
      [ChaosExplodeUpdater, params],
      [DrownUpdater, params],
      [BoulderUpdater, params]
    ]