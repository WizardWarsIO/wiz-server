from ..entity import *

class Experience(Entity):
  def configure(self, params):
    self.owner = params['owner']
    self.level = 1
    self.exp = 0
    self.spendExp = 0 #easier calculation

  def requiredExp(self):
    return 25 * self.level

  def attemptLevelUp(self):
    ai = self.owner.ai
    if ai != None:
      return
      
    if self.spendExp > self.requiredExp():
      self.spendExp = self.spendExp - self.requiredExp()
      self.level = self.level + 1
      self.owner.basePower['direct'] = self.owner.basePower['direct'] + 1
      self.owner.msg('levelup', self.level)

  def handleMessage(self, name, value):
    if name == 'score':
      self.exp = self.exp + value
      self.spendExp = self.spendExp + value
      self.attemptLevelUp()