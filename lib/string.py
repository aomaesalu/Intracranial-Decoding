#!/usr/bin/env python2.7
# -*- coding: utf8 -*-i


def pad(string, length, character=' '):
    return str(string) + (length - len(str(string))) * character


def format_path(path, number):

    # Split the path by points to find the file extension
    path = path.split('.')

    # Add the number just before the file extension, and return the updated
    # file path
    return '.'.join(path[:-1]) + '-' + str(number) + '.' + path[-1]
