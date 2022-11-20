from src.routing_algorithms.BASE_routing import BASE_routing


class GeoRouting(BASE_routing):

    def __init__(self, drone, simulator):
        BASE_routing.__init__(self, drone, simulator)

    def relay_selection(self, opt_neighbors, packet):
        """
        This function returns a relay for packets according to geographic routing using C2S criteria.

        @param packet:
        @param opt_neighbors: a list of tuples (hello_packet, drone)
        @return: The best drone to use as relay or None if no relay is selected
        """

        # TODO: Implement your code HERE

        return None
