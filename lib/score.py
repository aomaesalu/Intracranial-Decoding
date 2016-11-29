#!/usr/bin/env python2.7
# -*- coding: utf8 -*-i

from sklearn.metrics import precision_score, recall_score, f1_score


def pad(string, length, character=' '):
    return str(string) + (length - len(str(string))) * character


class Score(object):

    def __init__(self, true_values, predictions):

        # Set data variables from parameters
        self.true_values = true_values
        self.predictions = predictions

        # Initialise score variables
        self.scores = {}
        self.average_scores = {}

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
            self.scores[image_class] = {
                'precision': precision_score(separated[image_class][0],
                                             separated[image_class][1]),
                'recall': recall_score(separated[image_class][0],
                                       separated[image_class][1]),
                'f1': f1_score(separated[image_class][0],
                               separated[image_class][1])
            }


    def calculate_average(self):

        # Calculate the average scores.
        # We are using macro averaging because it doesn't take class
        # distribution inbalance into account. Each class is as important as
        # another.
        self.average_scores = {
            'precision': precision_score(self.true_values, self.predictions,
                                         average='macro'),
            'recall': recall_score(self.true_values, self.predictions,
                                   average='macro'),
            'f1': f1_score(self.true_values, self.predictions, average='macro')
        }

    def __str__(self):
        methods = ['precision', 'recall', 'f1']
        output = 'Scores per class:\n'
        output += '    ' + pad('class', 8)
        for method in methods:
            output += pad(method, 16)
        output += '\n'
        for image_class, scores in sorted(self.scores.items()):
            output += '    ' + pad(image_class, 8)
            for method in methods:
                output += pad(scores[method], 16)
            output += '\n'
        output += 'Average scores:\n'
        for method in methods:
            output += '    ' + pad(method, 16) + \
                      pad(self.average_scores[method], 16) + '\n'
        return output
