import numpy as np
from src.simulation.simulator import Simulator
from src.utilities.policies import *

def main():
    """ the place where to run simulations and experiments. """

    sim = Simulator(5, 0.5, 0.5, 1000, Optimistic(2))  # empty constructor means that all the parameters of the simulation are taken from src.utilities.config.py
    sim.run()  # run the simulation
    print(len(sim.metrics.drones_packets_to_depot) / sim.metrics.all_data_packets_in_simulation)
    sim.close()

    # data= np.load('src\Risultati.npy')
    #
    # data = data[np.argsort(data[:, 5])]
    # data = np.flip(data, 0)
    # #print(data[:20])
    # sett = set()
    # for i in range(data.shape[0]-900):
    #     drone, alpha, gamma, epsilon, div, metric = data[i]
    #     sett.add((alpha, gamma, epsilon, div))
    #
    # print(len(sett))
    #
    #
    # result = []
    # for tupla in sett:
    #     somma = 0
    #     for drone in range(5, 35, 5):
    #         alpha, gamma, epsilon, div = tupla
    #         sim = Simulator(drone, alpha, gamma, epsilon, div)
    #         sim.run()
    #         somma += len(sim.metrics.drones_packets_to_depot) / sim.metrics.all_data_packets_in_simulation
    #         sim.close()
    #     result.append((alpha, gamma, epsilon, div, somma))
    #     print(len(result))
    #
    # np.save("Risultati2.0", np.array(result))
    # result = np.array(result)
    # result = result[np.argsort(result[:, 4])]
    # result = np.flip(result, 0)
    # print(result[:20])
'''
    alphas = [0.1, 0.2, 0.05, 0.01, 0.15]
    gammas = [0.1, 0.2, 0.05, 0.01, 0.5]
    epsilons = [15, 20, 25, 30]
    initial_values = [1, 2, 3, 4]
    divs = [1000, 1200]
    results = []

    for drone in range(5, 30, 5):
        for alpha in alphas:
            for gamma in gammas:
                for epsilon in epsilons:
                    for div in divs:
                        sim = Simulator(drone, alpha, gamma, epsilon, div)
                        sim.run()
                        results.append((drone, alpha, gamma, epsilon, div, len(sim.metrics.drones_packets_to_depot) / sim.metrics.all_data_packets_in_simulation))
                        sim.close()

    np.save("Risultati", np.array(results))

'''

if __name__ == "__main__":
    main()
