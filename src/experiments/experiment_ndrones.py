from src.utilities.experiments_config import *
from src.experiments.parser.parser import command_line_parser
from src.utilities import config
from src.simulation.simulator import Simulator
import os


def sim_setup(n_drones, seed, algorithm):
    """
    Build an instance of Simulator using the parameters from src.utilities.experiments_config.py
    @param n_drones: the number of drones during the simulation
    @param seed: the simulation seed
    @param algorithm: the algorithm used to route the packets
    @return: an instance of Simulator
    """

    return Simulator(
        len_simulation=len_simulation,
        time_step_duration=time_step_duration,
        seed=seed,
        n_drones=n_drones,
        env_width=env_width,
        env_height=env_height,

        drone_com_range=drone_com_range,
        drone_sen_range=drone_sen_range,
        drone_speed=drone_speed,
        drone_max_buffer_size=drone_max_buffer_size,
        drone_max_energy=drone_max_energy,
        drone_retransmission_delta=drone_retransmission_delta,
        drone_communication_success=drone_communication_success,
        event_generation_delay=event_generation_delay,

        depot_com_range=depot_com_range,
        depot_coordinates=depot_coordinates,

        event_duration=event_duration,
        event_generation_prob=event_generation_prob,
        packets_max_ttl=packets_max_ttl,
        routing_algorithm=config.RoutingAlgorithm[algorithm],
        communication_error_type=config.ChannelError.GAUSSIAN,
        show_plot=show_plot,

        # ML parameters
        simulation_name="",

    )


def launch_experiments(n_drones, in_seed, out_seed, algorithm):
    """
    The function launches simulations for a given algorithm and drones number
    with seeds ranging from in_seed up to out_seed
    @param n_drones: integer that describes the number of drones
    @param in_seed: integer that describe the initial seed
    @param out_seed: integer that describe the final seed
    @param algorithm: the routing algorithm
    @return:
    """

    for seed in range(in_seed, out_seed):

        print(f"Running {algorithm} with {n_drones} drones seed {seed}")

        simulation = sim_setup(n_drones, seed, algorithm)

        simulation.run()

        simulation.close()


if __name__ == "__main__":

    args = command_line_parser.parse_args()

    number_of_drones = args.number_of_drones
    initial_seed = args.initial_seed
    end_seed = args.end_seed
    algorithm_routing = args.algorithm_routing
    path_filename = config.EXPERIMENTS_DIR

    # build directories for results and models
    os.system("mkdir " + path_filename)

    launch_experiments(number_of_drones, initial_seed, end_seed, algorithm_routing)

    print("Simulations completed!")
