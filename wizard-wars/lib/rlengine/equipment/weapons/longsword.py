from weapon import *

class LongSword(Weapon):
    def defaultPowerModifiers(self):
        return {'direct':17, 'swipe':8}