import numpy as np
import multiprocessing
from itertools import chain
from src.simulation.simulator import Simulator
from src.utilities.policies import *

alphas = [0.1, 0.2, 0.01]
gammas = [0.1, 0.01]
divs = [1000]
epsilons = range(5,80,5)
optimistic_values = [5, 10, 1]
c_values = [0.4, 0.9]
negRewards = [-2]
used_values = []

def multi_simulation(value):
    my_result = []
    for neg in negRewards:
        for alpha in alphas:
            for gamma in gammas:
                for div in divs:
                    somma = 0
                    for drone in range(5, 35, 5):
                        for seed in range(10):
                            sim = Simulator(drone, alpha, gamma, div, 1, neg, Optimistic(), seed)
                            sim.run()
                            # we compute the sum of the ratio to choose the best tuple of hyperparameters considering all the possible num of drones
                            somma += len(sim.metrics.drones_packets_to_depot) / sim.metrics.all_data_packets_in_simulation
                            sim.close()
                    my_result.append((alpha, gamma, div, value, neg, somma))

if __name__ == "__main__":
    pool = multiprocessing.Pool(4)
    used_values = optimistic_values
    results = pool.map(multi_simulation, optimistic_values)
    results = list(map(tuple, chain.from_iterable(results)))

    np.save("optimistic.npy", np.array(results))

    results = np.array(results)
    results = results[np.argsort(results[:, 5])]
    results = np.flip(results, 0)
    np.save("../Risultati.npy", results)

    (alpha, gamma, div, value, neg, somma) = results[0]
    Optimistic(value)

    seed_results = []

    for drone in range(5,35,5):
        values = []
        times = []
        for seed in range(1, 31):
            sim = Simulator(drone, alpha, gamma, div, 1, neg, Optimistic(), seed)
            sim.run()
            first_metric = len(sim.metrics.drones_packets_to_depot) / sim.metrics.all_data_packets_in_simulation
            sim.close()
            second_metric = sim.metrics.packet_mean_delivery_time
            seed_results.append((drone, seed, first_metric, second_metric))

    np.save("Seed_Results.npy", np.array(seed_results))

    print(seed_results)