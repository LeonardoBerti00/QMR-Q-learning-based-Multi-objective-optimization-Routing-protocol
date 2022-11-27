import numpy as np
from src.simulation.simulator import Simulator


def main():
    """ the place where to run simulations and experiments. """

    alphas = [0.1, 0.2, 0.05, 0.01, 0.15]
    gammas = [0.1, 0.2, 0.05, 0.01, 0.5]
    epsilons = [15, 20, 25, 30]
    divs = [1000, 1200]
    results = []

    for drone in range(5, 30, 5):
        for alpha in alphas:
            for gamma in gammas:
                for epsilon in epsilons:
                    for div in divs:
                        sim = Simulator(drone, alpha, gamma, epsilon, div, Simulator.Policy.EPSILON)
                        sim.run()
                        results.append((drone, alpha, gamma, epsilon, div, len(sim.metrics.drones_packets_to_depot) / sim.metrics.all_data_packets_in_simulation))
                        sim.close()

    np.save("Risultati", np.array(results))


    sim = Simulator(5, 0.1, 0.1, 20, 50)  # empty constructor means that all the parameters of the simulation are taken from src.utilities.config.py
    sim.run()  # run the simulation
    print(len(sim.metrics.drones_packets_to_depot) / sim.metrics.all_data_packets_in_simulation)
    sim.close()

    # for i in range(6):

if __name__ == "__main__":
    main()
