from src.routing_algorithms.BASE_routing import BASE_routing


class QLearningRouting(BASE_routing):

    def __init__(self, drone, simulator):

        BASE_routing.__init__(self, drone, simulator)

    def relay_selection(self, opt_neighbors: list):
        """
        This function returns the best relay to send packets.

        @param opt_neighbors: a list of tuples (hello_packet, drone)
        @return: The best drone to use as relay or None if no relay is selected
        """
        # TODO: Implement your code HERE

        return None
