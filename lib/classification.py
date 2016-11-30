#!/usr/bin/env python2.7
# -*- coding: utf8 -*-i

from lib.io import read_data
from lib.string import format_path
from lib.cross_validation import construct_data_sets
from lib.score import ConfusionMatrix, Score


def classify(data_path, partitions, iterations, model):

    # Initialise the true value and prediction lists
    true_values = []
    predictions = []

    # Repeat cross-validation a set amount of times
    for iteration in range(iterations):

        # Read input data
        data = []
        for partition in range(partitions):
            data.append(read_data(format_path(format_path(data_path,
                                                          iteration + 1),
                                              partition + 1)))

        # Iterate through all of the data sets, using each of them for test data
        # exactly once, and using all others as training data sets at the same
        for test_index in range(partitions):

            # Construct training and test data sets
            train_data, test_data = construct_data_sets(data, partitions,
                                                        test_index)

            # Classification
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

    # Return results
    return confusion_matrix, score
