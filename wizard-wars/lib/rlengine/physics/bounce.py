from random import randint

class Bounce():
  @staticmethod
  def bounce(dx, dy, space, worldMap):
    ax = abs(dx)
    ay = abs(dy)
    if ax == 0 or ay == 0:
        if ay == 0:
          dx = -dx
        else:
          dy = -dy
        space = [space[0] + dx, space[1] + dy]
    else:
        # this is 7913 direction
        candidateH = [space[0] + dx, space[1]]
        candidateV = [space[0], space[1] + dy]

        blocked = 0
        if worldMap.isWall(candidateH):
            blocked = blocked + 1
        if worldMap.isWall(candidateV):
            blocked = blocked + 2

        if blocked == 0:
            blocked = 1
            if randint(0, 1) == 0:
                blocked = 2

        if blocked == 3:
            # both blocked, this hit a room corner
            dx = -dx
            dy = -dy
        elif blocked == 1:
            space = candidateV
            dx = -dx
        elif blocked == 2:
            space = candidateH
            dy = -dy

    return [space, dx, dy]