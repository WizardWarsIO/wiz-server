from ..entity import *

class Eyeballs(Entity):
    def configure(self, params):
        self.owner = params['owner']
        self.blind = False
        self.torch_radius = 10
        self.xray = False

