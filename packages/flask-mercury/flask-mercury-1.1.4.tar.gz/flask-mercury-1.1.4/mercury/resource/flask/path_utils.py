# -*- coding: utf-8 -*-
"""
Module path_utils.py
---------------------
    utility functions to dealing with paths during serialization
"""
from mercury.parameters import path
import inspect
import re


# ROUTE_REGEX = re.compile(r"^/\W+/$", re.IGNORECASE)
ROUTE_REGEX = re.compile(
    r"^<int:\W+>|"
    r"<float:\W+>|"
    r"<path:\W+>|"
    r"<any:\W+>|"
    r"<uuid:\W+>|"
    r"<\W+>$",
    re.IGNORECASE
)


def get_route_parameters(route_path):
    """
    Returns a list of parameters defined on the flask route string.
    :param route_path: a route path string.
    :return: a list of parameter names
    """
    # get the resource base path
    # checks for route meta data
    parameters = list()
    # builds a base path parameter lists
    for p in ROUTE_REGEX.findall(route_path):
        p.replace("<", "").split(":")
        if len(p) > 1:
            parameters.append(p[1])
        else:
            parameters.append(p[0])
    return