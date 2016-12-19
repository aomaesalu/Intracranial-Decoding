#!/usr/bin/env python2.7
# -*- coding: utf8 -*-i

from argparse import ArgumentParser
from lib.grid_search import grid_search
from lib.io import read_partitioned_data, write_data


def run(input_path, output_path, number_of_partitions, number_of_iterations,
        number_of_trials):

    # Read partitioned input data
    data = read_partitioned_data(input_path, number_of_iterations,
                                 number_of_partitions)

    # Define classification models and their corresponding parameters
    models = {
        'svm': {
            'C': (int, (5, 15)),
            'decision_function_shape': (tuple, ('ovo', 'ovr', None))
        },
        'random_forest': {
            'max_features': (int, (5, 15)),
            'class_weight': (tuple, ('balanced', 'balanced_subsample'))
        }
    }

    # Initialise the grid search result list
    results = []

    # Iterate trough each classification model defined
    for algorithm, parameter_model in models.items():

        # Perform grid search and append the results to the complete result list
        results += grid_search(data, algorithm, parameter_model,
                               number_of_trials)

    # Output the grid search results into the specified file
    write_data(output_path, results)


if __name__ == '__main__':
    # Parse command line arguments
    PARSER = ArgumentParser()
    PARSER.add_argument('input_path', help='the pickled input data file path')
    PARSER.add_argument('output_path', help='the pickled results data output ' +
                        'data file path')
    PARSER.add_argument('partitions', help='the amount of equal sized data ' +
                        'sets created upon partitioning the data', type=int)
    PARSER.add_argument('iterations', help='the amount of times to perform ' +
                        'k-fold cross-validation', type = int)
    PARSER.add_argument('trials', help='the amount of trials with different ' +
                        'randomly generated parameters for each model',
                        type=int)

    ARGUMENTS = PARSER.parse_args()

    # Run the data classification script
    run(ARGUMENTS.input_path, ARGUMENTS.output_path, ARGUMENTS.partitions,
        ARGUMENTS.iterations, ARGUMENTS.trials)
