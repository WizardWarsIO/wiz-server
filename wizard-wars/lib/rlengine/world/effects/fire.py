from effect import * 

class FireEffect(Effect):
    def getRendercode(self):
        return 520

    def effectType(self):
        return "fire"

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
                  'duration': self.duration - 1,
                  'owner': self.owner,
                  'power': self.power,
                  'original': self.original,
                  'maxSpreads' : self.maxSpreads - 1}})
    
    def spreadDelay(self):
        return 1