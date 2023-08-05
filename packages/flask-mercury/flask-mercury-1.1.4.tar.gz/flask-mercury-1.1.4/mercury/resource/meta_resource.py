# -*- coding: utf-8 -*-
"""
Module meta_resource.py
---------------------
    Metaclass implementation for the api resource
"""
from flask.views import MethodView
import inspect
from mercury import utils
from flask.views import MethodViewType
from . import _verbs


class MetaResource(MethodViewType):
    """
    A Api Resource Meta class.
    """
    def __new__(mcs, what, bases=None, namespace=None):
        """
        Meta Resource constructor function.
        :param what: The resource class name.
        :param bases: A collection of superclasses.
        :param namespace: The namespace __dict__ for the class.
        """
        cls = super(MetaResource, mcs).__new__(mcs, what, bases, namespace)
        for verb in _verbs:
            mcs.get_signature(cls, verb)
        return cls

    def get_signature(cls, name):
        """
        Sets __params__, __pdoc__, __returns__ attribute to functions that are
        verb implementation.
        :param name: the function name.
        """
        if hasattr(cls, name):
            method = getattr(cls, name)
            signature = inspect.signature(method)
            method_params = list(signature.parameters.values())
            # add the meta attribute __params__ to the method dict
            object.__setattr__(method, "__params__", method_params)
            # add the meta attribute __pdoc__ containing the parsed method doc string
            object.__setattr__(method, "__pdoc__", utils.parse_docstring(method.__doc__))
            # adds the meta attribute __returns__
            object.__setattr__(method, "__returns__", signature.return_annotation)


# the base resource class
BaseResource = MetaResource("BaseResource", (MethodView,), dict())
