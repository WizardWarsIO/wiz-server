from ..item import *
from random import randint

class FangDagger(Weapon):
    def specialMeleeAttack(self):
        return ['venom', {'power': 4, 'owner': self.owner}]