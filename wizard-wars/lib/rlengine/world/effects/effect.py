from ...entity import *

class Effect(Entity):
  def configure(self, params):
    self.duration = params['duration']
    self.owner = params['owner']
    self.power = params['power']
    self.maxSpreads = -1
    if 'maxSpreads' in params.keys():
      self.maxSpreads = params['maxSpreads']
    if 'original' in params.keys():
      self.original = params['original']
    else:
      self.original = self

  def processEntity(self, entity):
    entity.msg(self.effectName(), {'type':self.effectType(), 'power':self.power, 'owner':self.owner})

  def effectName(self):
    return "exploded" + self.effectType()

  def effectType(self):
    pass

  def loop(self, value):
    if self.duration:
      self.duration -= 1

    if self.duration <= 0:
      self.active = False

    self.spread(value)

  def spread(self, value):
    [tile, worldMap] = value
    delay = self.spreadDelay()
    if self.active and self.maxSpreads != 0 and delay >= 0 and self.duration % delay == 0:
      for [dx, dy] in self.eightDirections():
        coord = [tile.x + dx, tile.y + dy]
        if not worldMap.beyondBoundary(coord):
          adjacent = worldMap.getTile(coord)
          if not adjacent.block_sight:
            worldMap.msg('spread', {'to':adjacent, 'create':{'type': self.effectType(),
              'duration': self.duration,
              'owner': self.owner,
              'power': self.power,
              'original': self.original,
              'maxSpreads' : self.maxSpreads - 1}})
  
  def spreadDelay(self):
    return -1

  def handleMessage(self, name, value):
    if name == 'maploop':
      self.loop(value)

    if name == 'processEntities':
      for item in value:
        self.processEntity(item)

  def eightDirections(self):
    return [ [-1, 0], [-1, -1], [0, -1], [1, -1], [1, 0], [1, 1], [0 ,1], [-1, -1]]



