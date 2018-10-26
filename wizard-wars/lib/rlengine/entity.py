import math

class Entity(object):
    def __init__(self, params = {}):
        self.active = True 
        self.type = 'entity'
        self.pickup = False 
        self.attackable = False
        self.pushable = False
        self.momentum = [0,0]
        self.components = []
        self.preSetup(params)
        self.setupDefaultComponents(params)
        self.configure(params)
        self.postConfigure(params)

    def destruction(self):
        for c in self.components:
            c.destruction()
        self.components = []

    def aligned(self, target):
        if target.x == self.x or target.y == self.y:
            return True
        dx = abs(target.x - self.x)
        dy = abs(target.y - self.y)
        return dx == dy

    def preSetup(self, params):
        pass

    def postConfigure(self, params):
        pass

    def setupDefaultComponents(self, params):
        for item in self.defaultComponents(params):
            componentName = item[0]
            componentParams = item[1]
            newItem = componentName(componentParams)
            self.components.append(newItem)

    def setupNewComponents(self, components):
        for item in components:
            componentName = item[0]
            componentParams = item[1]
            newItem = componentName(componentParams)
            self.components.append(newItem)            

    def addComponents(self, newComponents):
        for component in newComponents:
            self.components.append(component)

    def configure(self, arg):
        pass

    def defaultComponents(self, params):
        return []

    def msg(self, name, value):
        self.handleMessage(name, value)
        for item in self.components:
            item.msg(name, value)

    def getComponent(self, component):
        for item in self.components:
            if type(item).__name__ == component:
                return item 

    def getNamedComponent(self, component, name):
        for item in self.components:
            if type(item).__name__ == component:
                if item.name == name:
                    return item
        return None

    def getComponents(self, componentList):
        items = []
        for item in self.components:
            if type(item).__name__ in componentList:
                items.append(item)

        return items 

    def getTypes(self, parentType):
        items = []
        for item in self.components:
            if item.im_class.__name__ == parentType:
                items.append(item)

        return items 

    def moveTo(self, component, destination):
        self.components.remove(component)
        destination.addComponents[[component]]

    def clearInactive(self):
        toRemove = []
        for component in self.components:
            if component.active == False:
                toRemove.append(component)

        for c in toRemove:
            self.components.remove(c)
                
    def distanceTo(self, x, y, other):
        return(math.sqrt((x - other.x) ** 2 + (y - other.y) ** 2))

    def findClosest(self, x, y, others):
        closest = None 
        closestDistance = None 
        for obj in others:
            distance = self.distanceTo(x, y, obj)
            if obj != self and closestDistance == None or distance < closestDistance:
                closestDistance = distance
                closest = obj
        return [closest, closestDistance]

    def rotateDirection(self, direction, rotations):
        dirs = [[0, -1], [1, -1], [1, 0], [1, 1], [0, 1], [-1, 1], [-1, 0], [-1, -1]]
        index = dirs.index(direction)
        index = index + rotations
        if index < 0 or index > len(dirs) - 1:
            index = index % len(dirs)
        return dirs[index]

    @staticmethod
    def directions():
        return {5: [0,0], 8: [0, -1], 9: [1, -1], 6: [1, 0], 3: [1, 1], 2: [0, 1], 1: [-1, 1], 4: [-1, 0], 7: [-1, -1]}

    def numberDirection(self, direction):
        for num, vector in Entity.directions().items():
            if vector == direction:
                return num

        return 5

    def vectorForNum(self, num):
        return Entity.directions()[num]

    def vectorTowards(self, other):
        dx = other.x - self.x
        dy = other.y - self.y
        distance = self.distanceTo(self.x, self.y, other)
        if distance == 0:
            distance = 1
        dx = int(round( dx / distance))
        dy = int(round( dy / distance))
        return [dx, dy]

    def orthoTowards(self, other):
        [vx, vy] = self.vectorTowards(other)
        if abs(vx) > abs(vy):
            return [vx, 0]
        return [0, vy]


    def handleMessage(self, name, value):
        if name == 'loop':
            self.clearInactive()
