# -*- coding: utf-8 -*-
"""
Package parameters:
-----------------------
 Flask-Mercury *query* parameter type definitions.
"""
import inspect
from ..base import BaseParameter
from flask import request


class BaseQueryParameter(BaseParameter):
    """
    Base path parameter class
    """
    @classmethod
    def to_swagger(cls, param, doc):
        """
        Base query parameter spec serialization function.
        """
        spec = super().to_swagger(param, doc)
        spec["in"] = "query"

        return spec

    @classmethod
    def from_request(cls, name, default=None):
        value = request.args.get(name, default)
        if value is not None:
            return cls(name, value)
        else:
            return None