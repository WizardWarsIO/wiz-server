from ..item import *
from random import randint

class CorrosiveCutlass(Weapon):
    def specialMeleeAttack(self):
        return ['explodedacid', {'power': 7, 'owner': self.owner}]