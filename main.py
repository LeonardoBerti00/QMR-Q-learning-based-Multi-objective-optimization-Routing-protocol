import numpy as np
import multiprocessing
from src.simulation.simulator import Simulator
from src.utilities.policies import *


def main():
    """ the place where to run simulations and experiments. """

    drones = range(5,35,5)

    '''
    sim = Simulator(5, 1)
    sim.run()
    first_metric = len(sim.metrics.drones_packets_to_depot) / sim.metrics.all_data_packets_in_simulation
    print(first_metric)
    sim.close()
    '''
    #grid_search(drones, alphas, gammas, divs, epsilons, Epsilon(), negRewards)
    seed_results = []


    for drone in drones:
        values = []
        times = []
        for seed in range(1, 31):
            sim = Simulator(drone, seed)
            sim.run()
            first_metric = len(sim.metrics.drones_packets_to_depot) / sim.metrics.all_data_packets_in_simulation
            print(first_metric)
            sim.close()
            sim.metrics.other_metrics()
            second_metric = sim.metrics.packet_mean_delivery_time
            seed_results.append((drone, seed, first_metric, second_metric))
    np.save("Seed_Results.npy", np.array(seed_results))


if __name__ == "__main__":
    main()
