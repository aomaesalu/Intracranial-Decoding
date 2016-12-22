#!/usr/bin/env python2.7
# -*- coding: utf8 -*-i

from argparse import ArgumentParser
from lib.io import read_data, read_partitioned_data, write_data
from lib.classification import get_true_values, Result
from lib.ensemble import construct_ensemble, ensemble_vote


def run(data_path, grid_search_path, output_path, number_of_partitions,
        number_of_iterations, best_proportion, used_proportion):

    # Read partitioned input data
    data = read_partitioned_data(data_path, number_of_iterations,
                                 number_of_partitions)

    # Read true values from the partitioned data set
    true_values = get_true_values(data)

    # Read the grid search results as input data
    results = read_data(grid_search_path)

    # Construct the ensemble based on the results of the grid search and the
    # proportion parameters passed to this script
    ensemble = construct_ensemble(results, best_proportion, used_proportion)

    # Retrieve the classification results from the ensemble based on a
    # popularity vote
    predicted_values = ensemble_vote(ensemble)

    # Score the classification results of the ensemble against the true values
    result = Result()
    result.add_values(true_values, predicted_values)
    result.calculate()

    # Output the ensemble into the specified file
    write_data(output_path, ensemble)

    # Output the results of the ensemble on the screen
    print(result)


if __name__ == '__main__':

    # Parse command line arguments
    PARSER = ArgumentParser()
    PARSER.add_argument('data_path', help='the pickled input data file path')
    PARSER.add_argument('grid_search_path', help='the pickled data input ' +
                        'file containing all of the results of the grid search')
    PARSER.add_argument('output_path', help='the pickled ensemble results ' \
                        'data output data file path')
    PARSER.add_argument('partitions', help='the amount of equal sized data ' +
                        'sets created upon partitioning the data', type=int)
    PARSER.add_argument('iterations', help='the amount of times to perform ' +
                        'k-fold cross-validation', type=int)
    PARSER.add_argument('best_proportion', help='the proportion of best ' \
                        'results to be taken into account while constructing ' \
                        'the ensemble', type=float)
    PARSER.add_argument('used_proportion', help='the proportion of results ' \
                        'most disagreeing with each other to be kept in the ' \
                        'ensemble', type=float)
    ARGUMENTS = PARSER.parse_args()

    # Run the ensemble construction and scoring script
    run(ARGUMENTS.data_path, ARGUMENTS.grid_search_path, ARGUMENTS.output_path,
        ARGUMENTS.partitions, ARGUMENTS.iterations, ARGUMENTS.best_proportion,
        ARGUMENTS.used_proportion)
