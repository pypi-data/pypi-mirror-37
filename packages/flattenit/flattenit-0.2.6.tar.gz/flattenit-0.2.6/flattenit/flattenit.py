# -*- coding: utf-8 -*-

"""Main module."""


def flattenit(matrix):
    """Return flattened list from 2D list of lists"""
    return [
        item
        for row in matrix
        for item in row
    ]
