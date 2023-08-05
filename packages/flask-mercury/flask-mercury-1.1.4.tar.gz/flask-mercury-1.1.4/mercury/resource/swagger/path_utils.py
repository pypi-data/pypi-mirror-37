# -*- coding: utf-8 -*-
"""
Module path_utils.py
---------------------
    utility functions to dealing with paths during serialization
"""
from mercury.parameters import path
import inspect
import re


# route substring replace map
ROUTE_REPLACE_MAP = {
    "int:": "",
    "float:": "",
    "path:": "",
    "any:": "",
    "uuid:": "",
    # Escape all the characters in pattern except ASCII letters, numbers and '_'.
    "\\<": "{",
    "\\>": "}",
    ":":  ""
}
# the route replace regex
ROUTE_REPLACE_REGEX = re.compile("|".join(ROUTE_REPLACE_MAP.keys()))


def format_base_path_swagger(cls):
    """
    Returns the swagger base path
    :param cls: a resource class.
    :return: the base resource path
    """
    # checks for route meta data
    if cls.ROUTE is not None:
        swagger_path = cls.ROUTE
        # then formats the parameters correctly
        swagger_path = ROUTE_REPLACE_REGEX.sub(
            lambda match: ROUTE_REPLACE_MAP[re.escape(match.group(0))],
            swagger_path
        )
        # swagger_path = swagger_path.replace(":", "")
    else:
        # otherwise uses the module dotted path as path
        mod = cls.__module__.split('.')

        if len(mod) > 0 and cls.__name__.lower() != mod[-1]:
            mod = "/".join(mod)
            swagger_path = "/{}/{}".format(mod, cls.__name__.lower())
        else:
            mod = "/".join(mod)
            swagger_path = "/{}".format(mod)

    return swagger_path


# ROUTE_REGEX = re.compile(
#     r"<int:\W+>|"
#     r"<float:\W+>|"
#     r"<path:\W+>|"
#     r"<any:\W+>|"
#     r"<uuid:\W+>|"
#     r"<\W+>",
#     re.IGNORECASE
# )
ROUTE_REGEX = re.compile(
    r"<([A-Za-z_0-9]*:?)[A-Za-z0-9_]*>",
    re.IGNORECASE
)

def get_base_path_parameters(cls):
    """
    Returns a dictionary containing the base path parameter names as key and
    it type's as value.
    :param cls: a resource class.
    :return: the base path parameters.
    """
    # prepare swagger paths
    params = dict()
    # checks for route meta data
    if cls.ROUTE:
        swagger_path = cls.ROUTE
        # searches for path parameters on the route
        path_parameters = ROUTE_REGEX.findall(swagger_path)
        # if found any query parameter on the route
        if len(path_parameters) > 0:
            for p in path_parameters:
                p = p.replace("<", "").replace(">", "").split(":")
                if len(p) > 1:
                    params[p[1]] = p[0]
                else:
                    params[p[0]] = None
    return params


def check_route_and_verb_path_parameter_specifications(cls, verb):
    """Checks the base route parameters and the verb function parameter definitions and
    raises an error when the verb does not defines some of the route defined parameters."""
    method = getattr(cls, verb, None)
    if method is not None:
        method_params = method.__params__

        # sanity check in the base_path parameters and method parameters
        p_name = [p.name for p in method_params]
        for param_name in get_base_path_parameters(cls).keys():
            if param_name not in p_name:
                raise NotImplementedError(
                    "The path parameter '{parameter}' defined on the base_path of the class '{cls}'"
                    "is not defined on the method '{method}' for the verb '{verb}'."
                    "The method '{method}' must receive all path_parameters as its parameters."
                    "".format(parameter=param_name, cls=cls.__qualname__, method=method.__qualname__, verb=verb)
                )


def find_additional_params(cls, verb):
    """
    Returns a list of parameters that are not defined on the base path.
    :param cls: a resource class.
    :param verb: the verb implementation.
    :return: a list of parameters that are not defined on the base path.
    """
    base_params = get_base_path_parameters(cls).keys()
    ret = list()
    for par in verb.__params__:
        if issubclass(par.annotation, path.BasePathParameter) and par.name not in base_params:
            ret.append(par)

    return ret


def filter_required_params(param_list):
    """
    Removes all parameters that has default value defined from the param_list and returns it.
    :param param_list: a list of verb parameters
    :return: a list of required parameters
    """
    ret = list()
    for par in param_list:
        if issubclass(par.annotation, path.BasePathParameter):
            if par.default is inspect._empty:
                ret.append('{'+par.name+'}')
    return ret


def filter_not_required_params(param_list):
    """
    Removes all parameters that has default value defined from the param_list and returns it.
    :param param_list: a list of verb parameters
    :return: a list of required parameters
    """
    ret = list()
    for par in param_list:
        if issubclass(par.annotation, path.BasePathParameter):
            if par.default is not inspect._empty:
                ret.append('{'+par.name+'}')
    return ret
