#!/usr/bin/env python2.7
# -*- coding: utf8 -*-i

from .io import read_data
from .string import add_suffix_to_path
from .cross_validation import construct_data_sets
from .score import ConfusionMatrix, Score

from sklearn.metrics import f1_score
from sklearn.metrics import make_scorer
from sklearn.model_selection._search import RandomizedSearchCV


def classify(data_path, partitions, iterations, model, search_params, search_iterations):

    # Randomized parameter search
    f1_scorer = make_scorer(f1_score, average='macro')
    search = RandomizedSearchCV(estimator=model, param_distributions=search_params,
                                n_iter=search_iterations, scoring=f1_scorer, refit=True)

    # Initialise the true value and prediction lists
    true_values = []
    predictions = []

    # Repeat cross-validation a set amount of times
    for iteration in range(iterations):

        # Read input data
        data = []
        for partition in range(partitions):
            file_path = add_suffix_to_path(data_path, '-', iteration + 1,
                                           partition + 1)
            data.append(read_data(file_path))

        # Iterate through all of the data sets, using each of them for test data
        # exactly once, and using all others as training data sets at the same
        for test_index in range(partitions):

            # Construct training and test data sets
            train_data, test_data = construct_data_sets(data, partitions,
                                                        test_index)

            # Classification
            search.fit(train_data['neural_responses'],
                      train_data['image_category'])

            # Prediction
            prediction = search.predict(test_data['neural_responses'])

            # Append the true values and predictions to the corresponding
            # general lists for later scoring
            true_values += test_data['image_category']
            predictions += list(prediction)

    # Scoring
    confusion_matrix = ConfusionMatrix(true_values, predictions)
    score = Score(true_values, predictions)

    # Return results
    return confusion_matrix, score
