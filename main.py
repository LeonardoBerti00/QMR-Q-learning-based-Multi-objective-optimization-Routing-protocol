import numpy as np
from src.simulation.simulator import Simulator
from src.utilities.policies import *

def main():
    """ the place where to run simulations and experiments. """

    #FIRST PART GRID SEARCH: we search between the possible tuple of hyperparameters and we save the metrics for every one, with only one simulation for every tuple, n_drones

    # drones = range(5,35,5)
    # alphas = [0.1, 0.2, 0.05, 0.01, 0.15]
    # gammas = [0.1, 0.2, 0.05, 0.01, 0.5]
    # divs = [1000, 1200]
    #
    # epsilons = [15, 20, 25, 30]
    # values = [0.1, 0.2, 0.5, 1, 2, 3]

    drones = [5, 10]
    alphas = [0.1]
    gammas = [0.1]
    divs = [1000]
    epsilons = [20]

    egreedy_grid_search(drones, alphas, gammas, divs, epsilons)


results = []


def grid_search(drones, alphas, gammas, divs, policy):
    for drone in drones:
        for alpha in alphas:
            for gamma in gammas:
                for div in divs:
                    sim = Simulator(drone, alpha, gamma, div, policy)
                    sim.run()
                    results.append((drone, alpha, gamma, div, policy.value(), len(sim.metrics.drones_packets_to_depot) / sim.metrics.all_data_packets_in_simulation))
                    sim.close()


def egreedy_grid_search(drones, alphas, gammas, divs, epsilons):
    for epsilon in epsilons:
        grid_search(drones, alphas, gammas, divs, Epsilon(epsilon))
    optimization(drones, Epsilon())


def optimistic_grid_search(drones, alphas, gammas, divs, values):
    for value in values:
        grid_search(drones, alphas, gammas, divs, Optimistic(value))
    optimization(drones, Optimistic())


def optimization(drones, type):
    np.save("src/Risultati.npy", np.array(results))

    # SECOND PART GRID SEARCH: we choose the fifty tuples of parameters with the best metric and we try them with all the possible number of drones, toassure the generalization
    data = np.load('src/Risultati.npy')
    data = data[np.argsort(data[:, 5])]
    data = np.flip(data, 0)

    sett = set()
    # for i in range(data.shape[0] - 950):
    for i in range(data.shape[0]):
        drone, alpha, gamma, div, value, result = data[i]
        sett.add((alpha, gamma, div, value))

    result = []
    for tupla in sett:
        somma = 0
        alpha, gamma, div, value = tupla
        for drone in drones:
            type.add(value)
            sim = Simulator(drone, alpha, gamma, div, type)
            sim.run()
            somma += len(sim.metrics.drones_packets_to_depot) / sim.metrics.all_data_packets_in_simulation
            sim.close()
        result.append((alpha, gamma, div, value, somma))
        # print(len(result))

    np.save("Risultati2.0", np.array(result))

    # THIRD PART GRID SEARCH: after testing the generalization of the best tuple of hyperparameters,
    # we extract the best 10 tuples, so we can test them with the script for 30 seed for each num of drones, to assure the results stability.

    result = np.array(result)
    result = result[np.argsort(result[:, 4])]
    result = np.flip(result, 0)
    print(result[:10])

    np.save("Risultati", np.array(results))


'''
    sim = Simulator(5, 0.1, 0.1, 20, 50)  # empty constructor means that all the parameters of the simulation are taken from src.utilities.config.py
    sim.run()  # run the simulation
    print(len(sim.metrics.drones_packets_to_depot) / sim.metrics.all_data_packets_in_simulation)
    sim.close()
'''

if __name__ == "__main__":
    main()
