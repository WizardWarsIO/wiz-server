from ...entity import *
import random

class EventWitness(Entity):
  def topic(self):
    pass

  def processEvent(self, name, originator):
    pass

  def handleMessage(self, name, value):
    if name == self.topic():
      seenOriginators   = []
      owner             = value['owner']
      events            = value['events']
      seenEvents = []
      for event in events:
        name        = event['name']
        if name == 'none':
          continue
        originator  = event['originator']
        if originator not in seenEvents and originator != owner and name != owner:
          if self.topic in ['deaths', 'throws']:
            owner.delayedMessage(self.processEvent(name, originator))
          else:
            owner.logMessage(self.processEvent(name, originator))
          seenEvents.append(originator)

        if not isinstance(name, basestring):
          event['name'] = name.name

        event['originator'] = originator.name