from lib.rlengine.client import *
from random import randint

class Client(RoguelikeClient):
  def defaultLevels(self):
    return [Town, Cavern, Arena, Temple, Labyrinth, Bash]

#Randomize levels. Delete this function to go through defaultLevels in order.
  def selectNewLevel(self):
    oldIndex = self.levelIndex
    while (self.levelIndex == oldIndex):
      self.levelIndex = randint(0, len(self.levelRotation))

#Keeps the leaderboard populated with some minimum number of AI wizards
  def targetWizards(self):
    return 4