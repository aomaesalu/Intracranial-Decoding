#!/usr/bin/env python2.7
# -*- coding: utf8 -*-i

from argparse import ArgumentParser
from lib.classification import classify
from sklearn import svm

# TODO: Tune model


def run(data_path, cv_amount, cv_iterations):

    # Define classification model
    model = svm.SVC()

    # Classify, predict and calculate the confusion matrix and scores
    confusion_matrix, scores = classify(data_path, cv_amount, cv_iterations,
                                        model)
    # Output model results
    print(confusion_matrix)
    print(scores)


if __name__ == '__main__':

    # Parse command line arguments
    PARSER = ArgumentParser()
    PARSER.add_argument('data_path', help='the pickled data file path')
    PARSER.add_argument('cv_amount', help='the amount of equal sized data ' +
                        'sets created upon partitioning the data', type=int)
    PARSER.add_argument('cv_iterations', help='the amount of times to ' +
                        'perform k-fold cross-validation', type=int)
    ARGUMENTS = PARSER.parse_args()

    # Run the data classification script
    run(ARGUMENTS.data_path, ARGUMENTS.cv_amount, ARGUMENTS.cv_iterations)
