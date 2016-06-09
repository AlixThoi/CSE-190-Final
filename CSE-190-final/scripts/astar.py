# astar implementation needs to go here
from copy import deepcopy, copy
from heapq import *

from read_config import *

def astar(move_list,mapSize,start,goal,walls,pits,cost):


    # traverse part
    frontier = []
    visited = []

    h = manhattanDistance(start,goal)

    c = cost
    # print  c
    heappush(frontier, (c+h,  [start]))
    # print "pass1"
    visited.append(start)

    while len(frontier) != 0:
        currentState = heappop(frontier)  # (f,tie,[pathlist])   frontier
        nk = currentState[-1][-1]  #  element

        if nk == goal:
            movement = currentState[-1]
            return movement

        else:

            for move in move_list:
                cur = deepcopy(nk)
                next = addTwoPoint(cur,move)
                if next not in walls and next not in pits and next[0]>=0 and next[0]<mapSize[0] and next[1]>=0 and next[1]<mapSize[1]:
                    # if next not in visited:
                    temp = deepcopy(currentState[-1])  # [pathlist]
                    temp.append(next)


                    heappush(frontier, (manhattanDistance(next, goal)+cost*len(temp), temp))


    return

def manhattanDistance (start,goal):
    return abs(start[0]-goal[0])+abs(start[1]-goal[1])

def addTwoPoint(p1,p2):
    return [p1[0]+p2[0],p1[1]+p2[1]]