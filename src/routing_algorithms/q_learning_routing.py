import random

from src.routing_algorithms.BASE_routing import BASE_routing
from src.utilities import utilities as util
import numpy as np




class QLearningRouting(BASE_routing):


    def __init__(self, drone, simulator):
        BASE_routing.__init__(self, drone, simulator)
        self.taken_actions = {}  # id event : (old_state, old_action)
        self.num_cells = int((self.simulator.env_height / self.simulator.prob_size_cell) * (self.simulator.env_width / self.simulator.prob_size_cell))
        self.Q = np.ones((self.num_cells, int(self.simulator.n_drones)))
        self.a = 0.2
        self.l = 0.1
        self.eps = 20
        self.div = 50

    def feedback(self, drone, id_event, delay, outcome):
        """
        Feedback returned when the packet arrives at the depot or
        Expire. This function have to be implemented in RL-based protocols ONLY
        @param drone: The drone that holds the packet
        @param id_event: The Event id
        @param delay: packet delay
        @param outcome: -1 or 1 (read below)
        """



        if id_event in self.taken_actions:
            array = self.taken_actions[id_event]
            maxx = -1111111111
            for i in range(self.Q.shape[0]):          #select the best Q[s, a]
                for j in range(self.Q.shape[1]):
                    if (self.Q[i, j] > maxx):
                        max_action = j
                        max_state = i
                        maxx = self.Q[i, j]

            for i in range(len(array)):
                state, action = array[i]
                reward = self.computeReward(id_event, outcome, delay, state, action)
                self.Q[state, action] = self.Q[state, action] + self.a * (reward + self.l * self.Q[max_state, max_action] - self.Q[state, action])

            del self.taken_actions[id_event]

        # Be aware, due to network errors we can give the same event to multiple drones and receive multiple
        # feedback for the same packet!!

    def computeReward(self, id_event, outcome, delay, state, action):
        reward = outcome
        return reward * (delay/self.div)


    def relay_selection(self, opt_neighbors: list, packet):
        """
        This function returns the best relay to send packets.
        @param packet:
        @param opt_neighbors: a list of tuple (hello_packet, source_drone)
        @return: The best drone to use as relay
        """

        cell_index = util.TraversedCells.coord_to_cell(size_cell=self.simulator.prob_size_cell,
                                                        width_area=self.simulator.env_width,
                                                        x_pos=self.drone.coords[0],  # e.g. 1500
                                                        y_pos=self.drone.coords[1])[0]  # e.g. 500

        state = int(cell_index)
        action = None


        chosen = self.egreedy(opt_neighbors, state)
        if (chosen == None):
            id = self.drone.identifier
        else:
            id = chosen.identifier

        if (packet.event_ref.identifier in self.taken_actions):            #if I've done the same action with the same packet
            self.taken_actions[packet.event_ref.identifier].append((state, int(id)))
        else:
            self.taken_actions[packet.event_ref.identifier] = [(state, int(id))]
        #print()
        return chosen

    def egreedy(self, opt_neighbors, state):
        r = random.randint(1, 100)
        maxx = -1000000
        if (r > self.eps):
            for i in range(len(opt_neighbors)):
                id = int(opt_neighbors[i][1].identifier)
                if (self.Q[state, id] > maxx):
                    chosen = opt_neighbors[i][1]
                    maxx = self.Q[state, id]

            if (self.Q[state, int(self.drone.identifier)] > maxx):
                return None
        else:
            r = random.randint(0, len(opt_neighbors))
            if (r == len(opt_neighbors)):
                return None
            else:
                chosen = opt_neighbors[r][1]
        return chosen
