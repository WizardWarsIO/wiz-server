from ..entity import *
from random import randint

class MeleeProcessor(Entity):
    def handleMessage(self, name, value):
        if name == 'processMelees':
            avatars = value['avatars']
            self.events = {'smacks':[]}
            self.addedItems = []
            smackList = []
            
            for avatar in avatars:
                if avatar.intent['type'] == 'melee':
                    [dx, dy] = avatar.intent['direction']
                    target = avatar.intent['target']
                    if target.x == avatar.x + dx and target.y == avatar.y + dy:
                        attackPower = avatar.getPower('direct')
                        special = avatar.specialMeleeAttack()
                        if special:
                            [specialName, specialParams] = special
                            target.msg(specialName, specialParams)

                        avatar.msg('attack', {'target':target, 'type':'direct'})
                        target.msg('attacked', {'assailant':avatar, 'type':'direct', 'power':attackPower})
                    else:
                        attackPower = avatar.getPower('swipe')
                        special = avatar.specialMeleeAttack()
                        if special:
                            if avatar.specialMeleeHit(target):
                                [specialName, specialParams] = special
                                target.msg(specialName, specialParams)

                        avatar.msg('attack', {'target':target, 'type':'swipe'})
                        target.msg('attacked', {'assailant':avatar, 'type':'swipe', 'power':attackPower})
                    smackList.append({'originator':avatar, 'name':target, 'affectedSpaces':[[avatar.x + dx, avatar.y + dy], [avatar.x, avatar.y]]})
                    avatar.intent['type'] = 'move' 
            self.events = {'smacks':smackList}
