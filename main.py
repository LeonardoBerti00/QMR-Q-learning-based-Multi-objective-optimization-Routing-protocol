import numpy as np
import multiprocessing
from src.simulation.simulator import Simulator
from src.utilities.policies import *


def main():
    """ the place where to run simulations and experiments. """

    drones = range(5,35,5)
    alphas = [0.1, 0.2, 0.01, 0.05]
    gammas = [0.1, 0.2, 0.01, 0.5]
    divs = [1000]
    epsilons = [15, 20, 25]
    optimistic_values = [2, 5]
    c_values = [100, 1000]
    negRewards = [-2, -5]
    grid_search(drones, alphas, gammas, divs, epsilons, Epsilon(), negRewards)
    grid_search2(drones, alphas, gammas, divs, epsilons, Epsilon(), negRewards)
    # sim = Simulator(5, 0.2, 0.2, 1000, UCB(1000))
    # sim.run()
    # sim.close()

    # np.save("results", np.array(results))
    # my_results = np.load("results.npy")
    #
    # for (seed, result) in my_results:
    #     print("seed ", seed, " result ", result)


def grid_search(drones, alphas, gammas, divs, policy_values, policy, negRewards):
    # FIRST PART GRID SEARCH: we search between the possible tuple of hyperparameters and
    # we save the metric (sum of the ratio) simulating for every tuple for all the possible num of drones
    results = []
    for neg in negRewards:
        for value in policy_values:
            policy.value = value
            for alpha in alphas:
                for gamma in gammas:
                    for div in divs:
                        sum = 0
                        for drone in drones:
                            for seed in range(1, 3):
                                sim = Simulator(drone, alpha, gamma, div, neg, 1, policy, seed)
                                sim.run()
                                # we compute the sum of the ratio to choose the best tuple of hyperparameters considering all the possible num of drones
                                sum += len(sim.metrics.drones_packets_to_depot) / sim.metrics.all_data_packets_in_simulation
                                sim.close()
                        results.append((alpha, gamma, 1000, value, neg, sum))


    results = np.array(results)
    results = results[np.argsort(results[:, 5])]
    results = np.flip(results, 0)
    np.save("Risultati.npy", np.array(results))

    (alpha, gamma, div, value, neg, sum) = results[0]
    policy.add(value)

    seed_results = []

    for drone in drones:
        values = []
        for seed in range(1, 20):
            sim = Simulator(drone, alpha, gamma, div, 2, neg, policy, seed)
            sim.run()
            values.append(len(sim.metrics.drones_packets_to_depot) / sim.metrics.all_data_packets_in_simulation)
            sim.close()
        seed_results.append((drone, sum(values) / len(values)))

    np.save("Seed_Results.npy", np.array(seed_results))

    print(seed_results)

def grid_search2(drones, alphas, gammas, divs, policy_values, policy, negRewards):
    # FIRST PART GRID SEARCH: we search between the possible tuple of hyperparameters and
    # we save the metric (sum of the ratio) simulating for every tuple for all the possible num of drones
    results = []
    for neg in negRewards:
        for value in policy_values:
            policy.value = value
            for alpha in alphas:
                for gamma in gammas:
                    sum = 0
                    for drone in drones:
                        for seed in range(1, 3):
                            sim = Simulator(drone, alpha, gamma, 1000, neg, 2, policy, seed)
                            sim.run()
                            # we compute the sum of the ratio to choose the best tuple of hyperparameters considering all the possible num of drones
                            sum += len(sim.metrics.drones_packets_to_depot) / sim.metrics.all_data_packets_in_simulation
                            sim.close()
                    results.append((alpha, gamma, 1000, value, neg, sum))


    results = np.array(results)
    results = results[np.argsort(results[:, 5])]
    results = np.flip(results, 0)
    np.save("Risultati2.npy", np.array(results))

    (alpha, gamma, div, value, neg, sum) = results[0]
    policy.add(value)

    seed_results = []

    for drone in drones:
        values = []
        for seed in range(1, 20):
            sim = Simulator(drone, alpha, gamma, div, 2, neg, policy, seed)
            sim.run()
            values.append(len(sim.metrics.drones_packets_to_depot) / sim.metrics.all_data_packets_in_simulation)
            sim.close()
        seed_results.append((drone, sum(values) / len(values)))

    np.save("Seed_Results2.npy", np.array(seed_results))

    print(seed_results)

if __name__ == "__main__":
    main()
