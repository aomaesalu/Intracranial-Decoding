#!/usr/bin/env python2.7
# -*- coding: utf8 -*-i

from argparse import ArgumentParser
from lib.classification import classify
from sklearn.ensemble import RandomForestClassifier
from scipy.stats import randint as sp_randint

# TODO: Tune model


def run(data_path, partitions, iterations):
    # Define classification model
    # Possible additional parameters:
    #   max_features=... (10?)
    #   max_leaf_nodes=... (15?)
    #   max_depth=... (5?)
    #   class_weight=...
    model = RandomForestClassifier(n_estimators=100)

    # Parameters to be randomized
    search_params = {"max_features": sp_randint(5, 15),
                  "class_weight": ["balanced", "balanced_subsample"]}

    # Iterations for randomizing
    search_iterations = 3

    # Classify, predict and calculate the confusion matrix and scores
    confusion_matrix, scores = classify(data_path, partitions, iterations,
                                        model, search_params, search_iterations)

    # Output model results
    print(confusion_matrix)
    print(scores)


if __name__ == '__main__':
    # Parse command line arguments
    PARSER = ArgumentParser()
    PARSER.add_argument('data_path', help='the pickled data file path')
    PARSER.add_argument('partitions', help='the amount of equal sized data ' +
                                           'sets created upon partitioning the data', type=int)
    PARSER.add_argument('iterations', help='the amount of times to perform ' +
                                           'k-fold cross-validation', type=int)
    ARGUMENTS = PARSER.parse_args()

    # Run the data classification script
    run(ARGUMENTS.data_path, ARGUMENTS.partitions, ARGUMENTS.iterations)
