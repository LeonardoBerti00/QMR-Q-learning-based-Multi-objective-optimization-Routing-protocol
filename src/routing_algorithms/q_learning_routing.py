import random
from src.routing_algorithms.BASE_routing import BASE_routing
from src.utilities import utilities as util
from src.utilities.policies import *
import numpy as np
import math

class QMAR(BASE_routing):

    def __init__(self, drone, simulator):
        BASE_routing.__init__(self, drone, simulator)
        self.maxReward = 5
        self.minReward = -5
        self.w = 0.7


    def feedback(self, outcome, id_j, Q_value_best_action):
        """
        Feedback returned when the packet arrives at the depot or
        """
        alpha = self.drone.neighbor_table[id_j, 10]
        gamma = self.drone.neighbor_table[id_j, 7]
        Q_value_i_j = self.drone.neighbor_table[id_j, 9]

        #gives the max reward when the packet arrives to the depot
        if (outcome == 1):
            self.drone.neighbor_table[id_j, 9] = Q_value_i_j + alpha * (self.maxReward)

        #the packet is arrived to the node j, but it isn't the depot
        elif (outcome == 0):
            delay = self.drone.neighbor_table[id_j, 8] + self.drone.neighbor_table[id_j, 11]
            reward = self.computeReward(outcome, delay)
            #Update Q table
            self.drone.neighbor_table[id_j, 9] = Q_value_i_j + alpha * (reward + gamma * Q_value_best_action - Q_value_i_j)

        else:
            self.drone.neighbor_table[id_j, 9] = Q_value_i_j + alpha * (self.minReward + gamma * Q_value_best_action - Q_value_i_j)


    def computeReward(self, outcome, delay):
        return self.w * math.exp(delay) + (1 - self.w) * (self.drone.residual_energy/self.drone.initial_energy)


    def relay_selection(self, opt_neighbors, data):

        packet = data[0]
        candidates = []
        candidates2 = []
        for node_j in self.simulator.drones:
            if (node_j in opt_neighbors):
                j = node_j.identifier
                #first of all we need to compute the requested velocity not to expire the packet
                deadline = 2001 - (self.simulator.cur_step - packet.time_step_creation)
                if (deadline == 0):
                    print()
                distance_i = util.euclidean_distance(self.drone.coords, self.simulator.depot_coordinates)      #distance from node i to depot
                req_v = distance_i / deadline

                #we compute the actual velocity from node i to node j
                actual_v, distance_i_j = self.computeActualVel(j, node_j, distance_i)

                if (actual_v >= req_v):
                    #node_j is a possible candidate!!! Now we need to compute the weight k
                    LQ = self.drone.neighbor_table[j, 12]

                    #Computing relationship coefficient
                    R = self.drone.communication_range

                    if (distance_i_j > R):
                        M = 0
                    else:
                        M = 1 - (distance_i_j/R)

                    k = M * LQ
                    candidates.append((node_j, k))

                elif(actual_v > 0):
                    '''
                    we append in the secondary array of candidates the neighbors
                    whose actual velocities are greater than 0, so the neighbor associated
                    with the maximum actual velocity will be selected as the next hop
                    '''
                    candidates2.append((node_j, actual_v))

        if len(candidates) == 0:
            maxx = -3414212
            if (len(candidates2) > 0):
                for i in range(len(candidates2)):
                    if (candidates2[i][1] > maxx):
                        maxx = candidates2[i][1]
                        chosen = candidates2[i][0]
            else:
                #we've encountered the routing hole problem so we give to the previous hop node 𝑖 the minimum reward
                return "RHP"


        else:
            #Choosing the next hop with weighted Q_value max
            maxx = -100000
            chosen = None
            for i in range(len(candidates)):
                candidate = candidates[i][0]
                k = candidates[i][1]
                Q_val = self.drone.neighbor_table[candidate.identifier, 9]
                if (Q_val * k > maxx):
                    chosen = candidate
                    maxx = Q_val * k

        #Select the id of the chosen drone
        if (chosen == None):
            id = self.drone.identifier
        else:
            id = chosen.identifier

        return chosen

    def computeActualVel(self, j, node_j, distance_i):

        #we try to estimate the position of node j at time t3, so when the packet should arrive
        x2 = self.drone.neighbor_table[j, 4]
        y2 = self.drone.neighbor_table[j, 5]
        x1 = self.drone.neighbor_table[j, 0]
        y1 = self.drone.neighbor_table[j, 1]


        if (x2 - x1 != 0):
            angle_j = math.atan((y2 - y1) / (x2 - x1))
        else:
            #it's possible that the hello packet from node_j isn't arrived yet
            angle_j = math.atan(0)

        delay = self.drone.neighbor_table[j, 8] + self.drone.neighbor_table[j, 11]
        if (delay == 0):
            delay = 0.01
        t1 = self.drone.neighbor_table[j, 6]    #timestamp of the last update of the node j in the neighbor table of node i (=self.drone)
        t3 = self.simulator.cur_step + delay
        x = x1 + node_j.speed * math.cos(angle_j) * (t3 - t1)
        y = node_j.coords[1] + node_j.speed * math.sin(angle_j) * (t3 - t1)
        distance_j = util.euclidean_distance((x, y), self.simulator.depot_coordinates)
        distance_i_j = util.euclidean_distance(self.drone.coords, (x, y))
        return (distance_i - distance_j) / delay, distance_i_j
