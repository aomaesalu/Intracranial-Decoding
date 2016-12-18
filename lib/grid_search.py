#!/usr/bin/env python2.7
# -*- coding: utf8 -*-i

from random import choice, randint, uniform


class DistinctParameter(object):

    def __init__(self, values):
        self.values = values

    def generate(self):
        return choice(self.values)


class ContinuousParameter(object):

    def __init__(self, low, high, sampler):
        self.low = low
        self.high = high
        self.sampler = sampler

    def generate(self):
        return self.sampler(self.low, self.high)


class IntParameter(ContinuousParameter):

    def __init__(self, low, high):
        super(IntParameter, self).__init__(low, high, randint)


class FloatParameter(ContinuousParameter):

    def __init__(self, low, high):
        super(FloatParameter, self).__init__(low, high, uniform)


def grid_search(classify, algorithm, model, number_of_iterations):

    # Initialise the grid search results list
    results = []

    # Repeat grid search a set amount of times
    for iteration in range(number_of_iterations):

        # Generate model parameters
        parameters = {}
        for name, parameter in model['parameters'].items():
            parameters[name] = parameter.generate()

        pass # TODO

    # Return grid search results
    return results
