#!/usr/bin/env python2.7
# -*- coding: utf8 -*-i

from argparse import ArgumentParser
from lib.io import read_data
from lib.string import format_path
from lib.cross_validation import construct_data_sets
from lib.score import ConfusionMatrix, Score
from sklearn import svm


def run(data_path, cv_amount):

    # Read input data
    data = []
    for i in range(cv_amount):
        data.append(read_data(format_path(data_path, i + 1)))

    # Iterate through all of the data sets, using each of them for test data
    # exactly once, and using all others as training data sets at the same
    for test_index in range(cv_amount):

        # Construct training and test data sets
        train_data, test_data = construct_data_sets(data, cv_amount, test_index)

        print('Performing SVM classifier...')
        svcClassif = svm.SVC()
        print('Fitting training samples to create a training model...')

        # TODO not sure if this is the correct type of data that should be used
        # for fitting, but this should be the general sequence of the
        # classification

        # First parameter: array of size [n_samples, n_features], second
        # parameter: array of size [n_samples]
        svcClassif.fit(train_data['neural_responses'], train_data['image_category'])
        print('Performing classification on test samples...')
        prediction = svcClassif.predict(test_data['neural_responses'])
        print 'Resulting classifications: ', prediction
        print 'Actual classes: ', test_data['image_category']

        # Scoring
        confusion_matrix = ConfusionMatrix(test_data['image_category'], prediction)
        print(confusion_matrix)
        score = Score(test_data['image_category'], prediction)
        print(score)


if __name__ == '__main__':

    # Parse command line arguments
    PARSER = ArgumentParser()
    PARSER.add_argument('data_path', help='the pickled data file path')
    PARSER.add_argument('cv_amount', help='the amount of equal sized data ' +
                        'sets created upon partitioning the data', type=int)
    ARGUMENTS = PARSER.parse_args()

    # Run the data classification script
    run(ARGUMENTS.data_path, ARGUMENTS.cv_amount)
