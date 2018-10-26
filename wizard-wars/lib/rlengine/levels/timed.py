from ..entity import *

class Timed(Entity):
  def configure(self, params):
    super(Timed, self).configure(params)
    wcc = params['winConditionConfig']
    self.timeout = wcc['time']
    self.levelName = params['levelName']

  def isFinished(self):
    return self.timeout <= 0

  def currentStatus(self):
    return self.levelName + "  (TIME: " + str(self.timeout)  + ")"

  def handleMessage(self, name, value):
    if name == 'loop':
      self.timeout = self.timeout - 1
