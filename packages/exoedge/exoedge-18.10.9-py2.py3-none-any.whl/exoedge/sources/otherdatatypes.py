"""
Module for testing data types
"""

def iam_object(**kwargs):
    return kwargs


def iam_list(**kwargs):
    return kwargs.values()


def iam_tuple(**kwargs):
    return zip(kwargs.keys(), kwargs.values())[0]


def iam_bool(**kwargs):
    key = kwargs.keys()[0]
    return key == kwargs[key]

