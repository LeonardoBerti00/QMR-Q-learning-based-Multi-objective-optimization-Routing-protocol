"""
You can write here the data elaboration function/s

You should read all the JSON files containing simulations results and compute
average and std of all the metrics of interest.

You can find the JSON file from the simulations into the data.evaluation_tests folder.
Each JSON file follows the naming convention: simulation-current date-simulation id__seed_drones number_routing algorithm

In this way you can parse the name and properly aggregate the data.

To aggregate data you can use also external libraries such as Pandas!

IMPORTANT: Both averages and stds must be computed over different seeds for the same metric!
"""


def compute_data_avg_std(path: str):
    """
    Computes averages and stds from JSON files
    @param path: results folder path
    @return: one or more data structure containing data
    """

    # TODO: Implement your code HERE

    pass


if __name__ == "__main__":
    """
    You can run this file to test your script
    """

    path = "data/evaluation_tests"

    compute_data_avg_std(path=path)