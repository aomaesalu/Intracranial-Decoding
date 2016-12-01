#!/usr/bin/env python2.7
# -*- coding: utf8 -*-i

from .io import read_data
from .string import add_suffix_to_path
from .cross_validation import construct_data_sets
#from .score import ConfusionMatrix, Score
from sklearn.metrics import confusion_matrix, precision_recall_fscore_support


class Result(object):

    def __init__(self):#, labels):

        # # Set the label list from the parameter passed to the constructor
        # self.labels = labels

        # Intialise the true and predicted value lists
        self.true_values = []
        self.predicted_values = []

        # Initialise the result confusion matrix and scores per each class
        self.confusion_matrix = None
        self.scores_per_class = None
        self.average_scores = None


    def add_values(self, true_values, predictions):

        # Append the new true and predicted values to the existing lists
        self.true_values.append(true_values)
        self.predictions.append(predictions)


    def calculate(self):

        # Calculate the score matrix
        self.confusion_matrix = confusion_matrix(self.true_values,
                                                 self.predicted_values)#,
                                                 #self.labels)

        # Calculate the scores per each class
        pass # TODO

        # Calculate the average score
        # We are using macro averaging because it doesn't take class
        # distribution inbalance into account. Each class is as important as
        # another.
        score_labels = ['precision', 'recall', 'f1', 'support']
        average_scores = precision_recall_fscore_support(self.true_values,
                                                         self.predicted_values,
                                                         average='macro')
        for i in range(len(score_labels)):
            self.average_scores[score_labels[i]] = average_scores[i]


def classify(data_path, partitions, iterations, model):

    # Initialise the result of the classification
    result = Result()

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
