import numpy as np
from src.simulation.simulator import Simulator
from src.utilities.policies import *

def main():
    """ the place where to run simulations and experiments. """


'''
    drones = range(5,35,5)
    alphas = [0.1, 0.2, 0.05, 0.01, 0.15]
    gammas = [0.1, 0.2, 0.05, 0.01, 0.5]
    divs = [1000, 1200]
    epsilons = [15, 20, 25, 30]
    values = [0.1, 0.2, 0.5, 1, 2, 3]
    egreedy_grid_search(drones, alphas, gammas, divs, epsilons)


    drones = [5, 10]
    alphas = [0.1]
    gammas = [0.1]
    divs = [1000]
    epsilons = [20]
'''


def grid_search(drones, alphas, gammas, divs, policy):
    # FIRST PART GRID SEARCH: we search between the possible tuple of hyperparameters and
    # we save the metric (sum of the ratio) simulating for every tuple for all the possible num of drones
    results = []
    for alpha in alphas:
        for gamma in gammas:
            for div in divs:
                for drone in drones:
                    sim = Simulator(drone, alpha, gamma, div, policy)
                    sim.run()
                    # we compute the sum of the ratio to choose the best tuple of hyperparameters considering all the possible num of drones
                    sum += len(sim.metrics.drones_packets_to_depot) / sim.metrics.all_data_packets_in_simulation
                    sim.close()
                results.append((alpha, gamma, div, policy.value(), sum))

    results = np.array(results)
    results = results[np.argsort(results[:, 4])]
    data = np.flip(results, 0)
    np.save("Risultati.npy", np.array(results))

    # SECOND PART GRID SEARCH: after testing the generalization of the best tuple of hyperparameters, we extract the best 10 tuples,
    # so we can test them with the script for 30 seed for each num of drones, to assure the results stability.


def egreedy_grid_search(drones, alphas, gammas, divs, epsilons):
    for epsilon in epsilons:
        grid_search(drones, alphas, gammas, divs, Epsilon(epsilon))



def optimistic_grid_search(drones, alphas, gammas, divs, values):
    for value in values:
        grid_search(drones, alphas, gammas, divs, Optimistic(value))



if __name__ == "__main__":
    main()
