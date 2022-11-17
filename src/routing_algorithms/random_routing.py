import src.utilities.utilities as util
from src.routing_algorithms.BASE_routing import BASE_routing


class RandomRouting(BASE_routing):

    def __init__(self, drone, simulator):
        BASE_routing.__init__(self, drone, simulator)

    def relay_selection(self, opt_neighbors):
        """
        Random relay selection
        @param opt_neighbors: the list of all the neighbors
        @return: a random relay
        """

        return self.simulator.rnd_routing.choice([v[1] for v in opt_neighbors])
