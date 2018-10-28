from style import *
from entity import *
from item import *
from itemmaker import *
from items.items import *
from world.world import *
from avatar.avatar import *
from game import *
from levels.levels import *
from random import randint

class RoguelikeClient(Entity):
    def configure(self, params):
      Item.styleMap = self.itemStyleMap()
      self.loadLevelRotation()

    def defaultLevels(self):
      return [Temple]

    def loadLevelRotation(self):
      self.levelIndex = 0
      self.levelRotation = []
      for levelName in self.defaultLevels():
        level = levelName()
        print "adding level " + str(level) + " to rotation"
        self.levelRotation.append(level)

    def level(self):
      self.levelIndex = self.levelIndex % len(self.levelRotation)
      return self.levelRotation[self.levelIndex]

    def itemStyleMap(self):
      return Style.itemMap()

    def getPlayerByID(self, component, pid):
      for item in self.components:
          if type(item).__name__ == 'Avatar':
              if item.pid == pid:
                  return item
      return None

    def newAvatar(self, name, pid):
      player = self.getPlayerByID('Avatar', pid)
      if player:
          self.components.remove(player)
      self.setupNewComponents([[Avatar, {'name':name, 'pid':pid, 'race':'human', 'HP':50, 'basePower':{'direct':10, 'swipe':5}, 'baseDefense':{'direct':2, 'swipe':2, 'lightning':0}}]])
      return self.getPlayerByID('Avatar', pid)

    def enQueue(self, avatar, level):
      pass

# Pull worldmap + default items into level description object
    def worldMapParams(self):
      return self.level().worldMapParams()

    def defaultItemNames(self):
      return self.level().defaultItemNames()

    def makeDefaultItems(self, itemManager):
      names = self.defaultItemNames()
      for name in names:
        itemManager.msg('make', name)
      
      return itemManager.handleMessage('deliver', None)

    def scatterDefaultItems(self, game, toScatter):
      game.msg('scatterItems', {'items':toScatter, 'extantItems':[]})

    def sendFirstLoop(self, game):
      game.msg('loop', 1)

    def levels(self):
      return 

    def selectNewLevel(self):
      self.levelIndex = self.levelIndex + 1

    def targetWizards(self):
      return 0

    def currentGame(self):
      return self.getComponent('Game')

    def makeGame(self, params):
      gameID = params['gameID']
      self.selectNewLevel()
      level = self.level()
      print "Setting up with level" + str(level)
      avatarList = params['avatarList']
      if self.currentGame():
        self.components.remove(self.currentGame())
      self.setupNewComponents([[Game, {'gameID':gameID, 'level':level, 'targetWizards':self.targetWizards()}]])
      game = self.currentGame()
      game.setupNewComponents([[WorldMap, self.worldMapParams()]])
      worldMap = game.getComponent('WorldMap')
      itemManager = game.getComponent('ItemManager')
      self.styleGuide = Style.guide({'scheme':self.level().style()})
      level.makeMap(game, worldMap)

      defaultItems = self.makeDefaultItems(itemManager)
      defaultItems += avatarList
      toScatter = game.itemList + game.playerList + game.botList + defaultItems
      self.scatterDefaultItems(game, toScatter)

      startItems = level.extraItems
      for preSpawn in startItems:
        [[x, y], name] = preSpawn
        items = itemManager.handleMessage('spawn', [[name, x, y]])
        game.msg('placeItems', items)
        defaultItems += items

      startMons = level.extraMonsters
      for preSpawn in startMons:
        [[x, y], name] = preSpawn
        items = itemManager.handleMessage('spawn', [[name, x, y]])
        game.msg('placeMonster', items)
        defaultItems += items

      game.addObjects(defaultItems)

      self.sendFirstLoop(game)
      return game
      
