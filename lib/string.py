#!/usr/bin/env python2.7
# -*- coding: utf8 -*-i


def pad(string, length, character=' '):
    return str(string) + (length - len(str(string))) * character


def add_suffix_to_path(path, separator, *suffixes):

    # Split the path by points to find the file extension
    path_components = path.split('.')

    # Change suffixes to strings
    suffixes = [str(suffix) for suffix in suffixes]

    # Add suffixes to the file name with the specified separator
    path_components[-2] = '-'.join([path_components[-2], '-'.join(suffixes)])

    # Join the path components in order, and return the resulting new path
    return '.'.join(path_components)
