from ..entity import *
from zapprocessor import *
from movementprocessor import *
from meleeprocessor import *
from ballisticprocessor import *
from explosionprocessor import *
from avatarmanager import *
from spawnprocessor import *

class TurnProcessor(Entity):
    def defaultComponents(self, params):
        return [
                [ZapProcessor, {}],
                [MovementProcessor, {}],
                [MeleeProcessor, {}],
                [BallisticProcessor, {}],
                [ExplosionProcessor, {}],
                [AvatarManager, {}],
                [SpawnProcessor, {}]
                ]

    def handleMessage(self, name, value):
        if name == 'processIntents':
            self.addedItems = []
            self.spawnList = []
            avatars = value['avatars']
            items = value['items']
            worldMap = value['map']
            [zapProcessor, movementProcessor, meleeProcessor, ballisticProcessor, explosionProcessor, avatarManager, spawnProcessor] = self.components

            self.events = {'zaps':[], 'attacks':[], 'throws':[], 'collisions':[], 'hurts':[]}

            #Aggregate intents
            intentList = []
            for avatar in avatars:
                avatar.moved = [0,0]
                if avatar.dead == False:
                    avatar.adjustIntent()
                    intentList.append({'originator':avatar, 'intent':avatar.intent})

            avatars = [avatar for avatar in avatars if avatar.dead == False]
            objects = {'map':worldMap, 'avatars':avatars, 'items':items}

            def runTurn(processor, triggerMsg):
                processor.msg(triggerMsg, objects)
                self.events.update(processor.events)
                self.addedItems += processor.addedItems

            turn = [[zapProcessor, 'startProcess'],
                    [movementProcessor, 'processMoves'],
                    [meleeProcessor, 'processMelees'],
                    [zapProcessor, 'endProcess'],
                    [ballisticProcessor, 'processBallistics'],
                    [explosionProcessor, 'processExplosions'],
                    [avatarManager, 'processAvatars']
                    ]

            for item in turn:
                runTurn(item[0], item[1])

            spawnProcessor.msg('process', objects)
            self.events.update(spawnProcessor.events)
            self.spawnList += spawnProcessor.spawnList
