#!/usr/bin/env python2.7
# -*- coding: utf8 -*-i

from argparse import ArgumentParser
from lib.io import read_data
from lib.ensemble import construct_ensemble, ensemble_vote


def run(input_path, best_proportion, used_proportion):

    # Read the grid search results as input data
    data = read_data(input_path)

    # Construct the ensemble based on the results of the grid search and the
    # proportion parameters passed to this script
    ensemble = construct_ensemble(data, best_proportion, used_proportion)

    # Retrieve the classification results from the ensemble based on a
    # popularity vote
    predicted_values = ensemble_vote(ensemble)

    # Score the classification results of the ensemble against the true values
    pass # TODO

    # Output the results
    pass # TODO


if __name__ == '__main__':

    # Parse command line arguments
    PARSER = ArgumentParser()
    PARSER.add_argument('input_path', help='the pickled data input file ' \
                        'containing all of the results of the grid search')
    PARSER.add_argument('best_proportion', help='the proportion of best ' \
                        'results to be taken into account while constructing ' \
                        'the ensemble', type=float)
    PARSER.add_argument('used_proportion', help='the proportion of results ' \
                        'most disagreeing with each other to be kept in the ' \
                        'ensemble')
    ARGUMENTS = PARSER.parse_args()

    # Run the ensemble construction and scoring script
    run(ARGUMENTS.input_path, ARGUMENTS.best_proportion,
        ARGUMENTS.used_proportion)
