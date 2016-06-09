# mdp implementation needs to go here
import copy

from read_config import *



class slot:
    walls = {}
    pits = {}
    goal = []

    @staticmethod
    def initialMap(wall,pit,goal):
        slot.walls  = wall
        slot.pits = pit
        slot.goal = goal


    def __init__(self,xpos,ypos):
        self.value = {"E":15.0,"W":15.0,"S":15.0,"N":15.0}
        self.time = {"E":1,"W":1,"S":1,"N":1}
        self.xpos = xpos
        self.ypos =ypos
        self.bestPolicy = ["",0.0]
        self.updatePolicy()
        self.isGoal()
        self.isWall()
        self.isPit()


    def isWall(self):
        if (self.xpos,self.ypos) in slot.walls:
            self.value = {"wall":0.0}
            self.bestPolicy = list(self.value)
            return True
        return False

    def isGoal(self):
        if self.xpos == slot.goal[0] and self.ypos==slot.goal[1]:
            self.value={"goal":10}
            self.bestPolicy = list(self.value)
            return True
        return False

    def isPit(self):
        if (self.xpos,self.ypos) in slot.pits:
            self.value={"pit":-10}
            self.bestPolicy =list(self.value)
            return True
        return False

    def updatePolicy(self):
        self.bestPolicy[0]= max(self.value, key=self.value.get)
        self.bestPolicy[1] = self.value[self.bestPolicy[0]]

    def updateValue(self,direction,value):
        self.value[direction.upper()] = value
        self.updatePolicy()
        self.time[direction.upper()] +=1


    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__



class QLearningLValue:
    def __init__(self):
        self.move_list = read_config()["move_list"]
        self.mapSize = read_config()["map_size"]
        self.start = read_config()["start"]

        self.goal = read_config()["goal"]
        self.walls = dict((tuple(el),0) for el in read_config()["walls"])
        self.pits =dict((tuple(el),0) for el in read_config()["pits"])

        self.cost = read_config()["reward_for_each_step"]

        self.goalReward = read_config()["reward_for_reaching_goal"]
        self.pitReward = read_config()["reward_for_falling_in_pit"]
        self.wallReward = read_config()["reward_for_hitting_wall"]

        self.factor = read_config()['discount_factor']
        self.alpha = 0.2
        self.c = 15.0


        # self.move_foward = read_config()["prob_move_forward"]
        # self.move_left = read_config()["prob_move_left"]
        # self.move_right = read_config()["prob_move_right"]
        # self.move_backward = read_config()["prob_move_backward"]


        self.iteration = read_config() ["max_iterations"]
        # self.diff = read_config()[ "threshold_difference"]

        self.QLearningMap = []
        self. moveString = {"E":(0, 1),
                            "W":(0, -1),
                            "S":(1, 0),
                            "N":(-1, 0)}
        slot.initialMap(self.walls,self.pits,self.goal)
        for row in range(0,self.mapSize[0]): #[3,4]
            tempRow  = []
            for column in range(0,self.mapSize[1]): #x
                tempRow.append(slot(row,column))
            self.QLearningMap.append(tempRow)



    def learning(self):
        for x in range(0,50000):
            self.run()
    def run(self):
        startState = self.QLearningMap[self.start[0]][self.start[1]]
        goalState = self.QLearningMap[self.goal[0]][self.goal[1]]
        keepGoing = True
        while (keepGoing):
            # if startState.isPit() or startState.isGoal():
            #     keepGoing =False
            #     if startState.isPit():
            #         newValue =
            #         startState.value = {"E":self.pitReward,"W":self.pitReward,"S":self.pitReward,"N":self.pitReward}
            #         startState.updatePolicy()
            #
            #     if startState.isGoal():
            #         startState.value = {"E":self.goalReward,"W":self.goalReward,"S":self.pitReward,"N":self.pitReward}
            #
            #
            #
            #     break

            policy = startState.bestPolicy
            move = self.movement(policy[0],startState)
            if move[0]==False:
                #update value
                # print "hit wall!"
                L = self.c/(startState.time[policy[0]])
                Q = (1-self.alpha)*policy[1]+ self.alpha*(self.wallReward+self.factor*policy[1])

                startState.updateValue(policy[0],L+Q)



            else:
                if move[1].isPit():
                    L = self.c / (startState.time[policy[0]] )
                    Q = (1 - self.alpha) * policy[1] + self.alpha * (self.cost+ self.factor * self.pitReward)
                    startState.updateValue(policy[0],L+Q)
                    break
                elif move[1].isGoal():
                    L = self.c / (startState.time[policy[0]] )
                    Q = (1 - self.alpha) * policy[1] + self.alpha * (self.cost + self.factor * self.goalReward)
                    startState.updateValue(policy[0], L + Q)
                    break


                else:
                    L = self.c / (startState.time[policy[0]] )
                    Q = (1 - self.alpha) * policy[1] + self.alpha * (self.cost + self.factor * move[1].bestPolicy[1])
                    startState.updateValue(policy[0], L + Q)
                    startState = move[1]


            # print startState






        # print policy

    def movement(self,direction,startState):

        [xpos,ypos] = [startState.xpos+self.moveString[direction][0],startState.ypos+self.moveString[direction][1]]
        if xpos<0 or xpos>=self.mapSize[0] or ypos<0 or ypos>=self.mapSize[1]:
            return (False,None)

        newState = self.QLearningMap[xpos][ypos]
        if newState.isWall():
            return (False,None)
        return (True, newState)





    def printThing(self):
        for row in self.QLearningMap:
            l = []
            for column in row:
                # print column.bestPolicy[0]
                l.append(column.bestPolicy[0])
            s =' '.join(('%*s' % (7, i) for i in l))
            print s

    def convertToList(self):
        l = []
        for row in self.QLearningMap:
            for column in row:
              l.append(column.bestPolicy[0].upper())

        return l

        # for row in self.QLearningMap:
        #     for column in row:
        #         print column
        #     print
        #
        # print  "pit:", slot.pits
        # print "goal:",slot.goal
        # print "wall:",slot.walls






x = QLearningLValue()
x.learning()
x.printThing()

print x.convertToList()








