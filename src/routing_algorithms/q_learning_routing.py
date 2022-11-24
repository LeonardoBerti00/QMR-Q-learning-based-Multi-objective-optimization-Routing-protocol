import random

from src.routing_algorithms.BASE_routing import BASE_routing
from src.utilities import utilities as util
import numpy as np

class QLearningRouting(BASE_routing):


    def __init__(self, drone, simulator):
        BASE_routing.__init__(self, drone, simulator)
        self.taken_actions = {}  # id event : (old_state, old_action)
        self.num_cells = int((self.simulator.env_height / self.simulator.prob_size_cell) * (self.simulator.env_width / self.simulator.prob_size_cell))
        self.Q = np.zeros((self.num_cells, int(self.simulator.n_drones)))
        self.a = 0.1
        self.l = 0.1

    def feedback(self, drone, id_event, delay, outcome):
        """
        Feedback returned when the packet arrives at the depot or
        Expire. This function have to be implemented in RL-based protocols ONLY
        @param drone: The drone that holds the packet
        @param id_event: The Event id
        @param delay: packet delay
        @param outcome: -1 or 1 (read below)
        """
        # Packets that we delivered and still need a feedback
        # print(self.taken_actions)

        #if(outcome == 1):
        if id_event in self.taken_actions:
            state, action = self.taken_actions[id_event]
            #state = int(state)
            #action = int(action)
            maxx = -1111111111
            for i in range(self.Q.shape[0]):
                for j in range(self.Q.shape[1]):
                    if (self.Q[i, j] > maxx):
                        max_action = j
                        max_state = i
                        maxx = self.Q[i, j]

            self.Q[state, action] = self.Q[state, action] + self.a * (outcome + self.l * self.Q[max_state, max_action] - self.Q[state, action])

        # Be aware, due to network errors we can give the same event to multiple drones and receive multiple
        # feedback for the same packet!!
        if id_event in self.taken_actions:
            state, action = self.taken_actions[id_event]
            del self.taken_actions[id_event]

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
        #print(len(opt_neighbors))
        #print(self.drone.identifier)
        maxx = -1000000
        r = random.randint(1, 100)
        if (r > 20):
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

        self.taken_actions[packet.event_ref.identifier] = (state, int(chosen.identifier))

        return chosen