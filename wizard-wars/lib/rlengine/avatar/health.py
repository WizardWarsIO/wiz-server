from ..entity import *
from random import randint

class Health(Entity):
  def configure(self, params):
    self.hp = params['HP']
    self.owner = params['owner']
    self.maxHp = self.hp
    self.heals = 0
    self.poison = 0
    self.poisonHurt = 0
    self.poisonDamage = 1
    self.previousPoisonDamage = 0
    self.venom = 0
    self.venomAttacker = None

  def destruction(self):
    super(Health, self).destruction()
    self.venomAttacker = None

  def heal(self, amount):
    self.hp = self.hp + amount
    if self.hp > self.maxHp:
      self.hp = self.maxHp        
    self.owner.msg('updateKnowledge', {'type':'hp', 'data':None})

  def getHealthCode(self):
    if self.hp >= 49:
      return 0
    if self.hp >= 10:
      return 1
    
    return 2

  def takeDamage(self, value):
    if value <= 0:
      return
    self.owner.events['hurts'] = True
    self.hp = self.hp - value
    self.owner.msg('updateKnowledge', {'type':'hp', 'data':None})

  def handleMessage(self, name, value):
    if name == 'levelup':
      self.heals = self.heals + (10 + value)
      if value < 12:
        ratio = self.hp / (self.maxHp * 1.0)
        self.maxHp = self.maxHp + 10
        self.hp = int(ratio * self.maxHp)

    if name == 'heal':
      self.heals = self.heals + value['power']

    if name == 'take-damage':
      self.takeDamage(value)

    if name == 'poison':
      self.poisonHurt = 2

      poisonDefense = self.owner.defenseForType('poison')
      if poisonDefense > 0:
        self.owner.delayedMessage('You breathe harmlessly.')
        self.poisonHurt = 0
        self.poisonDamage = 1
        self.poison = 0
        self.previousPoisonDamage = 0
        return

      self.poison = self.poison + 1
      damageDealt = self.poisonDamage + self.previousPoisonDamage - 1
      damageDealt = self.owner.takeDamage('poison', damageDealt)      

      if value != self.owner:
        value.msg('score', damageDealt)

      if damageDealt == 0:
        self.owner.delayedMessage('Your lungs start to burn.')
      else:
        self.owner.delayedMessage('You cough up poison for ' + str(damageDealt) + ' damage!')
        self.owner.lastDamage = "poison"

      previous = self.previousPoisonDamage
      self.previousPoisonDamage = self.poisonDamage
      self.poisonDamage = previous + self.poisonDamage

    if name == 'venom':
      venomDefense = self.owner.defenseForType('venom')
      venomPower = value['power']
      venomOwner = value['owner']
      self.venom = self.venom + max(0, venomPower - venomDefense)
      self.venomAttacker = venomOwner
    elif name == 'venom-foot':
      venomDefense = self.owner.defenseForType('venom-foot')
      venomPower = value['power']
      venomOwner = value['owner']
      self.venom = self.venom + max(0, venomPower - venomDefense)
      self.venomAttacker = venomOwner
    elif name == 'loop':
      if self.venom > 0:
        self.owner.delayedMessage('Venom courses through your veins.')
        self.owner.takeDamage('venom', self.venom)
        if (self.venomAttacker):
          self.venomAttacker.msg('score', self.venom)
        self.owner.lastDamage = "venom"

        if randint(0, 2) < 2:
          self.venom = self.venom - 1      

      if self.heals > 0 and self.hp > 0:
        self.heals = self.heals - 1
        self.heal(5)

      if self.poison > 0:
        if self.poisonHurt > 0:
          self.poisonHurt = self.poisonHurt - 1
        else:
          self.poison = self.poison - 1
          if self.poison < 1:
            self.poisonDamage = 1
            self.previousPoisonDamage = 0