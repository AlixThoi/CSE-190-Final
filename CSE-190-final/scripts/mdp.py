# mdp implementation needs to go here
import copy

from read_config import *
class mdp:
    def __init__(self):
        self.move_list = read_config()["move_list"]
        self.mapSize = read_config()["map_size"]
        self.start = read_config()["start"]
        self.goal = read_config()["goal"]
        self.walls = read_config()["walls"]
        self.pits = read_config()["pits"]
        self.cost = read_config()["reward_for_each_step"]

        self.goalReward = read_config()["reward_for_reaching_goal"]
        self.pitReward = read_config()["reward_for_falling_in_pit"]
        self.wallReward = read_config()["reward_for_hitting_wall"]

        self.factor = read_config()['discount_factor']
        self.move_foward = read_config()["prob_move_forward"]
        self.move_left = read_config()["prob_move_left"]
        self.move_right = read_config()["prob_move_right"]
        self.move_backward = read_config()["prob_move_backward"]
        self.iteration = read_config() ["max_iterations"]
        self.diff = read_config()[ "threshold_difference"]

        self.MDPmap = []
        self. moveString = {(0, 1):"E",
                            (0, -1):"W",
                            (1, 0):"S",
                            (-1, 0):"N"}

        for row in range(0,self.mapSize[0]): #[3,4]
            tempRow  = []
            for column in range(0,self.mapSize[1]): #x
                tempRow.append([float(0),"Empty"])
            self.MDPmap.append(tempRow)


        self.MDPmap[self.goal[0]][self.goal[1]] =[self.goalReward,"GOAL"]
        for wall in self.walls:
            self.MDPmap[wall[0]][wall[1]] = [self.wallReward,"WALL"]

        for pit in self.pits:
            self.MDPmap[pit[0]][pit[1]]=[self.pitReward,"PIT"]



    def isAValiable(self,x,y):
        if [x,y] in self.pits:
            return False
        if [x,y] in self.walls:
            return False
        if self.goal[0] == x and self.goal[1]==y:
            return False
        return True


    def isHitWall(self,nextState):

        if nextState in self.walls:
            return True
        if nextState[0]<0 or nextState[0]>=self.mapSize[0] or nextState[1]<0 or nextState[1]>=self.mapSize[1]:
            return True
        return False


    def iterativeValue(self,x,y):

        value = [float("-inf"),"Empty"]

        for item in self.move_list:
            #forward
            nextFoward = [x+item[0],y+item[1]]
            reward = self.cost
            if self.isHitWall(nextFoward):
                nextFoward = [x,y]
                reward=self.wallReward

            vForward = self.move_foward*(reward+self.factor*self.MDPmap[nextFoward[0]][nextFoward[1]][0])
            # if(x ==1 and y ==2):
            #     print "for:", vForward
            #left
            reward= self.cost
            if item[0]==0:
                nextLeft= [x-item[1],y-item[0]]
                nextRight = [x+item[1],y+item[0]]
            else:
                nextLeft = [x+item[1],y+item[0]]
                nextRight = [x-item[1],y-item[0]]

            if self.isHitWall(nextLeft):
                nextLeft = [x,y]
                reward = self.wallReward
            vLeft = self.move_left*(reward+self.factor*self.MDPmap[nextLeft[0]][nextLeft[1]][0])
            # if (x == 1 and y == 2):
            #     print "l:",vLeft

            #right
            reward = self.cost
            if self.isHitWall(nextRight):
                nextRight  = [x,y]
                reward = self.wallReward
            vRight = self.move_right*(reward+self.factor*self.MDPmap[nextRight[0]][nextRight[1]][0])
            # if (x == 1 and y == 2):
            #     print "r:",vRight

            sumV = vForward+vLeft+vRight
            # if (x == 1 and y == 2):
            #     print "sum:" ,sumV
            if(sumV>value[0]):
                value = [sumV,self.moveString[(item[0],item[1])]]
            # if (x == 1 and y == 2):
            #     print "val:", value

        return value



    def looping(self):
        for iter in range (0,self.iteration):
            # print "iter:", iter
           
            tempMap = copy.deepcopy(self.MDPmap)
            diffirence  = 0
            for row in range (self.mapSize[0]):
                for col in range(self.mapSize[1]):
                    if self.isAValiable(row,col):
                        val = self.iterativeValue(row,col)
                        tempMap[row][col] = val
                        diffirence+=abs(self.MDPmap[row][col][0]-tempMap[row][col][0])


            self.MDPmap = tempMap

            if diffirence<= self.diff:
                # print "out", iter
                break
            diffirence = 0

        return self.MDPmap
















    def convertToList(self):
        l = []
        for row in range(0,self.mapSize[0]):
            for col in range(0,self.mapSize[1]):
              l.append(self.MDPmap[row][col][1])

        return l

    def printthing(self):
        # print self.MDPmap

        for row in self.MDPmap:
            l = []
            for column in row:
                # print column.bestPolicy[0]
                l.append(column[1])
            s = ' '.join(('%*s' % (7, i) for i in l))
            print s



x = mdp()
x.looping()
x.printthing()






