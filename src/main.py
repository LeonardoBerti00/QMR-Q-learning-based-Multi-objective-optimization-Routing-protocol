
from src.simulation.simulator import Simulator


def main():
    """ the place where to run simulations and experiments. """

    for i in range(1, 7):
        sim = Simulator(i*5, 15000)   # empty constructor means that all the parameters of the simulation are taken from src.utilities.config.py
        sim.run()            # run the simulation
        sim.close()


if __name__ == "__main__":
    main()
