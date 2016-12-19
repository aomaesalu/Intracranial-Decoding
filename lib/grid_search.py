#!/usr/bin/env python2.7
# -*- coding: utf8 -*-i

from random import choice, randint, uniform
from multiprocessing import Pool, cpu_count
from .classification import classify, classifierFromAlgorithm


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


def generate_parameter(parameter):
    if parameter[0] == tuple:
        return samplerFromType[parameter[0]](parameter[1])
    else:
        return samplerFromType[parameter[0]](*parameter[1])


def grid_search_iteration(data, algorithm, parameter_model):

    # Initialise the classifier
    classifier = classifierFromAlgorithm[algorithm]

    # Generate model parameters
    parameters = {}
    for name, parameter in parameter_model.items():
        parameters[name] = generate_parameter(parameter)

    # Set the generated parameters to the classifier
    classifier.set_params(**parameters)

    # Classify, predict and score the classifier
    results = classify(data, classifier)

    # Return the classification results for the algorithm with the generated
    # parameters
    return {
        'algorithm': algorithm,
        'parameters': parameters,
        'f1': results.average_f1(),
        'predicted_values': results.predicted_values
    }


def grid_search(data, algorithm, parameter_model, number_of_iterations):

    # Initialise the grid search results list
    results = []

    # Initialise the multiprocessing pool
    pool = Pool(processes=cpu_count())

    # Run grid search and construct the results list
    raw_results = [pool.apply_async(grid_search_iteration, (data, algorithm, parameter_model)) for i in range(number_of_iterations)]
    results = [result.get() for result in raw_results]

    # Prevent any more tasks to be submitted to the pool. Once all the tasks
    # have been completed, the worker processes will exit.
    pool.close()

    # Wait for all of the worker processes to finish.
    pool.join()

    # Return grid search results
    return results


samplerFromType = {
    int: randint,
    float: uniform,
    tuple: choice
}
