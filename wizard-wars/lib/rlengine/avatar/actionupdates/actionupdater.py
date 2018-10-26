from ...entity import *

class ActionUpdater(Entity):    
  def configure(self, params):
    self.owner = params['owner']

  def topic(self):
    pass

  def processEvent(self, name, details, avatar):
    pass

  def handleMessage(self, name, details):
    if name == self.topic():
      self.processEvent(name, details, self.owner)