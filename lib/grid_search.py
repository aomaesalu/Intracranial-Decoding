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

    def generate(self):
        return uniform(self.low, self.high)


class IntParameter(ContinuousParameter):

    def __init(self, low, high):
        super(IntParameter, self).__init__(low, high, randint)


class FloatParameter(ContinuousParameter):

    def __init__(self, low, high):
        super(FloatParameter, self).__init__(low, high, uniform)
