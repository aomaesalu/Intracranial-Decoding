#!/usr/bin/env python2.7
# -*- coding: utf8 -*-i

from sklearn.metrics import precision_score, recall_score, f1_score
from string import pad

# TODO: Use the confusion matrix in scoring


class ConfusionMatrix(object):

    def __init__(self, true_values, predictions):

        # Set data variables from parameters
        self.true_values = true_values
        self.predictions = predictions

        # Find all classes
        self.classes = sorted(set(true_values) | set(predictions))

        # Initialise matrix
        self.initialise()

        # Construct confusion matrix
        self.construct()

    def initialise(self):

        # Create a complete confusion matrix with 0-s
        self.matrix = {}
        for class_1 in self.classes:
            self.matrix[class_1] = {}
            for class_2 in self.classes:
                self.matrix[class_1][class_2] = 0

    def construct(self):

        for i in range(len(self.predictions)):
            self.matrix[self.true_values[i]][self.predictions[i]] += 1

    def __str__(self):
        output = 'Confusion matrix:\n'
        output += '    ' + pad('class', 8)
        for class_2 in self.classes:
            output += pad(class_2, 8)
        output += '\n'
        for class_1 in self.classes:
            output += '    ' + pad(class_1, 8)
            for class_2 in self.classes:
                output += pad(self.matrix[class_1][class_2], 8)
            output += '\n'
        return output


class Score(object):

    def __init__(self, true_values, predictions):

        # Set data variables from parameters
        self.true_values = true_values
        self.predictions = predictions

        # Initialise score variables
        self.scores = {}
        self.average_scores = {}

        # Find all classes in test data
        self.classes = sorted(set(true_values) | set(predictions))

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
