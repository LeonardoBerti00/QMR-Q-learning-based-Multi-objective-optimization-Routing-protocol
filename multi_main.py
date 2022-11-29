import numpy as np
import multiprocessing
from itertools import chain
from src.simulation.simulator import Simulator
from src.utilities.policies import *

alphas = [0.1, 0.2, 0.01, 0.05]
gammas = [0.1, 0.2, 0.01]
divs = [1000]
epsilons = [15, 20, 25]
optimistic_values = [5, 10, 2, 0.1, 0.01, 0.5, 0.8]
c_values = [100, 1000]
negRewards = [-2, -5]

def multi_simulation(drone):
    my_result = []
    for negreward in negRewards:
        for value in optimistic_values:
            for alpha in alphas:
                for gamma in gammas:
                    for div in divs:
                        sum = 0
                        sim = Simulator(drone, alpha, gamma, div, negreward, 1, Optimistic(value))
                        sim.run()
                        # we compute the sum of the ratio to choose the best tuple of hyperparameters considering all the possible num of drones
                        sum += len(sim.metrics.drones_packets_to_depot) / sim.metrics.all_data_packets_in_simulation
                        sim.close()
                        my_result.append((alpha, gamma, div, value, sum, drone))

    return my_result


if __name__ == "__main__":
    pool = multiprocessing.Pool(2)
    results = pool.map(multi_simulation, range(5, 35, 5))
    results = list(map(tuple, chain.from_iterable(results)))
    np.save("prova.npy", np.array(results))