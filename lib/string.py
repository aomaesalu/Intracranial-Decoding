#!/usr/bin/env python2.7
# -*- coding: utf8 -*-i


def pad(string, length, character=' '):
    return str(string) + (length - len(str(string))) * character
