from actionupdater import *

class WarpUpdater(ActionUpdater):
  def topic(self):
    return 'warp'

  def processEvent(self, name, details, avatar):
    newCoordinate = details['wandEffect']['newCoordinate']
    moved = [newCoordinate[0] - avatar.x, newCoordinate[1] - avatar.y]
    avatar.moved = moved
    worldMap = details['worldMap']
    worldMap.moveItem(avatar, newCoordinate)
    avatar.logMessage('With a sickening lurch, you teleport.')
