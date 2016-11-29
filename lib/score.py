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
        self.calculate_separated()
        self.calculate_average()

    def calculate_separated(self):

        # Check that the true values and predictions are of the same size
        if len(self.true_values) != len(self.predictions):
            raise ValueError

        # Intialise the separated predictions dictionary
        separated = {}

        # Initialise dictionary values for each class
        for image_class in self.classes:
            self.scores[image_class] = None
            separated[image_class] = [[], []]

        # Separate the prediction data set by class
        for i in range(len(self.predictions)):
            if self.true_values[i] == self.predictions[i]:
                for j in range(2):
                    separated[self.true_values[i]][j].append(True)
            else:
                separated[self.true_values[i]][0].append(True)
                separated[self.true_values[i]][1].append(False)
                separated[self.predictions[i]][0].append(False)
                separated[self.predictions[i]][1].append(True)

        # Find the score for each class
        for image_class in self.classes:
            self.scores[image_class] = f1_score(separated[image_class][0],
                                                separated[image_class][1])

    def calculate_average(self):

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
