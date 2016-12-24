#!/usr/bin/env python2.7
# -*- coding: utf8 -*-i

from random import choice, randint, uniform
from multiprocessing import Pool, cpu_count
from .classification import classify, classifier_from_algorithm


def generate_parameter(parameter):
    if parameter[0] == tuple:
        return sampler_from_type[parameter[0]](parameter[1])
    else:
        return sampler_from_type[parameter[0]](*parameter[1])


def grid_search_iteration(data, algorithm, parameter_model):

    # Initialise the classifier
    classifier = classifier_from_algorithm[algorithm]

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

    # Initialise the multiprocessing pool.
    # The number of processes is set to be the CPU count, as the classification
    # is CPU-bound.
    pool = Pool(processes=cpu_count())

    # Run grid search and construct the results list
    raw_results = [pool.apply_async(grid_search_iteration, (data, algorithm,
                                                            parameter_model)) \
                   for i in range(number_of_iterations)]
    results = [result.get() for result in raw_results]

    # Prevent any more tasks to be submitted to the pool. Once all the tasks
    # have been completed, the worker processes will exit.
    pool.close()

    # Wait for all of the worker processes to finish.
    pool.join()

    # Return grid search results
    return results


sampler_from_type = {
    int: randint,
    float: uniform,
    tuple: choice
}
