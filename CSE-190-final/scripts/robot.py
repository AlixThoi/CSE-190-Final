#!/usr/bin/env python

#robot.py implementation goes here


import rospy

from read_config import *
from cse_190_assi_3.msg import AStarPath, PolicyList
from astar import *
from std_msgs.msg import Bool
from mdp import  *
from QlearningEpislon import *
from QlearningWithUncertainty import *
from QLearningLValue import *



class robot:

    def __init__(self):
        rospy.init_node("robot")
        # self.move_list = read_config()["move_list"]


        self.move_list = read_config()["move_list"]
        self.mapSize = read_config()["map_size"]
        self.start = read_config()["start"]
        self.goal = read_config()["goal"]
        self.walls = read_config()["walls"]
        self.pits = read_config()["pits"]
        self.cost = read_config()["reward_for_each_step"]


        rospy.sleep(1)
        self.pathPub = rospy.Publisher("/results/path_list",AStarPath,queue_size=10)

        self.completePub = rospy.Publisher("/map_node/sim_complete",Bool,queue_size=10)
        self.mdpPub = rospy.Publisher("/results/policy_list",PolicyList,queue_size=10)

        rospy.sleep(3)
        pathList = astar(self.move_list,self.mapSize,self.start,self.goal,self.walls,self.pits,self.cost)

        print pathList
        for item in pathList:
            print item
            self.pathPub.publish(item)

        rospy.sleep(1)




        print "should publish"

        self.mdp = mdp()
        self.mdp.looping()
        self.QlearningEpsilon = QLearningEpislon()
        self.QlearningLValue = QLearningLValue()
        self.QlearningWithUncertainty = QLearningWithUncertainty()
        self.QlearningEpsilon.learning()
        self.QlearningLValue.learning()
        self.QlearningWithUncertainty.learning()



        policy = self.mdp.convertToList()

        self.mdpPub.publish(policy)
        rospy.sleep(1)

        policy = self.QlearningEpsilon.convertToList()
        self.mdpPub.publish(policy)
        rospy.sleep(1)


        policy =self.QlearningLValue.convertToList()
        self.mdpPub.publish(policy)
        rospy.sleep(1)

        policy =self.QlearningWithUncertainty.convertToList()
        self.mdpPub.publish(policy)
        rospy.sleep(1)


        self.completePub.publish(True)
        rospy.sleep(1)
        rospy.signal_shutdown("finish")










if __name__ == "__main__":
    rb = robot()