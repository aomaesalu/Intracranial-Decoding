#!/usr/bin/env python2.7
# -*- coding: utf8 -*-i

from sklearn.metrics import f1_score


def calculate_scores(true_values, predictions):

    # Check that the true values and predictions are of the same size
    if len(true_values) != len(predictions):
        raise ValueError

    # Initialise the score dictionary
    scores = {}

    # Intialise the separated predictions dictionary
    separated_predictions = {}

    # Find all classes in test data
    classes = sorted(set(true_values))

    # Initialise dictionary values for each class
    for image_class in classes:
        scores[image_class] = None
        separated_predictions[image_class] = []

    # Separate the prediction data set by class
    for i in range(len(predictions)):
        separated_predictions[true_values[i]].append(predictions[i] == \
                                                     true_values[i])

    # Find the score for each class
    for image_class in classes:
        scores[image_class] = f1_score(len(separated_predictions[image_class]) * [True], separated_predictions[image_class])

    # Return the score dictionary and the average score for the whole data set
    # We are using macro averaging because it doesn't take class distribution
    # inbalance into account. Each class is as important as another.
    return scores, f1_score(true_values, predictions, average='macro')
