#!/usr/bin/env python2.7
# -*- coding: utf8 -*-i

from argparse import ArgumentParser
from lib.io import read_data
from lib.string import format_path
from lib.cross_validation import construct_data_sets
from lib.score import ConfusionMatrix, Score
from sklearn import svm


def run(data_path, cv_amount, cv_iterations):

    # Initialise the true value and prediction lists
    true_values = []
    predictions = []

    # Repeat cross-validation a set amount of times
    for iteration in range(cv_iterations):

        # Read input data
        data = []
        for partition in range(cv_amount):
            data.append(read_data(format_path(format_path(data_path,
                                                          iteration + 1),
                                              partition + 1)))

        # Iterate through all of the data sets, using each of them for test data
        # exactly once, and using all others as training data sets at the same
        for test_index in range(cv_amount):

            # Construct training and test data sets
            train_data, test_data = construct_data_sets(data, cv_amount,
                                                        test_index)

            # Classification
            model = svm.SVC()
            model.fit(train_data['neural_responses'],
                      train_data['image_category'])

            # Prediction
            prediction = model.predict(test_data['neural_responses'])

            # Append the true values and predictions to the corresponding
            # general lists for later scoring
            true_values += test_data['image_category']
            predictions += list(prediction)

    # Scoring
    confusion_matrix = ConfusionMatrix(true_values, predictions)
    score = Score(true_values, predictions)
    print(confusion_matrix)
    print(score)


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
