from argparse import ArgumentParser
from src.utilities import config

command_line_parser = ArgumentParser()

routing_choices = config.RoutingAlgorithm.keylist()

command_line_parser.add_argument("-nd", dest='number_of_drones', action="store", type=int,
                                 help="the number of drones to use in the simulataion")
command_line_parser.add_argument("-i_s", dest='initial_seed', action="store", type=int,
                                 help="the initial seed (included) to use in the simualtions")
command_line_parser.add_argument("-e_s", dest='end_seed', action="store", type=int,
                                 help="the end seed (excluded) to use in the simualtions"
                         + "-notice that the simulations will run for seed in (i_s, e_s)")
command_line_parser.add_argument("-alg", dest='algorithm_routing', action="store", type=str,
                                 choices=routing_choices, help="the routing algorithm to use")