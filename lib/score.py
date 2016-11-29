#!/usr/bin/env python2.7
# -*- coding: utf8 -*-i

from sklearn.metrics import f1_score

class Score(object):

    def __init__(self, true_values, predictions):

        # Set data variables from parameters
        self.true_values = true_values
        self.predictions = predictions

        # Initialise score variables
        self.scores = {}
        self.average_score = {}

        # Find all classes in test data
        self.classes = sorted(set(true_values))

        # Calculate scores
        self.calculate()

    def calculate(self):

        # Check that the true values and predictions are of the same size
        if len(self.true_values) != len(self.predictions):
            raise ValueError

        # Intialise the separated predictions dictionary
        separated = {}

        # Initialise dictionary values for each class
        for image_class in self.classes:
            self.scores[image_class] = None
            separated[image_class] = []

        # Separate the prediction data set by class
        for i in range(len(self.predictions)):
            separated[self.true_values[i]].append(self.predictions[i] == \
                                                  self.true_values[i])

        # Find the score for each class
        for image_class in self.classes:
            self.scores[image_class] = f1_score(len(separated[image_class]) * \
                                       [True], separated[image_class])

        # Calculate the average F1 score
        # We are using macro averaging because it doesn't take class
        # distribution inbalance into account. Each class is as important as
        # another.
        self.average_score = f1_score(self.true_values, self.predictions,
                                      average='macro')

    def __str__(self):
        output = 'F1 scores per class:\n'
        for image_class, score in sorted(self.scores.items()):
            output += '  ' + str(image_class) + ': ' + str(score) + '\n'
        output += 'Average F1 score: ' + str(self.average_score)
        return output
