from src.routing_algorithms.BASE_routing import BASE_routing
from src.utilities import utilities as util


class QLearningRouting(BASE_routing):

    def __init__(self, drone, simulator):
        BASE_routing.__init__(self, drone, simulator)
        self.taken_actions = {}  # id event : (old_state, old_action)

    def feedback(self, drone, id_event, delay, outcome):
        """
        Feedback returned when the packet arrives at the depot or
        Expire. This function have to be implemented in RL-based protocols ONLY
        @param drone: The drone that holds the packet
        @param id_event: The Event id
        @param delay: packet delay
        @param outcome: -1 or 1 (read below)
        @return:
        """
        # Packets that we delivered and still need a feedback
        print(self.taken_actions)

        # outcome can be:
        #
        # -1 if the packet/event expired;
        # 1 if the packets has been delivered to the depot
        print(drone, id_event, delay, outcome)

        # remove the entry, the action has received the feedback
        # Be aware, due to network errors we can give the same event to multiple drones and receive multiple
        # feedback for the same packet!!
        if id_event in self.taken_actions:
            state, action = self.taken_actions[id_event]
            del self.taken_actions[id_event]
            # reward or update using the old state and the selected action at that time
            # do something or train the model (?)

    def relay_selection(self, opt_neighbors: list, packet):
        """
        This function returns the best relay to send packets.

        @param packet:
        @param opt_neighbors: a list of tuple (hello_packet, source_drone)
        @return: The best drone to use as relay
        """
        # TODO: Implement your code HERE

        # Only if you need!
        # cell_index = util.TraversedCells.coord_to_cell(size_cell=self.simulator.prob_size_cell,
        #                                                width_area=self.simulator.env_width,
        #                                                x_pos=self.drone.coords[0],  # e.g. 1500
        #                                                y_pos=self.drone.coords[1])[0]  # e.g. 500
        # print(cell_index)
        state, action = None, None

        # Store your current action --- you can add some stuff if needed to take a reward later
        self.taken_actions[packet.event_ref.identifier] = (state, action)

        return None  # here you should return a drone object!
