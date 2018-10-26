from zapwitness import *
from smackwitness import *
from dropwitness import *
from deathwitness import *
from throwwitness import *
from explosionwitness import *
from meltwitness import *
from fumblewitness import *
from burnwitness import *
from shatterwitness import *
from ...entity import *

class Witness(Entity):
  def configure(self, params):
    self.owner = params['owner']
    
  def defaultComponents(self, params):
    return [
      [ZapWitness, {}],
      [SmackWitness, {}],
      [DropWitness, {}],
      [DeathWitness, {}],
      [MeltWitness, {}],
      [ThrowWitness, {}],
      [ExplosionWitness, {}],
      [FumbleWitness, {}],
      [BurnWitness, {}],
      [ShatterWitness, {}]
    ]

  def handleMessage(self, name, value):
    if name == 'witness':
      for eventType in value:
        self.msg(eventType, {'events': value[eventType], 'owner': self.owner})
